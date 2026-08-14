# Spec 001: Rutinas de gimnasio semanales (lunes a viernes)

## Estado
Implementada — cerrada.

## Resumen
Aplicación de gimnasio que permite cargar y consultar, día por día, la rutina de ejercicios correspondiente. Solo existen rutinas para los días hábiles: **lunes, martes, miércoles, jueves y viernes**. Sábado y domingo no tienen rutina (días de descanso, fuera del alcance de la app).

El usuario irá programando las rutinas de forma incremental: hoy puede cargar solo la del lunes, y en sesiones futuras ir agregando o modificando las de los demás días.

## Motivación
El usuario quiere un lugar único donde definir qué ejercicios hace cada día de la semana laboral, para poder consultarlo y modificarlo a medida que ajusta su plan de entrenamiento.

## Alcance

### Incluido
- Definir una rutina para cada uno de los 5 días: lunes, martes, miércoles, jueves, viernes.
- Una rutina está compuesta por una lista ordenada de ejercicios.
- Cada ejercicio tiene, como mínimo: nombre, series, repeticiones. Opcionalmente: peso/carga y notas.
- Consultar la rutina de un día específico.
- Consultar todas las rutinas de la semana.
- Crear, editar y eliminar ejercicios dentro de la rutina de un día.
- Un día puede no tener rutina cargada todavía (se admite carga incremental).

### Fuera de alcance (por ahora)
- Sábado y domingo (no se modelan como días con rutina).
- Registro histórico de entrenamientos realizados (tracking de progreso, pesos levantados en cada sesión real).
- Múltiples usuarios / autenticación.
- Múltiples rutinas alternativas por día (solo una rutina activa por día).

## Entidades (modelo de datos)

### Día
- `dia`: enum restringido a `{lunes, martes, miercoles, jueves, viernes}`.
- `ejercicios`: lista ordenada de `Ejercicio`.

### Ejercicio
- `nombre`: texto, obligatorio.
- `series`: entero positivo, obligatorio.
- `repeticiones`: entero positivo (o rango, ej. "8-12"), obligatorio.
- `peso`: opcional (texto o número, para admitir "corporal", "20kg", etc.).
- `notas`: texto libre, opcional.
- `orden`: posición del ejercicio dentro de la rutina del día.

## Requisitos funcionales
1. El sistema debe rechazar la creación de rutinas para días que no sean lunes–viernes.
2. El sistema debe permitir agregar un ejercicio a la rutina de un día.
3. El sistema debe permitir editar los campos de un ejercicio existente.
4. El sistema debe permitir eliminar un ejercicio de la rutina de un día.
5. El sistema debe permitir reordenar los ejercicios dentro de un día.
6. El sistema debe permitir consultar la rutina completa de un día puntual.
7. El sistema debe permitir consultar la semana completa (los 5 días) en una sola vista.
8. Un día sin ejercicios cargados debe mostrarse como "sin rutina definida", no como error.

## Requisitos no funcionales
- Persistencia en archivo local JSON (un archivo con las 5 claves de día, cada una con su lista de ejercicios; los días sin rutina se guardan como lista vacía). Sin base de datos.
- La interfaz web debe dejar claro en todo momento a qué día corresponde la información mostrada.
- La aplicación se implementa con arquitectura MVC (ver `CLAUDE.md`): controllers exponen las rutas web, models representan Día/Ejercicio y su persistencia, views renderizan el HTML.

## Decisiones
- **Interfaz: Web.** La aplicación se implementa como interfaz web (no CLI). El servidor expone las rutinas y permite gestionarlas (alta/edición/borrado de ejercicios) a través del navegador.
- **Rutina semanal fija, sin duplicado.** Cada día de la semana (lunes–viernes) tiene una única rutina, sin fechas asociadas: la misma rutina se repite semana tras semana hasta que se edite. No se necesita función de duplicar/plantilla entre días — el modelo de datos ya definido (Día → lista de Ejercicios) cubre este caso.
- **Persistencia: JSON local.** Se elige JSON (no YAML) por ser nativo de Python (módulo estándar `json`, sin dependencia adicional que agregar con uv) y por mapear 1:1 con el modelo de datos (Día → lista de Ejercicios).

## Criterios de aceptación
- Dado que no existe rutina para el lunes, cuando se agrega un ejercicio al lunes, entonces la rutina del lunes queda creada con ese ejercicio.
- Dado un ejercicio cargado en martes, cuando se edita su número de series, entonces la consulta de la rutina del martes refleja el nuevo valor.
- Dado que se intenta crear una rutina para "sábado", entonces el sistema la rechaza.
- Dado que ningún día tiene rutina cargada, cuando se consulta la semana completa, entonces los 5 días aparecen listados como "sin rutina definida".
