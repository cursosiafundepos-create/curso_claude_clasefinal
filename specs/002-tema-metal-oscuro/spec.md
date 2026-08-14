# Spec 002: Tema visual "metal" (fondo negro, detalles amarillos, tipografía metal)

## Estado
Implementada — cerrada.

## Resumen
Reemplazar la apariencia visual actual de la app de rutinas de gimnasio ([[001-rutinas-gimnasio-semanales]]) por un tema oscuro estilo "metal": fondo negro, detalles/acentos en amarillo, y tipografía con look de banda de heavy metal para los títulos.

Es un cambio puramente visual (CSS + tipografía). No modifica modelos, controllers, ni la estructura de datos de las rutinas.

## Motivación
El usuario quiere que la app tenga una identidad visual más agresiva/"metal", en vez del tema claro genérico actual.

## Alcance

### Incluido
- Fondo negro en toda la aplicación (header, contenido, tarjetas).
- Acentos en amarillo: enlaces, botones, bordes destacados, hover states, título de marca.
- Tipografía "metal" para títulos (h1/h2, nombre de la marca en el header): fuente tipo banda de heavy metal (afilada/distressed).
- Tipografía de cuerpo (texto normal, inputs, tablas) que siga siendo legible — no se aplica el estilo metal a bloques largos de texto.
- Aplica a las tres vistas existentes: semana, día, y formularios.

### Fuera de alcance
- Cambios de layout/estructura HTML más allá de lo necesario para el nuevo estilo.
- Modo claro / toggle de tema (queda solo el tema oscuro).
- Animaciones o efectos más allá de estados hover/focus básicos.

## Decisiones
- **Paleta**: fondo `#0a0a0a` (negro), tarjetas/superficies `#161616`, texto principal blanco hueso `#f2f2f2`, acento amarillo `#f5c400`, bordes `#2a2a2a`.
- **Tipografía de títulos**: fuente "Metal Mania" (Google Fonts) — estilo afilado/manuscrito de banda de metal — para el nombre de marca en el header y los `h1`/`h2`.
- **Tipografía de cuerpo**: se mantiene una fuente de sistema legible (`system-ui`) para texto de tablas, inputs y párrafos, para no sacrificar legibilidad/usabilidad.
- Los estados de error/peligro (botón eliminar) mantienen un rojo suficientemente distinguible del amarillo de acento.

## Requisitos funcionales
No aplica (spec puramente visual, sin cambios de comportamiento).

## Requisitos no funcionales
1. El contraste texto/fondo debe cumplir como mínimo WCAG AA para texto normal (blanco hueso sobre negro y negro sobre amarillo en botones).
2. La tipografía metal se carga vía Google Fonts; si la fuente no carga (sin conexión), debe haber un fallback razonable (`serif` o `cursive` del sistema) para que los títulos no queden invisibles ni rotos.
3. El cambio se implementa en `src/gimnasio_rutinas/views/static/style.css` (y `base.html` para el `<link>` de la fuente); no requiere tocar `models/` ni `controllers/`.

## Criterios de aceptación
- Al abrir `/semana`, el fondo es negro y el nombre de marca del header se ve en la tipografía metal, en amarillo.
- Los botones de acción (Agregar, Guardar) tienen el acento amarillo definido; el botón eliminar sigue siendo distinguible en rojo.
- El texto de las tablas de ejercicios (inputs, notas) sigue siendo legible en fuente de sistema, no en la fuente metal.
- La app sigue siendo completamente funcional (agregar/editar/mover/eliminar ejercicios) — este cambio no altera ningún comportamiento, solo estilos.
