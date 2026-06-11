#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAIN_TEX="emse26-llm-guidelines.tex"
FLAT_OUTPUT="${1:-$PROJECT_DIR/emse26-llm-guidelines-flat.tex}"
LATEX_AUXILIARY_SUFFIXES=(
  aux
  bbl
  bcf
  blg
  fdb_latexmk
  fls
  lof
  log
  lot
  out
  run.xml
  synctex.gz
  toc
)

cd "$PROJECT_DIR"

cleanup_latex_auxiliary_files() {
  local tex_path="$1"
  local tex_dir stem suffix

  tex_dir="$(cd "$(dirname "$tex_path")" && pwd)"
  stem="$(basename "$tex_path" .tex)"

  for suffix in "${LATEX_AUXILIARY_SUFFIXES[@]}"; do
    rm -f "$tex_dir/$stem.$suffix"
  done
}

echo "Compiling $MAIN_TEX..."
cleanup_latex_auxiliary_files "$PROJECT_DIR/$MAIN_TEX"
latexmk -pdf -interaction=nonstopmode -halt-on-error "$MAIN_TEX"

echo "Flattening to $FLAT_OUTPUT..."
python3 "$PROJECT_DIR/scripts/flatten_latex.py" "$PROJECT_DIR/$MAIN_TEX" "$FLAT_OUTPUT"

echo "Compiling $(basename "$FLAT_OUTPUT")..."
cleanup_latex_auxiliary_files "$FLAT_OUTPUT"
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd "$FLAT_OUTPUT"
cleanup_latex_auxiliary_files "$PROJECT_DIR/$MAIN_TEX"
cleanup_latex_auxiliary_files "$FLAT_OUTPUT"

echo "Done: ${MAIN_TEX%.tex}.pdf, $(basename "${FLAT_OUTPUT%.tex}").pdf"
