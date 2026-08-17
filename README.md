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
4. Click en **Preparar paquete**. Se descarga un ZIP.
5. Descomprime el ZIP dentro de la carpeta `entregas/` de este proyecto.
6. Abre Claude Code en la raíz del proyecto y escribe:
   `digitar el trabajo <nombre-del-trabajo>`
7. El skill lee los archivos, lee el formato del banco elegido, y genera el informe final dentro de la misma carpeta del trabajo.

## Requisitos

- Claude Code instalado ([claude.com/claude-code](https://claude.com/claude-code)).
- Navegador moderno (Chrome, Edge, Safari, Firefox) para abrir `web/index.html`.
- Las plantillas oficiales de cada banco colocadas dentro de `formatos/<banco>/`.

## Estado

- [x] Estructura de carpetas
- [x] Skill `digitador` (SKILL.md)
- [x] Interfaz HTML
- [x] Plantillas oficiales de los 5 bancos en `formatos/`
- [ ] Contexto y glosario completos
- [ ] Guías por banco (`formatos/<banco>/guia.md`) con reglas específicas
