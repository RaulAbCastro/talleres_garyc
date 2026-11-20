#!/bin/bash

# Script para iniciar el servidor de presentaciones
# Uso: ./start-server.sh [puerto]

PORT=${1:-8000}
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Iniciando servidor de presentaciones..."
echo "📂 Directorio: $DIR"
echo "🔌 Puerto: $PORT"
echo ""

cd "$DIR"
python3 -m http.server $PORT

echo ""
echo "✅ Servidor detenido"
