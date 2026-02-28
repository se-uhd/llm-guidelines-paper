#!/bin/bash
set -euo pipefail

OLD_DIR="${1:-../papers/llm-guidelines-paper}"
MAIN_TEX="emse25-llm-guidelines.tex"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

OLD_DIR="$(cd "$OLD_DIR" && pwd)"

echo "Flattening old version from $OLD_DIR..."
(cd "$OLD_DIR" && latexpand "$MAIN_TEX" --output /tmp/old_flat.tex)

echo "Flattening current version..."
(cd "$PROJECT_DIR" && latexpand "$MAIN_TEX" --output /tmp/new_flat.tex)

echo "Generating diff markup..."
mkdir -p "$PROJECT_DIR/versions"
latexdiff /tmp/old_flat.tex /tmp/new_flat.tex > "$PROJECT_DIR/versions/diff.tex"


# Merge bibliographies: the diff references citations from both old and new
# versions. The current literature.bib may be missing entries that were removed
# or renamed during bibliography cleanup. We create a merged bib file that
# contains all entries from both versions (current entries take precedence).
echo "Merging bibliographies..."
python3 -c "
import re, sys

def parse_entries(path):
    \"\"\"Return dict mapping citation key -> full bib entry string.\"\"\"
    with open(path) as f:
        text = f.read()
    entries = {}
    for m in re.finditer(r'(@\w+\{)([^,]+),(.*?)(?=\n@|\Z)', text, re.DOTALL):
        key = m.group(2).strip()
        entries[key] = m.group(0)
    return entries

old = parse_entries('$OLD_DIR/literature.bib')
new = parse_entries('$PROJECT_DIR/literature.bib')

# Start with all new entries, then add old entries that are missing
merged = dict(new)
added = 0
for key, entry in old.items():
    if key not in merged:
        merged[key] = entry
        added += 1

with open('$PROJECT_DIR/versions/literature_merged.bib', 'w') as f:
    f.write('\n\n'.join(merged.values()))
    f.write('\n')

print(f'Merged bibliography: {len(new)} current + {added} old-only = {len(merged)} total entries')
"

# Point diff.tex to the merged bibliography
sed -i '' 's|\\bibliography{literature}|\\bibliography{versions/literature_merged}|' "$PROJECT_DIR/versions/diff.tex"

# Clean stale build artifacts to ensure bibtex re-runs with the merged bib
rm -f "$PROJECT_DIR"/versions/diff.{bbl,aux,blg,log,fls,fdb_latexmk,out,pdf}

echo "Compiling diff PDF..."
cd "$PROJECT_DIR"
latexmk -pdf -jobname=versions/diff -silent versions/diff.tex
# latexmk sometimes stops one pass short for the diff; run one extra pass
# to ensure all \bibcite entries from the .aux are resolved
pdflatex -interaction=nonstopmode -jobname=versions/diff versions/diff.tex > /dev/null 2>&1

# Verify no undefined citations remain
UNDEF=$(grep -c "Citation.*undefined" versions/diff.log 2>/dev/null || echo 0)
if [ "$UNDEF" -gt 0 ]; then
    echo "WARNING: $UNDEF undefined citation(s) remain — check versions/diff.log"
fi

echo "Cleaning auxiliary files..."
rm -f "$PROJECT_DIR"/versions/diff.{aux,bbl,blg,log,fls,fdb_latexmk,out,toc,lof,lot}

echo "Done: versions/diff.pdf"
