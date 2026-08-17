# formatos/

Plantillas oficiales de cada cliente. El skill `digitador` las lee antes de generar cualquier informe.

## Estructura por banco

Cada carpeta contiene:

- La plantilla oficial en `.xlsx` (todas las actuales son Excel).
- `README.md` con las particularidades del formato: hojas obligatorias, celdas con fórmulas, formato de valores, etc.
- `versiones-anteriores/` (opcional) para archivar plantillas viejas.

## Bancos

- `banbif/`
- `bcp/`
- `interbank/`
- `scotiabank/`
- `particular/`

## Convención

El skill busca cualquier archivo `.xlsx` en la carpeta del banco. Mantén sólo la versión vigente en la raíz de la carpeta y mueve las anteriores a `versiones-anteriores/` cuando se actualicen. El nombre del archivo suele indicar el tipo de inmueble (DEPARTAMENTO, CASA, INMUEBLE); ese dato es relevante y no debe perderse al renombrar.
