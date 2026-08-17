#!/bin/bash
# Empaqueta las plantillas oficiales de cada banco en web/plantillas.js
# como strings base64, para que web/index.html las use sin necesidad de
# servidor. Corre este script cada vez que actualices un formato en formatos/.

set -e
cd "$(dirname "$0")"

OUT="web/plantillas.js"

{
  echo "// Auto generado por build-plantillas.sh. No editar a mano."
  echo "// Se regenera desde formatos/<banco>/*.xlsx. Corre './build-plantillas.sh' cuando cambien."
  echo ""
  echo "window.PLANTILLAS = {"
} > "$OUT"

for dir in formatos/*/; do
  banco=$(basename "$dir")
  xlsx=$(find "$dir" -maxdepth 1 -name "*.xlsx" | head -1)
  if [ -z "$xlsx" ]; then
    echo "  aviso: no hay .xlsx en $dir, se omite" >&2
    continue
  fi
  filename=$(basename "$xlsx")
  b64=$(base64 -i "$xlsx" | tr -d '\n')
  {
    echo "  \"$banco\": {"
    echo "    filename: \"$filename\","
    echo "    base64: \"$b64\""
    echo "  },"
  } >> "$OUT"
  echo "  ok: $banco -> $filename"
done

echo "};" >> "$OUT"

size=$(wc -c < "$OUT" | tr -d ' ')
echo "listo: $OUT ($size bytes)"
