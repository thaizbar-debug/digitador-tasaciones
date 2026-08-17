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
├── server/            Server local Python (Flask + openpyxl) que hace el merge
├── web/               Interfaz HTML que usan las digitadoras
├── digitador/         Skill de Claude Code (opcional, para uso asistido por IA)
├── entregas/          Trabajos en curso (no se sube a git; contiene datos sensibles)
├── abrir.command      Doble click para arrancar el server y abrir el navegador
└── .claude/skills/    Enlace simbólico que expone el skill a Claude Code
```

## Cómo se usa (flujo de la digitadora)

1. **Doble click a `abrir.command`** en la raíz del proyecto. La primera vez tarda ~1 minuto instalando dependencias en un entorno virtual local. Después arranca instantáneo. Se abre el navegador en `http://localhost:5555/`.
2. Escribe el nombre del trabajo (ej. `2026-08-17-lopez-miraflores`) y elige el banco.
3. Arrastra o selecciona los archivos que envió el tasador:
   - Fotos del inmueble
   - Partidas arancelarias
   - PU (predios urbanos)
   - Borrador del tasador
   - Otros (opcional)
4. Click en **Generar informe**. El server local carga la plantilla oficial del banco (preservando logos, colores, imágenes y fórmulas), transfiere los datos del borrador celda por celda, inserta las fotos en la hoja FOTO, y devuelve un ZIP con:
   - `informe-<trabajo>-<banco>.xlsx`, la plantilla oficial rellenada con todo el look del banco.
   - `revisar.md`, checklist manual antes de enviar (dónde reubicar las fotos, cruzar con PU, campos del banco, etc.).
   - `anexo-fotografico.md`, listado de fotos con rotulado sugerido.
   - `manifest.json` con metadata del trabajo y estadísticas del merge.
5. Descomprime el ZIP, abre el Excel, reubica las fotos al layout oficial del banco (fueron insertadas al final de la hoja FOTO) y revisa el `revisar.md` antes de enviar al banco.

Todo el procesamiento ocurre en tu Mac. No se sube nada a servidores externos.

Para cerrar el server, cierra la ventana de Terminal que abrió `abrir.command`.

## Requisitos

- macOS con Python 3 (viene por default; para verificar, correr `python3 --version` en Terminal).
- Navegador moderno (Chrome, Edge, Safari, Firefox).
- Las plantillas oficiales de cada banco colocadas dentro de `formatos/<banco>/` (ya cargadas).
- (Opcional) Claude Code, si quieres correr el skill `digitador` para procesamiento asistido por IA.

## Actualizar plantillas

Si un banco actualiza su plantilla, reemplaza el `.xlsx` en `formatos/<banco>/` y listo. El server la lee directamente cada vez.

## Estado

- [x] Estructura de carpetas
- [x] Interfaz HTML con merge automático (SheetJS)
- [x] Plantillas oficiales de los 5 bancos en `formatos/` y embebidas en `web/plantillas.js`
- [x] Skill `digitador` (SKILL.md) para procesamiento asistido por IA (opcional)
- [ ] Contexto y glosario completos
- [ ] Guías por banco con reglas específicas del formato
