#!/usr/bin/env python3
"""Handle remaining unmatched bibliography entries after DBLP cleanup.

Steps:
  1. Crossref enrichment for entries with DOIs
  2. DBLP fuzzy search for category-B entries without DOIs
  3. URL validation for @misc entries with howpublished URLs
  4. Categorized summary report
"""

import json
import re
import subprocess
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

PROJECT = Path(__file__).resolve().parent.parent
BIB_FILE = PROJECT / "literature.bib"
REPORT_FILE = PROJECT / "dblp_unmatched_report.txt"

DBLP_SEARCH_URL = "https://dblp.uni-trier.de/search/publ/api?q={query}&format=json&h=10"
DBLP_REC_URL = "https://dblp.uni-trier.de/rec/{key}.bib"
CROSSREF_URL = "https://api.crossref.org/works/{doi}"

# ── The 27 non-misc unmatched entries, categorized ──────────────────────────

CAT_A_ARXIV = {
    "bjarnason2026randomnessagenticevals",
    "cao2025should",
    "ralph2021empiricalstandardssoftwareengineering",
}

CAT_B_PUBLISHED_CS = {
    "10.1145/3695988",
    "anandayuvaraj2024fail",
    "JIANG2024202",
    "Kistowski2015Benchmark",
    "Liang2024",
    "ronanki2023investigating",
    "russo2024navigating",
    "YuanNondeterminismLLMInference",
}

CAT_C_NON_CS = {
    "Begg1996",
    "doi:10.1148/radiol.232411",
    "Gallifant2025",
    "Gibney2024",
    "guba1981criteria",
    "SCHILKE2025104405",
    "Sullivan2011-ub",
    "ZHAO2025101167",
}

CAT_C_PRIME = {
    "khraisha2024canlargelanguagemodelshumans",
    "widder2024open",
}

CAT_D_GRAY = {
    "acm2020artifactreview",
    "daniel_graziotin_2024_10796477",
    "Huang2023Enhancing",
    "jowsey2025reject",
    "mitu2024hidden",
    "wiesinger2025agents",
}

ALL_UNMATCHED = CAT_A_ARXIV | CAT_B_PUBLISHED_CS | CAT_C_NON_CS | CAT_C_PRIME | CAT_D_GRAY

# Entries known to be @misc with howpublished URLs (fine as-is)
MISC_WITH_URLS = {
    "ACM2023", "Azure25", "Chandra2025benchmarks", "Chann2023",
    "OSIAI2024", "OpenAI23", "OpenAI25", "codebert",
    "continue.dev", "technology_innovation_institute_2023", "together2023redpajama",
}


# ── Utility functions ───────────────────────────────────────────────────────

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
                    wait = 3 * (attempt + 1)
                    print(f"    (429, wait {wait}s) ", end="", flush=True)
                    time.sleep(wait)
                    continue
                if status.startswith("2") and body.strip():
                    return body
        except (subprocess.TimeoutExpired, OSError):
            pass
        if attempt < retries - 1:
            time.sleep(2)
    return None


def check_url_status(url, timeout=10):
    """Check if a URL is reachable. Returns (status_code, final_url) or (None, None)."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{url_effective}",
             "-L", "--max-time", str(timeout), "--max-redirs", "5", url],
            capture_output=True, text=True, timeout=timeout + 5,
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split(" ", 1)
            code = int(parts[0])
            final = parts[1] if len(parts) > 1 else url
            return code, final
    except (subprocess.TimeoutExpired, OSError, ValueError):
        pass
    return None, None


def normalize_title(title):
    """Normalize a title for comparison."""
    t = title.lower()
    t = re.sub(r"[{}\\]", "", t)
    t = unicodedata.normalize("NFKD", t)
    t = re.sub(r"[^a-z0-9 ]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


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


def extract_doi(entry):
    """Extract a clean DOI from the entry's doi field."""
    doi = entry.get("doi", "").strip()
    if not doi:
        return None
    # Strip URL prefix if present
    doi = re.sub(r"^https?://doi\.org/", "", doi)
    doi = re.sub(r"^https?://dx\.doi\.org/", "", doi)
    return doi if doi else None


def get_category(key):
    """Return the category label for a given key."""
    if key in CAT_A_ARXIV:
        return "A (arXiv preprint)"
    if key in CAT_B_PUBLISHED_CS:
        return "B (published CS/SE)"
    if key in CAT_C_NON_CS:
        return "C (non-CS journal)"
    if key in CAT_C_PRIME:
        return "C' (non-CS academic)"
    if key in CAT_D_GRAY:
        return "D (gray literature)"
    if key in MISC_WITH_URLS:
        return "misc (website/docs)"
    return "unknown"


# ── Step 1: Crossref enrichment ─────────────────────────────────────────────

def fetch_crossref(doi):
    """Fetch metadata from Crossref for a DOI. Returns dict or None."""
    url = CROSSREF_URL.format(doi=quote(doi, safe=""))
    raw = fetch_url(url, timeout=20)
    if not raw:
        return None
    try:
        data = json.loads(raw)
        return data.get("message", {})
    except (json.JSONDecodeError, KeyError):
        return None


def enrich_from_crossref(entry, cr_data):
    """Enrich a bib entry with Crossref metadata. Returns list of fields added/updated."""
    changes = []

    # Volume
    if not entry.get("volume") and cr_data.get("volume"):
        entry["volume"] = cr_data["volume"]
        changes.append("volume")

    # Issue/number
    if not entry.get("number") and cr_data.get("issue"):
        entry["number"] = cr_data["issue"]
        changes.append("number")

    # Pages
    if not entry.get("pages") and cr_data.get("page"):
        entry["pages"] = cr_data["page"]
        changes.append("pages")

    # Publisher
    if not entry.get("publisher") and cr_data.get("publisher"):
        entry["publisher"] = cr_data["publisher"]
        changes.append("publisher")

    # ISSN
    if not entry.get("issn") and cr_data.get("ISSN"):
        issns = cr_data["ISSN"]
        if isinstance(issns, list) and issns:
            entry["issn"] = issns[0]
            changes.append("issn")

    # DOI (normalize — remove URL prefix if we added one)
    doi_val = entry.get("doi", "")
    if doi_val.startswith("https://doi.org/") or doi_val.startswith("http://doi.org/"):
        clean = re.sub(r"^https?://doi\.org/", "", doi_val)
        if clean != doi_val:
            entry["doi"] = clean
            changes.append("doi (normalized)")
    elif doi_val.startswith("https://dx.doi.org/"):
        clean = re.sub(r"^https?://dx\.doi\.org/", "", doi_val)
        if clean != doi_val:
            entry["doi"] = clean
            changes.append("doi (normalized)")

    # Journal name (only if missing — skip for @inproceedings which use booktitle)
    if cr_data.get("container-title") and entry.get("ENTRYTYPE", "").lower() != "inproceedings":
        ct = cr_data["container-title"]
        journal_name = ct[0] if isinstance(ct, list) and ct else str(ct) if ct else ""
        if journal_name and not entry.get("journal"):
            entry["journal"] = journal_name
            changes.append("journal")

    # Year (only if missing)
    if not entry.get("year") and cr_data.get("published"):
        parts = cr_data["published"].get("date-parts", [[]])
        if parts and parts[0]:
            entry["year"] = str(parts[0][0])
            changes.append("year")

    return changes


def step1_crossref(bib_db, key_to_idx):
    """Enrich entries that have DOIs via Crossref."""
    print("\n" + "=" * 60)
    print("Step 1: Crossref enrichment for entries with DOIs")
    print("=" * 60)

    enriched = {}  # key -> list of changed fields
    failed = []

    # Find all unmatched entries with DOIs
    targets = []
    for key in ALL_UNMATCHED:
        idx = key_to_idx.get(key)
        if idx is None:
            continue
        entry = bib_db.entries[idx]
        doi = extract_doi(entry)
        if doi:
            targets.append((key, idx, doi))

    print(f"  Found {len(targets)} entries with DOIs\n")

    for seq, (key, idx, doi) in enumerate(targets, 1):
        entry = bib_db.entries[idx]
        cat = get_category(key)
        print(f"  [{seq}/{len(targets)}] {key} ({cat})")
        print(f"    DOI: {doi}")

        cr_data = fetch_crossref(doi)
        if cr_data:
            changes = enrich_from_crossref(entry, cr_data)
            if changes:
                enriched[key] = changes
                print(f"    Enriched: {', '.join(changes)}")
            else:
                print(f"    No new fields to add (already complete)")
        else:
            failed.append(key)
            print(f"    Crossref lookup failed")

        time.sleep(1)  # polite rate limit

    print(f"\n  Summary: {len(enriched)} enriched, {len(failed)} failed, "
          f"{len(targets) - len(enriched) - len(failed)} already complete")
    return enriched, failed


# ── Step 2: DBLP fuzzy search for Cat B without DOIs ────────────────────────

def fuzzy_dblp_search(title, author_surname=None, year=None):
    """Search DBLP with aggressive normalization. Returns parsed entry or None."""
    # Strategy 1: full title search
    query = title
    entry = _dblp_search_query(query, title)
    if entry:
        return entry

    # Strategy 2: strip subtitle (after : or —)
    short_title = re.split(r"[:\u2014\u2013\-]{1,2}\s", title, maxsplit=1)[0].strip()
    if short_title != title and len(short_title) > 15:
        entry = _dblp_search_query(short_title, title)
        if entry:
            return entry

    # Strategy 3: author surname + year
    if author_surname and year:
        query = f"{author_surname} {year}"
        entry = _dblp_search_query(query, title)
        if entry:
            return entry

    return None


def _dblp_search_query(query, original_title):
    """Execute a DBLP search and return best matching entry or None."""
    url = DBLP_SEARCH_URL.format(query=quote(query))
    raw = fetch_url(url)
    if not raw:
        return None
    try:
        data = json.loads(raw)
        hits = data.get("result", {}).get("hits", {}).get("hit", [])
    except (json.JSONDecodeError, KeyError):
        return None

    norm_local = normalize_title(original_title)
    for hit in hits:
        info = hit.get("info", {})
        dblp_title = info.get("title", "")
        if dblp_title.endswith("."):
            dblp_title = dblp_title[:-1]
        if normalize_title(dblp_title) == norm_local:
            dblp_key = info.get("key", "")
            if dblp_key:
                bib_url = DBLP_REC_URL.format(key=dblp_key)
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
        if journal in ("arxiv", "corr", ""):
            return True
    return False


def dblp_is_better(local, dblp_entry):
    """Determine if DBLP entry is better than local."""
    if is_arxiv_or_corr(local) and not is_arxiv_or_corr(dblp_entry):
        return True
    metadata_fields = {"doi", "pages", "volume", "number", "publisher", "booktitle"}
    local_count = sum(1 for f in metadata_fields if local.get(f))
    dblp_count = sum(1 for f in metadata_fields if dblp_entry.get(f))
    return dblp_count > local_count


def extract_first_author_surname(entry):
    """Extract first author's surname from author field."""
    author = entry.get("author", "")
    if not author:
        return None
    # Handle "Surname, First" or "First Surname" format
    first_author = re.split(r"\s+and\s+", author, maxsplit=1)[0].strip()
    if "," in first_author:
        return first_author.split(",")[0].strip()
    parts = first_author.split()
    return parts[-1] if parts else None


def step2_dblp_fuzzy(bib_db, key_to_idx, already_enriched):
    """DBLP fuzzy search for category-B entries without DOIs."""
    print("\n" + "=" * 60)
    print("Step 2: DBLP fuzzy search for Cat B entries without DOIs")
    print("=" * 60)

    # Cat B entries that don't have a DOI
    targets = []
    for key in CAT_B_PUBLISHED_CS:
        idx = key_to_idx.get(key)
        if idx is None:
            continue
        entry = bib_db.entries[idx]
        doi = extract_doi(entry)
        if not doi:
            targets.append((key, idx))

    print(f"  Found {len(targets)} Cat B entries without DOIs\n")

    upgraded = []
    for seq, (key, idx) in enumerate(targets, 1):
        entry = bib_db.entries[idx]
        title = entry.get("title", "")
        surname = extract_first_author_surname(entry)
        year = entry.get("year", "")

        print(f"  [{seq}/{len(targets)}] {key}")
        print(f"    Title: {title[:80]}")
        print(f"    Searching DBLP (fuzzy)...", end=" ", flush=True)

        dblp_entry = fuzzy_dblp_search(title, surname, year)
        if dblp_entry:
            if dblp_is_better(entry, dblp_entry):
                dblp_entry["ID"] = key
                bib_db.entries[idx] = dblp_entry
                upgraded.append(key)
                print(f"UPGRADED ({entry.get('ENTRYTYPE','?')} -> {dblp_entry.get('ENTRYTYPE','?')})")
            else:
                print(f"FOUND but not better")
        else:
            print(f"NO MATCH")

        time.sleep(3)  # rate limit

    print(f"\n  Summary: {len(upgraded)} upgraded via DBLP fuzzy search")
    return upgraded


# ── Step 3: Validate @misc URLs ─────────────────────────────────────────────

def extract_url_from_howpublished(entry):
    """Extract URL from howpublished field."""
    hp = entry.get("howpublished", "")
    m = re.search(r"\\url\{([^}]+)\}", hp)
    if m:
        return m.group(1).replace("\\_", "_")
    return None


def step3_validate_urls(bib_db, key_to_idx):
    """Validate URLs in @misc entries with howpublished."""
    print("\n" + "=" * 60)
    print("Step 3: Validate @misc URLs")
    print("=" * 60)

    targets = []
    for key in MISC_WITH_URLS:
        idx = key_to_idx.get(key)
        if idx is None:
            continue
        entry = bib_db.entries[idx]
        url = extract_url_from_howpublished(entry)
        if url:
            targets.append((key, url))

    print(f"  Checking {len(targets)} URLs\n")

    ok_urls = []
    broken_urls = []
    for seq, (key, url) in enumerate(targets, 1):
        print(f"  [{seq}/{len(targets)}] {key}")
        print(f"    URL: {url[:80]}")
        print(f"    Status: ", end="", flush=True)

        status, final = check_url_status(url)
        if status and 200 <= status < 400:
            ok_urls.append((key, url, status))
            print(f"{status} OK")
        elif status:
            broken_urls.append((key, url, status))
            print(f"{status} BROKEN")
        else:
            broken_urls.append((key, url, None))
            print(f"TIMEOUT/ERROR")

        time.sleep(0.5)

    print(f"\n  Summary: {len(ok_urls)} OK, {len(broken_urls)} broken/unreachable")
    return ok_urls, broken_urls


# ── Step 5: Report ──────────────────────────────────────────────────────────

def write_report(crossref_enriched, crossref_failed, dblp_upgraded, ok_urls, broken_urls):
    """Append results to dblp_unmatched_report.txt."""
    lines = []
    lines.append("")
    lines.append("=" * 72)
    lines.append("Remaining Unmatched Entries — Final Handling")
    lines.append("=" * 72)
    lines.append("")

    # Crossref results
    lines.append("-" * 72)
    lines.append(f"Crossref enrichment: {len(crossref_enriched)} entries enriched")
    lines.append("-" * 72)
    if crossref_enriched:
        for key, fields in sorted(crossref_enriched.items()):
            lines.append(f"  {key}: added {', '.join(fields)}")
    if crossref_failed:
        lines.append(f"  Failed Crossref lookups: {', '.join(sorted(crossref_failed))}")
    lines.append("")

    # DBLP fuzzy results
    lines.append("-" * 72)
    lines.append(f"DBLP fuzzy search: {len(dblp_upgraded)} entries upgraded")
    lines.append("-" * 72)
    if dblp_upgraded:
        for key in sorted(dblp_upgraded):
            lines.append(f"  {key}")
    lines.append("")

    # URL validation
    lines.append("-" * 72)
    lines.append(f"URL validation: {len(ok_urls)} OK, {len(broken_urls)} broken")
    lines.append("-" * 72)
    if broken_urls:
        for key, url, status in sorted(broken_urls):
            lines.append(f"  BROKEN: {key} -> {url} (status: {status})")
    lines.append("")

    # Remaining by category
    lines.append("-" * 72)
    lines.append("Remaining entries by category (no further action needed):")
    lines.append("-" * 72)

    cats = [
        ("A — arXiv preprints (genuinely unpublished)", sorted(CAT_A_ARXIV)),
        ("B — Published CS/SE (DBLP title search failed, entries OK as-is)", sorted(CAT_B_PUBLISHED_CS - set(dblp_upgraded))),
        ("C — Non-CS journals (not on DBLP, enriched via Crossref where possible)", sorted(CAT_C_NON_CS)),
        ("C' — Non-CS academic (enriched via Crossref where possible)", sorted(CAT_C_PRIME)),
        ("D — Gray literature (whitepapers, Zenodo, SSRN, policy docs)", sorted(CAT_D_GRAY)),
        ("Misc — Websites/docs with URLs", sorted(MISC_WITH_URLS)),
    ]
    for label, keys in cats:
        if keys:
            lines.append(f"\n  {label}:")
            for k in keys:
                lines.append(f"    - {k}")

    lines.append("")

    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nReport appended to {REPORT_FILE.name}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Handle Remaining Unmatched Bibliography Entries")
    print("=" * 60)

    # Parse bib
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with open(BIB_FILE, encoding="utf-8") as f:
        bib_db = bibtexparser.load(f, parser=parser)
    print(f"Parsed {len(bib_db.entries)} entries from {BIB_FILE.name}")

    # Build key -> index map
    key_to_idx = {e["ID"]: i for i, e in enumerate(bib_db.entries)}

    # Verify all expected keys exist
    missing = (ALL_UNMATCHED | MISC_WITH_URLS) - set(key_to_idx.keys())
    if missing:
        print(f"\n  Warning: {len(missing)} expected keys not found in bib: {missing}")

    # Step 1: Crossref
    crossref_enriched, crossref_failed = step1_crossref(bib_db, key_to_idx)

    # Step 2: DBLP fuzzy
    dblp_upgraded = step2_dblp_fuzzy(bib_db, key_to_idx, crossref_enriched)

    # Step 3: URL validation
    ok_urls, broken_urls = step3_validate_urls(bib_db, key_to_idx)

    # Write updated bib
    if crossref_enriched or dblp_upgraded:
        writer = BibTexWriter()
        writer.indent = "  "
        writer.comma_first = False
        with open(BIB_FILE, "w", encoding="utf-8") as f:
            f.write(writer.write(bib_db))
        print(f"\nWrote {len(bib_db.entries)} entries to {BIB_FILE.name}")
    else:
        print("\nNo changes to write.")

    # Step 5: Report
    print("\n" + "=" * 60)
    print("Step 5: Summary Report")
    print("=" * 60)
    write_report(crossref_enriched, crossref_failed, dblp_upgraded, ok_urls, broken_urls)

    print("\nDone!")


if __name__ == "__main__":
    main()
