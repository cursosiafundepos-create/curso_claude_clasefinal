# Spec 003: Gráficos de progreso, comidas y suscripciones

## Estado
Implementada — cerrada.

## Resumen
Se agregan tres áreas nuevas a la app de gimnasio ([[001-rutinas-gimnasio-semanales]]):

1. **Gráficos de progreso**: visualización de la evolución del peso/series/repeticiones levantados por ejercicio a lo largo del tiempo, a partir de un nuevo registro histórico de entrenamientos (distinto de la rutina semanal fija, que es una plantilla sin fechas).
2. **Comidas**: registro nutricional (calorías y macronutrientes) por comida y fecha.
3. **Suscripciones**: planes de la app (free/premium) que habilitan o restringen funciones, sin procesamiento de pagos real.

## Motivación
El usuario quiere pasar de una app que solo define la rutina semanal a una que también permite ver progreso real de entrenamiento, llevar control nutricional, y tener una noción de planes/funciones premium dentro de la app.

## Alcance

### Incluido
- Registrar una sesión de entrenamiento real (fecha, ejercicio, peso, series, repeticiones) — el "log" histórico, separado de la plantilla de rutina de [[001-rutinas-gimnasio-semanales]].
- Ver un gráfico de evolución (peso y/o repeticiones a lo largo del tiempo) para un ejercicio dado, a partir del historial registrado.
- Registrar comidas: nombre, fecha, tipo (desayuno/almuerzo/cena/snack), calorías, proteínas, carbohidratos, grasas.
- Consultar comidas de un día y ver el total de calorías/macros del día.
- Crear, editar y eliminar comidas.
- Sección de suscripciones: mostrar el plan actual de la app (free o premium) y permitir cambiarlo manualmente (sin pago real, es un toggle/simulación).
- El plan premium habilita el gráfico de progreso de ejercicios (ver criterios de aceptación); el plan free no lo muestra.

### Fuera de alcance
- Procesamiento de pagos real, pasarela de pago, facturación.
- Multi-usuario / autenticación (sigue siendo una app de un solo usuario, como en [[001-rutinas-gimnasio-semanales]]); el "plan" es una configuración global de la instancia, no por usuario.
- Recomendaciones automáticas de dieta o de progresión de cargas.
- Búsqueda de alimentos en una base de datos externa (las calorías/macros se cargan a mano).
- Edición retroactiva masiva del historial de entrenamientos (import/export).

## Entidades (modelo de datos)

### RegistroEntrenamiento (nuevo)
- `fecha`: fecha, obligatoria.
- `dia`: enum `{lunes, martes, miercoles, jueves, viernes, sabado, domingo}` (a diferencia de la rutina plantilla, un registro real puede ocurrir cualquier día).
- `ejercicio`: texto, obligatorio (nombre del ejercicio, no necesita existir en la rutina plantilla).
- `peso`: opcional (texto o número, igual que en `Ejercicio` de [[001-rutinas-gimnasio-semanales]]).
- `series`: entero positivo, obligatorio.
- `repeticiones`: entero positivo, obligatorio.

### Comida (nuevo)
- `fecha`: fecha, obligatoria.
- `tipo`: enum `{desayuno, almuerzo, cena, snack}`, obligatorio.
- `nombre`: texto, obligatorio.
- `calorias`: entero ≥ 0, obligatorio.
- `proteinas_g`: número ≥ 0, opcional.
- `carbohidratos_g`: número ≥ 0, opcional.
- `grasas_g`: número ≥ 0, opcional.

### Suscripcion (nuevo)
- `plan`: enum `{free, premium}`, obligatorio. Configuración única y global de la app (no hay lista de suscripciones, es el estado actual).
- `fecha_cambio`: fecha del último cambio de plan.

## Requisitos funcionales

### Gráficos de progreso
1. El sistema debe permitir agregar un registro de entrenamiento (fecha, ejercicio, peso, series, repeticiones).
2. El sistema debe permitir listar el historial de registros de un ejercicio dado, ordenado por fecha.
3. El sistema debe permitir ver un gráfico de la evolución del peso (y opcionalmente repeticiones) de un ejercicio a lo largo del tiempo.
4. Si un ejercicio no tiene registros históricos, el gráfico debe mostrarse vacío con un mensaje ("sin datos"), no como error.
5. El gráfico de progreso solo está disponible si el plan actual es `premium`; con plan `free` la sección debe indicar que requiere upgrade, sin mostrar el gráfico.

### Comidas
6. El sistema debe permitir agregar, editar y eliminar una comida.
7. El sistema debe permitir consultar las comidas cargadas para una fecha específica.
8. El sistema debe calcular y mostrar el total de calorías y macros (proteínas, carbohidratos, grasas) de las comidas de un día.
9. Un día sin comidas cargadas debe mostrarse como "sin comidas registradas", no como error.

### Suscripciones
10. El sistema debe mostrar el plan actual (`free` o `premium`).
11. El sistema debe permitir cambiar el plan actual entre `free` y `premium` (sin pago real).
12. Al cambiar de plan, las funciones restringidas (gráfico de progreso) deben habilitarse/deshabilitarse inmediatamente según el nuevo plan.

## Requisitos no funcionales
- Persistencia en archivos JSON locales, siguiendo el mismo criterio que [[001-rutinas-gimnasio-semanales]] (sin base de datos): un archivo para historial de entrenamientos, uno para comidas, uno para el estado de la suscripción.
- Arquitectura MVC (ver `CLAUDE.md`): nuevos models para `RegistroEntrenamiento`, `Comida` y `Suscripcion`; controllers con las rutas correspondientes; views para las nuevas secciones (navegación agregada al layout existente).
- El gráfico de progreso se renderiza en el navegador (client-side), sin dependencias pesadas de backend para graficar.
- No se requiere migrar ni tocar los datos existentes de rutinas semanales ([[001-rutinas-gimnasio-semanales]]); son features independientes que conviven en la misma app.

## Criterios de aceptación
- Dado que se registran 3 sesiones de "sentadilla" en fechas distintas con pesos crecientes, cuando se consulta el gráfico de progreso de "sentadilla" en plan premium, entonces se ve una línea ascendente con los 3 puntos.
- Dado un ejercicio sin registros históricos, cuando se consulta su gráfico, entonces se muestra "sin datos" en vez de un error o gráfico roto.
- Dado el plan actual `free`, cuando se intenta ver el gráfico de progreso, entonces se muestra un mensaje pidiendo upgrade a premium, sin mostrar el gráfico.
- Dado que se cambia el plan de `free` a `premium`, cuando se vuelve a entrar a la sección de gráficos, entonces el gráfico se muestra normalmente.
- Dado que se cargan 2 comidas para el día de hoy (300 y 500 calorías), cuando se consulta el resumen del día, entonces el total mostrado es 800 calorías.
- Dado que se elimina una comida cargada, cuando se vuelve a consultar el día, entonces esa comida ya no aparece y el total se recalcula.
