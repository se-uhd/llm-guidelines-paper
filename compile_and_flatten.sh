#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAIN_TEX="emse26-llm-guidelines.tex"
FLAT_OUTPUT="${1:-$PROJECT_DIR/emse26-llm-guidelines-flat.tex}"

cd "$PROJECT_DIR"

echo "Compiling $MAIN_TEX..."
latexmk -pdf -interaction=nonstopmode -halt-on-error "$MAIN_TEX"

echo "Flattening to $FLAT_OUTPUT..."
latexpand --keep-comments \
  --in-encoding 'encoding(UTF-8)' \
  --out-encoding 'encoding(UTF-8)' \
  "$MAIN_TEX" > "$FLAT_OUTPUT"

echo "Compiling $(basename "$FLAT_OUTPUT")..."
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd "$FLAT_OUTPUT"

echo "Done: ${MAIN_TEX%.tex}.pdf, $(basename "${FLAT_OUTPUT%.tex}").pdf"
