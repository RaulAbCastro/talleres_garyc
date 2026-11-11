#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
project_dir="$PWD"
source .devcontainer/texlive-version.env
export PATH="/usr/local/bin:$PATH"
document="${1:-all}"
document="${document%.tex}"
case "$document" in
  all) documents=(temario recursos caso) ;;
  temario|recursos|caso) documents=("$document") ;;
  *) printf 'Uso: bash scripts/render-overleaf.sh [all|temario|recursos|caso]\n' >&2; exit 2 ;;
esac
if [[ ! -f documents_overleaf/.git ]]; then
  printf 'Descarga los documentos con bash scripts/overleaf.sh init.\n' >&2
  exit 1
fi
tex_version="$(pdflatex --version)"
if [[ "$tex_version" != *"TeX Live $TEXLIVE_YEAR"* ]]; then
  printf 'Se requiere TeX Live %s. Ejecuta bash .devcontainer/install-tex.sh.\n' "$TEXLIVE_YEAR" >&2
  exit 1
fi
mkdir -p outputs/overleaf
cd documents_overleaf
for document in "${documents[@]}"; do
  if [[ ! -f "$document.tex" ]]; then
    printf 'Falta %s.tex. Comprueba la revisión con bash scripts/overleaf.sh check.\n' "$document" >&2
    exit 1
  fi
  latexmk -g -pdf '-pdflatex=/usr/local/bin/pdflatex %O %S' \
    -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error \
    -outdir=build "$document.tex"
  cp "build/$document.pdf" "$project_dir/outputs/overleaf/$document.pdf"
  printf 'PDF generado: documents_overleaf/build/%s.pdf\n' "$document"
done
