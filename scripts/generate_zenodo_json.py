#!/usr/bin/env python3
"""Generate .zenodo.json from CITATION.cff plus scripts/zenodo-overlay.json.

Zenodo ignores CITATION.cff entirely when .zenodo.json is present, so keeping both
by hand means maintaining the author list twice. CITATION.cff is the source of
truth here: CFF splits a person into given-names / name-particle / family-names,
and joining those into Zenodo's flat "Family, Given" string is lossless, while
splitting the flat string back would be a guess.

The overlay holds what CFF cannot express (upload_type, publication_type,
related_identifiers), because CFF's type enum is software|dataset and its schema
sets additionalProperties: false.

Usage:
    python3 scripts/generate_zenodo_json.py            # write .zenodo.json
    python3 scripts/generate_zenodo_json.py --check    # exit 1 if it is stale
"""

import argparse
import json
import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
CFF = REPO / "CITATION.cff"
OVERLAY = REPO / "scripts" / "zenodo-overlay.json"
OUT = REPO / ".zenodo.json"


def creator(person):
    """CFF person -> Zenodo creator ("Family, Given", affiliation, bare ORCID)."""
    family = " ".join(p for p in (person.get("name-particle"),
                                  person.get("family-names")) if p)
    given = person.get("given-names", "")
    out = {"name": f"{family}, {given}" if given else family}
    if person.get("affiliation"):
        out["affiliation"] = person["affiliation"]
    if person.get("orcid"):
        # Zenodo wants the bare identifier, not the resolver URL.
        out["orcid"] = person["orcid"].rsplit("/", 1)[-1]
    return out


def build():
    cff = yaml.safe_load(CFF.read_text())
    overlay = json.loads(OVERLAY.read_text())

    meta = {
        "title": cff["title"],
        # CFF folds the abstract across lines; Zenodo wants one block of text.
        "description": re.sub(r"\s+", " ", cff["abstract"]).strip(),
        "creators": [creator(p) for p in cff["authors"]],
        "keywords": list(cff.get("keywords", [])),
        "license": cff["license"].lower(),
        "version": str(cff["version"]),
        "publication_date": str(cff["date-released"]),
    }
    meta.update({k: v for k, v in overlay.items() if not k.startswith("_")})
    return json.dumps(meta, indent=2, ensure_ascii=False) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="verify .zenodo.json matches CITATION.cff; do not write")
    args = ap.parse_args()

    generated = build()

    if args.check:
        current = OUT.read_text() if OUT.exists() else ""
        if current != generated:
            print(f"{OUT.name} is out of date; run "
                  f"'python3 scripts/generate_zenodo_json.py'", file=sys.stderr)
            return 1
        print(f"{OUT.name} is in sync with {CFF.name}")
        return 0

    OUT.write_text(generated)
    print(f"wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
