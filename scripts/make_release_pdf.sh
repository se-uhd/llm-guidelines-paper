#!/usr/bin/env bash
#
# Build the tracked release PDF for the version named in CITATION.cff.
#
# Zenodo archives the tag's source zipball and ignores files attached to a GitHub
# release, so the PDF has to be committed for the DOI record to hold a readable
# document.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

VERSION="$(python3 -c "import yaml; print(yaml.safe_load(open('CITATION.cff'))['version'])")"
OUT="release/llm-guidelines-${VERSION}.pdf"

echo "[1/3] compile emse26-llm-guidelines.tex"
latexmk -pdf -interaction=nonstopmode -halt-on-error emse26-llm-guidelines.tex >/dev/null

echo "[2/3] copy -> $OUT"
mkdir -p release
# Keep exactly one PDF per tag, so each archived release is unambiguous.
find release -maxdepth 1 -name 'llm-guidelines-*.pdf' ! -name "$(basename "$OUT")" -delete
cp emse26-llm-guidelines.pdf "$OUT"

echo "[3/3] clean auxiliary files"
latexmk -c emse26-llm-guidelines.tex >/dev/null

echo
echo "Done: $OUT ($(du -h "$OUT" | cut -f1))"
