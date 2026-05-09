#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 <a.pdf> <b.pdf> [diff-output]" >&2
  exit 2
fi

a=$1
b=$2
diff_file=${3:-"$(dirname "$a")/pdf-text.diff"}

for f in "$a" "$b"; do
  [[ -f $f ]] || { echo "missing: $f" >&2; exit 2; }
done

command -v pdftotext >/dev/null || { echo "pdftotext not installed" >&2; exit 2; }

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

pdftotext -layout "$a" "$tmp/a.txt"
pdftotext -layout "$b" "$tmp/b.txt"

set +e
diff -u "$tmp/a.txt" "$tmp/b.txt" > "$diff_file"
rc=$?
set -e

case $rc in
  0)
    rm -f "$diff_file"
    echo "PDFs match (text-equivalent)."
    exit 0
    ;;
  1)
    echo "PDFs differ. Diff written to $diff_file."
    echo "--- begin diff ---"
    cat "$diff_file"
    echo "--- end diff ---"
    exit 1
    ;;
  *)
    echo "diff failed with status $rc" >&2
    exit "$rc"
    ;;
esac
