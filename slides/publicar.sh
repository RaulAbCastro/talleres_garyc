#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

# Construir con la misma configuración y versión que la vista previa local.
bash render.sh render

# Preparar únicamente el sitio de participantes. Mantener las rutas relativas
# permite servirlo tanto en / como en /talleres_garyc/ en GitHub Pages.
site_dir="$PWD/_site"
session_dir="taller-1/sesion-1"
for file in index.html "$session_dir/index.html" \
    "$session_dir/datos/muestra.csv" "$session_dir/datos/poblacion_saldos.csv" \
    "$session_dir/codigo/sesion-1.R" "$session_dir/codigo/sesion-1.py" \
    "$session_dir/codigo/sesion-1.do"; do
  test -s "$file"
done
test -d "$session_dir/index_files"

# _site es un directorio generado por este script; se reconstruye en cada ejecución.
rm -rf -- "$site_dir"
mkdir -p "$site_dir/$session_dir/datos" "$site_dir/$session_dir/codigo"
cp index.html "$site_dir/index.html"
for file in index.html interacciones.js animaciones.js animaciones.css; do
  cp "$session_dir/$file" "$site_dir/$session_dir/$file"
done
for directory in index_files assets; do
  cp -R "$session_dir/$directory" "$site_dir/$session_dir/$directory"
done
for file in muestra.csv poblacion_saldos.csv; do
  cp "$session_dir/datos/$file" "$site_dir/$session_dir/datos/$file"
done
for file in sesion-1.R sesion-1.py sesion-1.do; do
  cp "$session_dir/codigo/$file" "$site_dir/$session_dir/codigo/$file"
done
touch "$site_dir/.nojekyll"
printf 'Sitio listo en %s\n' "$site_dir"
