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

# Renderizar todas las sesiones
for document in taller-1/sesion-1/index.qmd taller-1/sesion-2/index.qmd; do
  if [[ "$action" == "render" ]]; then
    printf '\n📊 Compilando: %s\n' "$document"
    quarto render "$document"
  fi
done

# Para preview, solo la primera sesión
if [[ "$action" == "preview" ]]; then
  document="taller-1/sesion-1/index.qmd"
  exec quarto preview "$document" --host 0.0.0.0 --port 4200 --no-browser
fi
