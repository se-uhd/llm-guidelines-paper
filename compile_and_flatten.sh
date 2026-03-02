#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAIN_TEX="emse25-llm-guidelines.tex"
FLAT_OUTPUT="${1:-$PROJECT_DIR/emse25-llm-guidelines-flat.tex}"

cd "$PROJECT_DIR"

echo "Compiling $MAIN_TEX..."
latexmk -pdf "$MAIN_TEX"

echo "Flattening to $FLAT_OUTPUT..."
latexpand --keep-comments \
  --in-encoding 'encoding(UTF-8)' \
  --out-encoding 'encoding(UTF-8)' \
  "$MAIN_TEX" > "$FLAT_OUTPUT"

echo "Done: $(basename "$FLAT_OUTPUT")"
