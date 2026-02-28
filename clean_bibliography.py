#!/usr/bin/env python3
"""Clean and update literature.bib: remove unreferenced entries, upgrade from DBLP."""

import re
import json
import shutil
import subprocess
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

PROJECT = Path(__file__).resolve().parent
BIB_FILE = PROJECT / "literature.bib"
AUX_FILE = PROJECT / "emse25-llm-guidelines.aux"
BACKUP_FILE = PROJECT / "literature.bib.backup"
REPORT_FILE = PROJECT / "dblp_unmatched_report.txt"

DBLP_REC_URL = "https://dblp.uni-trier.de/rec/{key}.bib"
DBLP_SEARCH_URL = "https://dblp.uni-trier.de/search/publ/api?q={query}&format=json&h=5"

CITE_RE = re.compile(r"\\cite[tp]?\*?\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}")
AUX_CITE_RE = re.compile(r"\\citation\{([^}]+)\}")
COMMENT_RE = re.compile(r"(?<!\\)%.*$", re.MULTILINE)

# ── Step 1: collect referenced keys ──────────────────────────────────────────

def keys_from_tex_files():
    """Parse all .tex files for \\cite commands, return set of keys."""
    keys = set()
    for tex in PROJECT.rglob("*.tex"):
        text = tex.read_text(errors="replace")
        text = COMMENT_RE.sub("", text)  # strip comments
        for m in CITE_RE.finditer(text):
            for k in m.group(1).split(","):
                k = k.strip()
                if k:
                    keys.add(k)
    return keys


def keys_from_aux():
    """Parse .aux file for \\citation{} entries, return set of keys."""
    keys = set()
    if not AUX_FILE.exists():
        print(f"  Warning: {AUX_FILE.name} not found, skipping aux keys")
        return keys
    text = AUX_FILE.read_text(errors="replace")
    for m in AUX_CITE_RE.finditer(text):
        for k in m.group(1).split(","):
            k = k.strip()
            if k:
                keys.add(k)
    return keys


def remove_unreferenced(bib_db, referenced_keys):
    """Remove entries not in referenced_keys. Returns list of removed keys."""
    kept, removed = [], []
    for entry in bib_db.entries:
        if entry["ID"] in referenced_keys:
            kept.append(entry)
        else:
            removed.append(entry["ID"])
    bib_db.entries = kept
    return removed


# ── Step 2: DBLP lookup ─────────────────────────────────────────────────────

def normalize_title(title):
    """Normalize a title for comparison: lowercase, strip braces, collapse whitespace."""
    t = title.lower()
    t = re.sub(r"[{}\\]", "", t)
    t = unicodedata.normalize("NFKD", t)
    t = re.sub(r"[^a-z0-9 ]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def fetch_url(url, timeout=15, retries=3):
    """Fetch URL content as string via curl, with retry on 429/failure."""
    for attempt in range(retries):
        try:
            result = subprocess.run(
                ["curl", "-s", "-w", "\n%{http_code}", "--max-time", str(timeout), url],
                capture_output=True, text=True, timeout=timeout + 5,
            )
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.rsplit("\n", 1)
                body = lines[0] if len(lines) > 1 else result.stdout
                status = lines[-1].strip() if len(lines) > 1 else ""
                if status == "429":
                    # Rate limited — back off and retry
                    wait = 3 * (attempt + 1)
                    print(f"(429, wait {wait}s) ", end="", flush=True)
                    time.sleep(wait)
                    continue
                if status.startswith("2") and body.strip():
                    return body
        except (subprocess.TimeoutExpired, OSError):
            pass
        if attempt < retries - 1:
            time.sleep(2)
    return None


def parse_single_bib(bib_str):
    """Parse a bib string and return the first entry dict, or None."""
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    try:
        db = bibtexparser.loads(bib_str, parser=parser)
        if db.entries:
            return db.entries[0]
    except Exception:
        pass
    return None


def fetch_dblp_by_key(dblp_key):
    """Fetch a DBLP entry by its key. Returns parsed entry dict or None."""
    # dblp_key might be like "DBLP:conf/icse/KangYY23" -> we need "conf/icse/KangYY23"
    key = dblp_key
    if key.startswith("DBLP:"):
        key = key[5:]
    url = DBLP_REC_URL.format(key=key)
    bib_str = fetch_url(url)
    if bib_str:
        return parse_single_bib(bib_str)
    return None


def fetch_dblp_by_title(title):
    """Search DBLP by title. Returns best matching entry dict or None."""
    query = quote(title)
    url = DBLP_SEARCH_URL.format(query=query)
    raw = fetch_url(url)
    if not raw:
        return None
    try:
        data = json.loads(raw)
        hits = data.get("result", {}).get("hits", {}).get("hit", [])
    except (json.JSONDecodeError, KeyError):
        return None

    norm_local = normalize_title(title)
    for hit in hits:
        info = hit.get("info", {})
        dblp_title = info.get("title", "")
        if dblp_title.endswith("."):
            dblp_title = dblp_title[:-1]
        if normalize_title(dblp_title) == norm_local:
            # Found match — fetch full bib
            dblp_key = info.get("key", "")
            if dblp_key:
                bib_url = f"https://dblp.uni-trier.de/rec/{dblp_key}.bib"
                bib_str = fetch_url(bib_url)
                if bib_str:
                    return parse_single_bib(bib_str)
    return None


def is_arxiv_or_corr(entry):
    """Check if entry is an arXiv/CoRR preprint."""
    journal = entry.get("journal", "").lower()
    if "corr" in journal or "arxiv" in journal:
        return True
    eprint = entry.get("eprint", "")
    if eprint and "arxiv" in entry.get("archiveprefix", "").lower():
        return True
    if "arxiv" in entry.get("url", "").lower():
        # Also check if journal field suggests arXiv
        if journal in ("arxiv", "corr", ""):
            return True
    return False


def is_misc_with_url(entry):
    """Check if entry is @misc with howpublished URL (website/docs/blog)."""
    return (entry.get("ENTRYTYPE", "").lower() == "misc"
            and "howpublished" in entry
            and "\\url{" in entry.get("howpublished", ""))


def dblp_is_better(local, dblp_entry):
    """Determine if DBLP entry is better than local entry."""
    # If local is arXiv but DBLP has a published venue, that's better
    if is_arxiv_or_corr(local):
        if not is_arxiv_or_corr(dblp_entry):
            return True

    # Count metadata fields
    metadata_fields = {"doi", "pages", "volume", "number", "publisher", "booktitle"}
    local_count = sum(1 for f in metadata_fields if local.get(f))
    dblp_count = sum(1 for f in metadata_fields if dblp_entry.get(f))
    if dblp_count > local_count:
        return True

    return False


def has_dblp_biburl(entry):
    """Check if entry has a DBLP biburl."""
    return "dblp.org" in entry.get("biburl", "")


def dblp_key_from_biburl(entry):
    """Extract DBLP record key from biburl field."""
    biburl = entry.get("biburl", "")
    # e.g. https://dblp.org/rec/conf/icse/KangYY23.bib -> conf/icse/KangYY23
    m = re.search(r"dblp\.org/rec/(.+?)\.bib", biburl)
    if m:
        return m.group(1)
    return None


def process_entries_dblp(bib_db):
    """Check entries against DBLP, upgrade where possible.

    Returns (upgraded_keys, unmatched_entries) where unmatched_entries is
    list of (key, entry_type, title, reason).
    """
    upgraded = []
    unmatched = []
    total = len(bib_db.entries)

    for i, entry in enumerate(bib_db.entries):
        key = entry["ID"]
        title = entry.get("title", "")
        entry_type = entry.get("ENTRYTYPE", "")

        print(f"  [{i+1}/{total}] {key[:60]}...", end=" ", flush=True)

        # Skip @misc with howpublished URLs
        if is_misc_with_url(entry):
            print("SKIP (misc+url)")
            unmatched.append((key, entry_type, title, "Skipped: @misc with howpublished URL"))
            continue

        dblp_entry = None
        reason = ""

        # Strategy 1: entry has DBLP key prefix or biburl
        if key.startswith("DBLP:") or has_dblp_biburl(entry):
            dblp_rec_key = None
            if key.startswith("DBLP:"):
                dblp_rec_key = key[5:]
            elif has_dblp_biburl(entry):
                dblp_rec_key = dblp_key_from_biburl(entry)

            if dblp_rec_key:
                dblp_entry = fetch_dblp_by_key(dblp_rec_key)
                if not dblp_entry:
                    reason = "DBLP key fetch failed"
        else:
            # Strategy 2: search by title
            if title:
                time.sleep(2)  # rate limit for search
                dblp_entry = fetch_dblp_by_title(title)
                if not dblp_entry:
                    reason = "No DBLP match by title"
            else:
                reason = "No title field"

        if dblp_entry:
            if dblp_is_better(entry, dblp_entry):
                # Upgrade: replace entry but keep original citation key
                old_dblp_id = dblp_entry["ID"]
                dblp_entry["ID"] = key
                bib_db.entries[i] = dblp_entry
                upgraded.append(key)
                print(f"UPGRADED (was {entry_type}, now {dblp_entry.get('ENTRYTYPE', '?')})")
            else:
                print("OK (DBLP not better)")
        else:
            print(f"UNMATCHED ({reason})")
            unmatched.append((key, entry_type, title, reason))

        # Rate limit between all DBLP requests
        time.sleep(2)

    return upgraded, unmatched


# ── Step 3: report ───────────────────────────────────────────────────────────

def write_report(removed, upgraded, unmatched):
    """Write dblp_unmatched_report.txt."""
    lines = []
    lines.append("=" * 72)
    lines.append("Bibliography Cleanup Report")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"Unreferenced entries removed:  {len(removed)}")
    lines.append(f"Entries upgraded from DBLP:     {len(upgraded)}")
    lines.append(f"Unmatched entries (for review): {len(unmatched)}")
    lines.append("")

    if removed:
        lines.append("-" * 72)
        lines.append("Removed (unreferenced) keys:")
        lines.append("-" * 72)
        for k in sorted(removed):
            lines.append(f"  - {k}")
        lines.append("")

    if upgraded:
        lines.append("-" * 72)
        lines.append("Upgraded from DBLP:")
        lines.append("-" * 72)
        for k in sorted(upgraded):
            lines.append(f"  - {k}")
        lines.append("")

    if unmatched:
        lines.append("-" * 72)
        lines.append("Unmatched entries (manual review needed):")
        lines.append("-" * 72)
        for key, etype, title, reason in sorted(unmatched, key=lambda x: x[0]):
            lines.append(f"  Key:    {key}")
            lines.append(f"  Type:   @{etype}")
            lines.append(f"  Title:  {title[:100]}")
            lines.append(f"  Reason: {reason}")
            lines.append("")

    REPORT_FILE.write_text("\n".join(lines))
    print(f"\nReport written to {REPORT_FILE.name}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Bibliography Cleanup")
    print("=" * 60)

    # Back up
    shutil.copy2(BIB_FILE, BACKUP_FILE)
    print(f"\nBackup: {BACKUP_FILE.name}")

    # Parse bib
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with open(BIB_FILE, encoding="utf-8") as f:
        bib_db = bibtexparser.load(f, parser=parser)
    print(f"Parsed {len(bib_db.entries)} entries from {BIB_FILE.name}")

    # Step 1: remove unreferenced
    print("\n--- Step 1: Remove unreferenced entries ---")
    tex_keys = keys_from_tex_files()
    aux_keys = keys_from_aux()
    referenced = tex_keys | aux_keys
    print(f"  Keys from .tex files: {len(tex_keys)}")
    print(f"  Keys from .aux file:  {len(aux_keys)}")
    print(f"  Union (referenced):   {len(referenced)}")

    removed = remove_unreferenced(bib_db, referenced)
    print(f"  Removed {len(removed)} unreferenced entries")
    if removed:
        for k in sorted(removed):
            print(f"    - {k}")
    print(f"  Remaining entries: {len(bib_db.entries)}")

    # Step 2: DBLP check
    print("\n--- Step 2: Check entries against DBLP ---")
    upgraded, unmatched = process_entries_dblp(bib_db)

    # Write cleaned bib
    writer = BibTexWriter()
    writer.indent = "  "
    writer.comma_first = False
    with open(BIB_FILE, "w", encoding="utf-8") as f:
        f.write(writer.write(bib_db))
    print(f"\nWrote {len(bib_db.entries)} entries to {BIB_FILE.name}")

    # Step 3: report
    print("\n--- Step 3: Write report ---")
    write_report(removed, upgraded, unmatched)

    print("\nDone!")


if __name__ == "__main__":
    main()
