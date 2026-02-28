#!/usr/bin/env bash
set -euo pipefail

OUTPUT="${1:-emse25-llm-guidelines-flat.tex}"

latexpand --keep-comments \
  --in-encoding 'encoding(UTF-8)' \
  --out-encoding 'encoding(UTF-8)' \
  emse25-llm-guidelines.tex > "$OUTPUT"

echo "Flattened to $OUTPUT"
