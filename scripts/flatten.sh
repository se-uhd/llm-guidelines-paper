#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT="${1:-$PROJECT_DIR/emse26-llm-guidelines-flat.tex}"

cd "$PROJECT_DIR"
latexpand --keep-comments \
  --in-encoding 'encoding(UTF-8)' \
  --out-encoding 'encoding(UTF-8)' \
  emse26-llm-guidelines.tex > "$OUTPUT"

echo "Flattened to $OUTPUT"
