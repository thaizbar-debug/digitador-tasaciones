#!/bin/bash
# Doble click a este archivo para iniciar el servidor local y abrir el navegador.
# La primera vez tarda ~1 minuto instalando dependencias en un entorno virtual.

set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
    osascript -e 'display alert "Python 3 no está instalado" message "Instalá Python desde https://www.python.org/downloads/ y volvé a intentar."'
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Configurando entorno Python por primera vez (~1 minuto)..."
    python3 -m venv .venv
    .venv/bin/pip install --quiet --upgrade pip
    .venv/bin/pip install --quiet -r server/requirements.txt
fi

# Abrir el navegador cuando el server esté listo.
(
    for i in {1..30}; do
        if curl -s http://127.0.0.1:5555/health >/dev/null 2>&1; then
            open "http://localhost:5555/"
            exit 0
        fi
        sleep 0.3
    done
    echo "El server tardó demasiado en arrancar; abrí http://localhost:5555/ manualmente."
) &

echo "Servidor corriendo en http://localhost:5555/"
echo "Cerrá esta ventana o presioná Ctrl+C cuando termines de trabajar."
echo ""
.venv/bin/python server/server.py
