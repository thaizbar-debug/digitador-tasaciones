# digitador-tasaciones

Herramienta interna para las digitadoras de una empresa peruana de tasaciones. Convierte la documentación que envían los tasadores (fotos, partidas arancelarias, PU, borrador) en el informe final con el formato del banco cliente.

## Bancos soportados

1. Banbif
2. BCP (Cibergestión)
3. Interbank (incluye MiVivienda)
4. Scotiabank
5. Particular

## Estructura del proyecto

```
digitador-tasaciones/
├── contexto/          Glosario, proceso, notas de dominio
├── formatos/          Plantillas oficiales de cada banco (una carpeta por banco)
├── digitador/         El skill de Claude Code (SKILL.md)
├── web/               Interfaz HTML que usan las digitadoras para subir información
├── entregas/          Carpeta de trabajos en curso y terminados (no se sube a git)
└── .claude/skills/    Enlace simbólico que expone el skill a Claude Code
```

## Cómo se usa (flujo de la digitadora)

1. Abre `web/index.html` en tu navegador (doble click al archivo).
2. Escribe el nombre del trabajo (ej. `2026-08-17-lopez-miraflores`) y elige el banco.
3. Arrastra o selecciona los archivos que envió el tasador:
   - Fotos del inmueble
   - Partidas arancelarias
   - PU (predios urbanos)
   - Borrador del tasador
   - Otros (opcional)
4. Click en **Generar informe**. La página carga la plantilla oficial del banco, transfiere los datos del borrador celda por celda respetando las fórmulas oficiales, y descarga un ZIP con:
   - `inputs/` con toda la documentación original ordenada.
   - `output/informe-<trabajo>-<banco>.xlsx`, la plantilla oficial ya rellenada.
   - `output/revisar.md`, checklist manual antes de enviar (fotos por pegar, cruzar con PU, campos del banco, etc.).
   - `output/anexo-fotografico.md`, listado de las fotos con rotulado sugerido.
   - `manifest.json` con metadata del trabajo y estadísticas del merge.
5. Descomprime el ZIP donde quieras (por ejemplo dentro de `entregas/`), abre el Excel, pega las fotos manualmente en la hoja `FOTO` y revisa el `revisar.md` antes de enviar al banco.

Todo el procesamiento ocurre en tu navegador. No se sube nada a servidores externos.

## Requisitos

- Navegador moderno (Chrome, Edge, Safari, Firefox) para abrir `web/index.html`.
- Las plantillas oficiales de cada banco colocadas dentro de `formatos/<banco>/` (ya cargadas).
- (Opcional) Claude Code, si quieres correr el skill `digitador` para procesamiento asistido por IA.

## Actualizar plantillas

Si un banco actualiza su plantilla, reemplaza el `.xlsx` en `formatos/<banco>/` y luego corre:

```
./build-plantillas.sh
```

Esto regenera `web/plantillas.js` (donde el HTML tiene embebidas las plantillas en base64). Después haz commit del cambio.

## Estado

- [x] Estructura de carpetas
- [x] Interfaz HTML con merge automático (SheetJS)
- [x] Plantillas oficiales de los 5 bancos en `formatos/` y embebidas en `web/plantillas.js`
- [x] Skill `digitador` (SKILL.md) para procesamiento asistido por IA (opcional)
- [ ] Contexto y glosario completos
- [ ] Guías por banco con reglas específicas del formato
