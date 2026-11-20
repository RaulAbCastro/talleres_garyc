#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

# Construir con la misma configuración y versión que la vista previa local.
bash render.sh render

# Preparar únicamente el sitio de participantes. Mantener las rutas relativas
# permite servirlo tanto en / como en /talleres_garyc/ en GitHub Pages.
site_dir="$PWD/_site"

# Verificar que las sesiones existen y están compiladas
for session in sesion-1 sesion-2; do
  session_dir="taller-1/$session"
  for file in ../website/index.html ../website/styles.css "$session_dir/index.html" \
      "$session_dir/datos/muestra.csv" \
      "$session_dir/codigo/$session.R" "$session_dir/codigo/$session.py" "$session_dir/codigo/$session.do"; do
    test -s "$file" || echo "⚠️  Falta: $file"
  done
  test -d "$session_dir/index_files" || echo "⚠️  Falta directorio: $session_dir/index_files"
done

# _site es un directorio generado por este script; se reconstruye en cada ejecución.
rm -rf -- "$site_dir"

# Copiar website raíz
mkdir -p "$site_dir"
cp ../website/index.html ../website/styles.css "$site_dir/"

# Copiar slides/index.html (página de índice de presentaciones)
cp index.html "$site_dir/"

# Procesar cada sesión
for session in sesion-1 sesion-2; do
  session_dir="taller-1/$session"
  mkdir -p "$site_dir/$session_dir/datos" "$site_dir/$session_dir/codigo"
  
  # Copiar archivos principales
  for file in index.html interacciones.js animaciones.js animaciones.css tema.scss; do
    if [ -f "$session_dir/$file" ]; then
      cp "$session_dir/$file" "$site_dir/$session_dir/$file"
    fi
  done
  
  # Copiar directorios
  for directory in index_files assets; do
    if [ -d "$session_dir/$directory" ]; then
      cp -R "$session_dir/$directory" "$site_dir/$session_dir/$directory"
    fi
  done
  
  # Copiar datos según la sesión
  if [ "$session" = "sesion-1" ]; then
    datos_files="muestra.csv poblacion_saldos.csv"
  else
    datos_files="muestra.csv poblacion_potencial.csv"
  fi
  
  for file in $datos_files; do
    if [ -f "$session_dir/datos/$file" ]; then
      cp "$session_dir/datos/$file" "$site_dir/$session_dir/datos/$file"
    fi
  done
  
  # Copiar código
  for file in "$session.R" "$session.py" "$session.do"; do
    if [ -f "$session_dir/codigo/$file" ]; then
      cp "$session_dir/codigo/$file" "$site_dir/$session_dir/codigo/$file"
    fi
  done
done

touch "$site_dir/.nojekyll"
printf 'Sitio listo en %s\n' "$site_dir"
