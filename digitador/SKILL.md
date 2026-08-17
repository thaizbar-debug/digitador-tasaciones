---
name: digitador
description: Transcribe informes de tasación inmobiliaria peruana al formato oficial del cliente. Toma la documentación que el tasador envió a la digitadora (fotos del inmueble, partidas arancelarias, PU o predios urbanos, borrador del tasador, otros anexos) y produce el informe final en el formato de Banbif, BCP (Cibergestión), Interbank (MiVivienda), Scotiabank o particular. Actívalo cuando el usuario diga "digitar", "digitar tasación", "digitar trabajo", "transcribir informe de tasación", "generar informe de tasación", o cuando mencione que tiene una carpeta de trabajo en entregas/ lista para procesar.
---

# Skill: digitador

Este skill toma un paquete de documentos de tasación y lo transcribe al formato final que exige el cliente (banco o particular). Está diseñado para el flujo interno de una empresa peruana de tasaciones.

## Cuándo activarte

Cuando el usuario:

- Diga "digitar el trabajo `<nombre>`" o "digitar `<nombre>` para `<banco>`".
- Mencione que descargó un ZIP de la interfaz web y lo extrajo en `entregas/`.
- Pida transcribir un informe de tasación al formato de un banco.

## Entradas que vas a encontrar

Dentro de `entregas/<nombre-del-trabajo>/` va a haber:

- `manifest.json` con el banco elegido y el nombre del trabajo.
- `inputs/fotos/` con las imágenes del inmueble.
- `inputs/partidas-arancelarias/` con documentos SUNAT o municipales.
- `inputs/pu/` con el o los predios urbanos.
- `inputs/borrador/` con el borrador del tasador (fuente principal de contenido).
- `inputs/otros/` (opcional) con documentos adicionales.

## Paso a paso

### 1. Lee el manifest

Empieza leyendo `entregas/<trabajo>/manifest.json`. De ahí sacas:

- `banco`: uno de `banbif`, `bcp`, `interbank`, `scotiabank`, `particular`.
- `jobName`: el identificador del trabajo.
- `notas`: instrucciones opcionales de la digitadora.

Si el manifest no existe, pídele a la digitadora que confirme el banco y el nombre del trabajo antes de continuar.

### 2. Lee el contexto de dominio

Antes de mirar los inputs, lee:

- `contexto/glosario.md`
- `contexto/proceso.md`
- Cualquier otro archivo en `contexto/`

Esto te da vocabulario y reglas implícitas del equipo.

### 3. Lee la plantilla oficial del banco

Ve a `formatos/<banco>/` y toma el archivo `.xlsx` que esté ahí (es único por banco). También lee el `README.md` de esa carpeta si existe. Si no hay ningún `.xlsx`, detén el proceso y avísale a la digitadora.

Para leer y escribir Excel usa `openpyxl` en Python. Respeta las fórmulas: no las sobrescribas con valores; escribe sólo en las celdas de entrada.

### 4. Lee todos los inputs del trabajo

- Extrae texto de PDFs (por ejemplo con `pdftotext` o similar).
- Para las fotos, mira cada imagen y describe brevemente qué se ve (fachada, sala, baño, vista exterior, etc.) para poder rotularlas.
- El borrador del tasador es la fuente principal de contenido. **Importante**: el borrador muchas veces viene en un Excel con estructura parecida a la plantilla oficial del banco (mismas hojas), pero con hojas auxiliares extra y datos aún por verificar. Trátalo como **fuente de datos**, no como base del output.
- Las partidas y el PU son fuentes de datos catastrales y valores oficiales. Cruza la información: si el borrador dice X área y el PU dice Y área, señálalo como discrepancia en vez de elegir uno.

### 5. Genera el informe final

El output es **una copia de la plantilla oficial del banco, rellenada con los datos del trabajo**. La estructura, las hojas, las fórmulas y el formato deben ser exactamente los de la plantilla; el borrador solo aporta los datos.

Pasos:

1. Copia `formatos/<banco>/<plantilla>.xlsx` a `entregas/<trabajo>/output/informe-<trabajo>-<banco>.xlsx`. Nunca edites el archivo original.
2. Rellena las celdas de entrada de la copia con datos del borrador, PU y partidas.
3. Cuando el borrador tenga la misma estructura de hojas que la plantilla, puedes mapear celda a celda hoja por hoja para acelerar; pero verifica cada valor antes de escribirlo y **nunca copies fórmulas del borrador sobre celdas de la plantilla que tengan sus propias fórmulas**.
4. Ignora hojas auxiliares del borrador que no existan en la plantilla oficial (por ejemplo `C2`, `Hoja4`).

Incluye también:

- `entregas/<trabajo>/output/anexo-fotografico.md` con las fotos rotuladas y organizadas por ambiente. Las fotos originales quedan en `inputs/fotos/`; la digitadora las pegará al Excel manualmente en la hoja `FOTO` (o equivalente) si el formato lo requiere.
- `entregas/<trabajo>/output/revisar.md` con un checklist de campos que la digitadora debe verificar manualmente: todo lo que inferiste, todo campo que quedó vacío, toda discrepancia entre fuentes, cualquier celda que dejaste con `[FALTA:]`.

## Reglas duras

1. **Nunca inventes datos.** Si un campo obligatorio no está en las fuentes, déjalo como `[FALTA: descripción del dato]` y agrégalo a `revisar.md`. No adivines valores comerciales, áreas, linderos, ni fechas.
2. **Nunca cambies un número.** Copia los valores tal como aparecen en el borrador o el PU. Si detectas una discrepancia entre dos fuentes, repórtala en `revisar.md`, no elijas por tu cuenta.
3. **Respeta el formato del banco.** Si la guía dice que el valor comercial va en soles con dos decimales y el borrador lo tiene en dólares, convierte usando el tipo de cambio que indique el borrador. Si no lo indica, marca como `[FALTA: tipo de cambio]`.
4. **Fotos.** Rotula cada foto con lo que veas y en qué ambiente estimas que fue tomada. Marca como `[REVISAR ROTULADO]` para que la digitadora confirme.
5. **Nunca uses guiones ni em dashes como separadores en el texto del informe.** Usa punto y seguido, coma, o dos puntos.
6. **Español peruano.** Redacción formal, tercera persona, terminología del sector inmobiliario y bancario peruano.

## Salida esperada

Al terminar, dile a la digitadora:

- Dónde quedó el informe (`entregas/<trabajo>/output/`).
- Cuántos campos quedaron marcados como `[FALTA:]` o `[REVISAR]`.
- Cualquier discrepancia importante entre fuentes.
- Recordatorio de revisar `revisar.md` antes de enviar al banco.

## Si algo falta

- Falta plantilla del banco: pide que la carguen como `.xlsx` en `formatos/<banco>/`.
- Falta borrador del tasador: no se puede continuar. Pide que lo agreguen a `inputs/borrador/`.
- Manifest ausente: pregunta el banco y el nombre del trabajo.
- Documento ilegible: reporta cuál y pide una versión mejor escaneada.
