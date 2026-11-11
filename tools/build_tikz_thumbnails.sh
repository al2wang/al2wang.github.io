#!/bin/bash
# Compile images/publications/tikz/*.tex and convert each to images/publications/<name>.webp.
#
# Usage: tools/build_tikz_thumbnails.sh [name.tex ...]   (default: every drawing)
# Needs pdflatex with TikZ and fontawesome5, and a Python with PyMuPDF and Pillow
# (point PYTHON at it if python3 lacks them).
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
build=$(mktemp -d)
trap 'rm -rf "${build:?}"' EXIT

cd "$root/images/publications/tikz"
files=("$@")
[ ${#files[@]} -eq 0 ] && files=(*.tex)
for tex in "${files[@]}"; do
  [ "$tex" = thumbstyle.tex ] && continue
  name=${tex%.tex}
  if ! pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$build" "$tex" >/dev/null; then
    grep -A5 '^!' "$build/$name.log" || tail -20 "$build/$name.log"
    exit 1
  fi
  "${PYTHON:-python3}" "$root/tools/make_thumbnail.py" "$build/$name.pdf" "$root/images/publications/$name.webp"
done
