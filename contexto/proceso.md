# Proceso end to end

## 1. Encargo

El cliente (banco o particular) solicita la tasación de un inmueble. La empresa asigna un tasador.

## 2. Visita e informe borrador

El tasador visita el inmueble y produce:

- Fotos del inmueble
- Partidas arancelarias (adjuntas)
- PU o predio urbano (adjunto)
- Borrador con la valuación y observaciones
- Posiblemente otros documentos: título de propiedad, minuta, planos, etc.

## 3. Envío a la digitadora

El tasador entrega el paquete de documentos a una digitadora, junto con la instrucción de qué formato de cliente usar (BCP, BBVA, Interbank, Scotiabank o particular).

## 4. Digitación

La digitadora:

1. Sube todos los documentos a `web/index.html`.
2. Selecciona el banco.
3. Descarga el paquete y lo coloca en `entregas/`.
4. Corre el skill `digitador` en Claude Code.
5. Revisa el output, ajusta si hace falta.
6. Entrega el informe final al cliente.

## 5. Control de calidad

_Definir._ Idealmente hay una segunda persona que revisa antes de enviar al banco.
