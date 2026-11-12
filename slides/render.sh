#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
action="${1:-render}"
case "$action" in
  render|preview) ;;
  *) printf 'Uso: bash slides/render.sh [render|preview]\n' >&2; exit 2 ;;
esac
# La caché queda en un directorio escribible también en entornos restringidos.
export XDG_CACHE_HOME="${TMPDIR:-/tmp}/talleres-quarto-cache"
document="taller-1/sesion-1/index.qmd"
if [[ "$action" == preview ]]; then
  exec quarto preview "$document" --host 0.0.0.0 --port 4200 --no-browser
fi
exec quarto render "$document"
