# formatos/

Plantillas oficiales de cada cliente. El skill `digitador` las lee antes de generar cualquier informe.

## Estructura por banco

Cada carpeta debe contener:

- La plantilla original tal como la exige el banco (`.docx`, `.pdf`, o `.xlsx`).
- `guia.md` con notas específicas del formato: campos obligatorios, redacción esperada, unidades, orden de secciones, etc.
- `ejemplo.md` (opcional) con un informe completo ya digitado en ese formato, útil como referencia.

## Bancos

- `bcp/`
- `bbva/`
- `interbank/`
- `scotiabank/`
- `particular/`

## Convención de nombres

Nombra el archivo de plantilla como `plantilla.docx` (o `.pdf`, `.xlsx`) para que el skill lo encuentre sin ambigüedad. Si tienes varias versiones, mantén sólo la vigente en la raíz y mueve las viejas a `versiones-anteriores/`.
