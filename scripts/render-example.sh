#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
language="${1:-python}"
format="${2:-html}"
case "$language" in python|r) ;; *) printf 'Usa python o r.\n' >&2; exit 2 ;; esac
case "$format" in html|pdf) ;; *) printf 'Usa html o pdf.\n' >&2; exit 2 ;; esac
export PATH="$PWD/.venv/bin:$PATH"
export QUARTO_PYTHON="$PWD/.venv/bin/python"
export RETICULATE_PYTHON="$QUARTO_PYTHON"
mkdir -p outputs
quarto render "code/examples/hola-${language}.qmd" --to "$format" --output-dir ../../outputs
