# Spec 002: Tema visual "metal" (fondo negro, detalles amarillos, tipografía metal)

## Estado
Implementada — cerrada. Ver [[#Adenda: tipografía gym y fondo con vectores]] para el ajuste posterior.

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

## Adenda: tipografía gym y fondo con vectores

### Motivación
El usuario pidió la tipografía "BaBaku Gym" (dafont.com) para reforzar la identidad de gimnasio, y vectores de fondo tipo pesas/máquinas en tonos amarillos.

### Decisión de tipografía
No se usa "BaBaku Gym": es un archivo de fuente de un sitio de terceros con licencia por-fuente no verificada (típicamente "solo uso personal"), y commitearlo al repo público implicaría redistribuir un archivo con copyright ajeno sin licencia confirmada. En su lugar se usa **Anton** (Google Fonts, licencia SIL Open Font License, embebible libremente), una fuente sans condensada/bold de estética muy usada en branding deportivo/gym. Reemplaza a "Metal Mania" como `--font-gym` (antes `--font-metal`) para `h1`, `h2` y `.brand`.

Si en el futuro se quiere usar específicamente "BaBaku Gym" u otra fuente de dafont: el usuario debe descargar el archivo verificando que la licencia permita el uso previsto, colocarlo en el proyecto, y desde ahí se conecta vía `@font-face` — no se descarga/commitea automáticamente por licencia desconocida.

### Decisión de vectores de fondo
No se usan vectores de bancos de imágenes (Freepik y similares) por la misma razón de licencia de redistribución. En su lugar se dibuja un ícono SVG propio de una barra con discos (barbell), embebido inline como `data:image/svg+xml` en `body::before`, repetido en mosaico a baja opacidad (`0.05`) en color acento (`#f5c400`), como capa de fondo (`z-index: -1`, `pointer-events: none`) detrás de todo el contenido.

### Requisitos no funcionales (adenda)
1. La opacidad del patrón de fondo debe ser suficientemente baja para no afectar el contraste WCAG AA del texto sobre fondo (los contenedores con fondo sólido —tarjetas, tablas— cubren el patrón; solo es visible sobre el negro base).
2. El patrón de fondo no debe interferir con la interacción (clicks, foco de inputs): `pointer-events: none`.
3. Igual que la fuente metal original, si Google Fonts no carga, el fallback (`"Impact", "Arial Narrow", sans-serif`) mantiene el look bold/condensado.

### Criterios de aceptación (adenda)
- Los títulos (`h1`, `h2`) y el nombre de marca se ven en la tipografía Anton (bold condensada), no en Metal Mania.
- El fondo negro de la app muestra un patrón sutil y repetido de barras con discos en amarillo, visible pero sin interferir con la lectura del contenido.
- Las tarjetas y tablas (con fondo sólido `--card`) no muestran el patrón por encima del texto.
