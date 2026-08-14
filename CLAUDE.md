# curso_claude_clasefinal

## Metodología: Spec-Driven Development

Todo el trabajo de este proyecto se organiza a partir de especificaciones, no de código escrito de forma ad-hoc.

- Cada nueva especificación se guarda en `specs/`, en su propia carpeta numerada: `specs/NNN-nombre-corto/spec.md` (ej. `specs/001-rutinas-gimnasio-semanales/spec.md`).
- Cada especificación se desarrolla en su propia rama, creada desde `main`, con el mismo nombre que la carpeta (`NNN-nombre-corto`).
- El código se implementa después de que la especificación esté escrita, siguiendo lo que ella define.

## Arquitectura de código: MVC

El código de la aplicación sigue el patrón Modelo-Vista-Controlador:

- **Models**: entidades y acceso/persistencia de datos.
- **Views**: presentación / salida al usuario.
- **Controllers**: lógica de aplicación que conecta modelos y vistas.

## Gestión de librerías: uv

Las dependencias de Python se gestionan con [uv](https://github.com/astral-sh/uv) (no pip/poetry directamente):

- `uv init` para inicializar el proyecto.
- `uv add <paquete>` para agregar dependencias.
- `uv run <comando>` para ejecutar scripts dentro del entorno gestionado.
