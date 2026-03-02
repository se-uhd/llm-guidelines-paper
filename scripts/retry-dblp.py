#!/usr/bin/env python3
"""Retry DBLP lookups for entries that failed in the initial run."""

import re
import json
import subprocess
import time
import unicodedata
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

PROJECT = Path(__file__).resolve().parent.parent
BIB_FILE = PROJECT / "literature.bib"
REPORT_FILE = PROJECT / "dblp_unmatched_report.txt"

DBLP_REC_URL = "https://dblp.uni-trier.de/rec/{key}.bib"
DELAY = 5  # seconds between requests


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
                    wait = 5 * (attempt + 1)
                    print(f"(429, wait {wait}s) ", end="", flush=True)
                    time.sleep(wait)
                    continue
                if status.startswith("2") and body.strip():
                    return body
        except (subprocess.TimeoutExpired, OSError):
            pass
        if attempt < retries - 1:
            time.sleep(3)
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


def is_arxiv_or_corr(entry):
    """Check if entry is an arXiv/CoRR preprint."""
    journal = entry.get("journal", "").lower()
    if "corr" in journal or "arxiv" in journal:
        return True
    eprint = entry.get("eprint", "")
    if eprint and "arxiv" in entry.get("archiveprefix", "").lower():
        return True
    if "arxiv" in entry.get("url", "").lower():
        if journal in ("arxiv", "corr", ""):
            return True
    return False


def dblp_is_better(local, dblp_entry):
    """Determine if DBLP entry is better than local entry."""
    if is_arxiv_or_corr(local) and not is_arxiv_or_corr(dblp_entry):
        return True
    metadata_fields = {"doi", "pages", "volume", "number", "publisher", "booktitle"}
    local_count = sum(1 for f in metadata_fields if local.get(f))
    dblp_count = sum(1 for f in metadata_fields if dblp_entry.get(f))
    if dblp_count > local_count:
        return True
    return False


def extract_failed_keys():
    """Parse dblp_unmatched_report.txt for keys still needing retry.

    If a 'Still failed keys' section exists (from a previous retry), use that.
    Otherwise fall back to all 'DBLP key fetch failed' entries.
    """
    text = REPORT_FILE.read_text()

    # Check for previous retry's "Still failed keys" section
    marker = "Still failed keys:"
    if marker in text:
        section = text.split(marker)[-1]
        keys = re.findall(r"- (.+)", section)
        if keys:
            return [k.strip() for k in keys]

    # Fall back to original report
    blocks = text.split("  Key:    ")
    keys = []
    for b in blocks[1:]:
        if "DBLP key fetch failed" in b:
            key = b.split("\n")[0].strip()
            keys.append(key)
    return keys


def dblp_rec_key_from_entry(key, entry):
    """Get DBLP record key from citation key or biburl."""
    if key.startswith("DBLP:"):
        return key[5:]
    biburl = entry.get("biburl", "")
    m = re.search(r"dblp\.org/rec/(.+?)\.bib", biburl)
    if m:
        return m.group(1)
    return None


def main():
    failed_keys = extract_failed_keys()
    print(f"Retrying {len(failed_keys)} DBLP key fetch failures\n")

    # Parse current bib
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with open(BIB_FILE, encoding="utf-8") as f:
        bib_db = bibtexparser.load(f, parser=parser)

    # Build key -> index map
    key_to_idx = {e["ID"]: i for i, e in enumerate(bib_db.entries)}

    upgraded = []
    still_failed = []
    ok_entries = []

    for seq, key in enumerate(failed_keys, 1):
        idx = key_to_idx.get(key)
        if idx is None:
            print(f"  [{seq}/{len(failed_keys)}] {key} — NOT FOUND in bib, skipping")
            continue

        entry = bib_db.entries[idx]
        rec_key = dblp_rec_key_from_entry(key, entry)
        if not rec_key:
            print(f"  [{seq}/{len(failed_keys)}] {key} — no DBLP rec key, skipping")
            still_failed.append(key)
            continue

        print(f"  [{seq}/{len(failed_keys)}] {key}...", end=" ", flush=True)

        url = DBLP_REC_URL.format(key=rec_key)
        bib_str = fetch_url(url)
        if not bib_str:
            print("FAILED")
            still_failed.append(key)
            time.sleep(DELAY)
            continue

        dblp_entry = parse_single_bib(bib_str)
        if not dblp_entry:
            print("PARSE ERROR")
            still_failed.append(key)
            time.sleep(DELAY)
            continue

        if dblp_is_better(entry, dblp_entry):
            dblp_entry["ID"] = key  # preserve citation key
            bib_db.entries[idx] = dblp_entry
            upgraded.append(key)
            print(f"UPGRADED (was {entry.get('ENTRYTYPE','?')}, now {dblp_entry.get('ENTRYTYPE','?')})")
        else:
            ok_entries.append(key)
            print("OK (DBLP not better)")

        time.sleep(DELAY)

    # Write updated bib
    if upgraded:
        writer = BibTexWriter()
        writer.indent = "  "
        writer.comma_first = False
        with open(BIB_FILE, "w", encoding="utf-8") as f:
            f.write(writer.write(bib_db))

    # Update report
    report_lines = []
    report_lines.append("")
    report_lines.append("=" * 72)
    report_lines.append("DBLP Retry Results")
    report_lines.append("=" * 72)
    report_lines.append(f"  Retried:       {len(failed_keys)}")
    report_lines.append(f"  Upgraded:      {len(upgraded)}")
    report_lines.append(f"  OK (no change):{len(ok_entries)}")
    report_lines.append(f"  Still failed:  {len(still_failed)}")
    if upgraded:
        report_lines.append("")
        report_lines.append("  Upgraded keys:")
        for k in sorted(upgraded):
            report_lines.append(f"    - {k}")
    if still_failed:
        report_lines.append("")
        report_lines.append("  Still failed keys:")
        for k in sorted(still_failed):
            report_lines.append(f"    - {k}")

    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print(f"\nDone! Upgraded: {len(upgraded)}, OK: {len(ok_entries)}, Still failed: {len(still_failed)}")
    if upgraded:
        print("Upgraded:", ", ".join(sorted(upgraded)))


if __name__ == "__main__":
    main()
