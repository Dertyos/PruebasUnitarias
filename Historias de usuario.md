# [cite_start]HISTORIAS DE USUARIO Y CRITERIOS DE ACEPTACIÓN [cite: 1]
## [cite_start]PROJECT MANAGER v1.0 [cite: 2]
> [cite_start]Gestor de Proyectos y Tareas estilo Kanban [cite: 3]
> [cite_start]Noviembre 2025 - Versión 1.0 [cite: 3]

---

# [cite_start]SPRINT 1: INFRAESTRUCTURA Y GESTIÓN DE USUARIOS [cite: sprint1]
## [cite_start]Temas: Persistencia de Datos, Usuarios [cite: sprint1]

---

## [cite_start]HU-010: Persistencia de Datos [cite: 58]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-010 | 🔴 Crítica | Media |
[cite_start][cite: 59]

### [cite_start]Descripción [cite: 60]
> [cite_start]Como usuario, quiero que mis datos se guarden automáticamente para no perder información cuando reinicio la aplicación.El sistema debe persistir automáticamente todos los cambios en una base de datos JSON estructurada y validada. [cite: 61]

### [cite_start]Criterios de Aceptación [cite: 62]
1.  [cite_start]El sistema guarda automáticamente después de crear usuarios [cite: 63]
2.  [cite_start]El sistema guarda automáticamente después de crear proyectos [cite: 63]
3.  [cite_start]El sistema guarda automáticamente después de crear tareas [cite: 63]
4.  [cite_start]El sistema guarda automáticamente después de editar tareas [cite: 63]
5.  [cite_start]El sistema guarda automáticamente después de eliminar datos [cite: 63]
6.  [cite_start]Los datos se almacenan en formato JSON bien estructurado [cite: 63]
7.  [cite_start]Se crea automáticamente la carpeta data/ si no existe [cite: 63]
8.  [cite_start]Se crea automáticamente el archivo projects.json si no existe [cite: 63]
9.  [cite_start]Se valida la estructura JSON antes de guardar [cite: 63]
10. [cite_start]El usuario recupera automáticamente datos después de reiniciar [cite: 63]
11. [cite_start]Se pueden hacer respaldos fácilmente (copiar projects.json) [cite: 63]
12. [cite_start]El sistema se recupera elegantemente de archivos JSON corruptos [cite: 63]

---

## [cite_start]HU-001: Gestión de Usuarios [cite: 4]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-001 | 🔴 Crítica | Alta |
[cite_start][cite: 5]

### [cite_start]Descripción [cite: 6]
> [cite_start]Como usuario, quiero gestionar usuarios en el sistema para tener un registro de los miembros del equipo que participarán en los proyectos.El sistema debe permitir crear nuevos usuarios con validación de email, listar todos los usuarios registrados, seleccionar un usuario como usuario actual del sistema, y eliminar usuarios cuando sea necesario. [cite: 7]

### [cite_start]Criterios de Aceptación [cite: 8]
1.  [cite_start]El usuario puede crear un nuevo usuario ingresando nombre y email válido [cite: 9]
2.  [cite_start]El sistema valida que el email contenga un "@" y un "." [cite: 9]
3.  [cite_start]El usuario puede listar todos los usuarios registrados en el sistema [cite: 9]
4.  [cite_start]El sistema muestra nombre, email y marca el usuario actual con "✓" [cite: 9]
5.  [cite_start]El usuario puede seleccionar un usuario existente como usuario actual [cite: 9]
6.  [cite_start]El usuario puede eliminar un usuario existente con confirmación previa [cite: 9]
7.  [cite_start]El sistema valida que no existan usuarios duplicados por email [cite: 9]
8.  [cite_start]Cada usuario recibe un ID único (UUID) asignado automáticamente [cite: 9]
9.  [cite_start]El sistema guarda la fecha de creación de cada usuario [cite: 9]
10. [cite_start]Todos los cambios se persisten automáticamente en JSON [cite: 9]

---

# [cite_start]SPRINT 2: PROYECTOS Y COLUMNAS [cite: sprint2]
## [cite_start]Temas: Proyectos, Columnas [cite: sprint2]

---

## [cite_start]HU-002: Crear Proyecto [cite: 10]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-002 | 🔴 Crítica | Media |
[cite_start][cite: 11]

### [cite_start]Descripción [cite: 12]
> [cite_start]Como usuario, quiero crear nuevos proyectos para organizar mis tareas y establecer un flujo de trabajo personalizado.El sistema debe permitir crear proyectos con nombre obligatorio y descripción opcional, asignando automáticamente columnas preconfiguradas para el flujo Kanban. [cite: 13]

### [cite_start]Criterios de Aceptación [cite: 14]
1.  [cite_start]El usuario puede crear un nuevo proyecto especificando nombre y descripción [cite: 15]
2.  [cite_start]El nombre del proyecto es obligatorio, no puede estar vacío [cite: 15]
3.  [cite_start]Se asigna automáticamente un ID único (UUID) a cada proyecto [cite: 15]
4.  [cite_start]Se asigna automáticamente el usuario actual como propietario del proyecto [cite: 15]
5.  [cite_start]Se crean automáticamente tres columnas: Pendiente, En Progreso, Completada [cite: 15]
6.  [cite_start]El usuario puede abrir/seleccionar un proyecto existente [cite: 15]
7.  [cite_start]El usuario puede listar todos los proyectos con conteo de tareas [cite: 15]
8.  [cite_start]El usuario puede eliminar un proyecto con confirmación previa [cite: 15]
9.  [cite_start]Se guardan las fechas de creación y última modificación [cite: 15]
10. [cite_start]Todos los cambios se persisten automáticamente en JSON [cite: 15]

---

## [cite_start]HU-007: Gestionar Columnas [cite: 40]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-007 | 🟠 Alta | Media |
[cite_start][cite: 41]

### [cite_start]Descripción [cite: 42]
> [cite_start]Como usuario, quiero gestionar las columnas del proyecto para customizar mi flujo de trabajo según mis necesidades específicas.El sistema debe permitir agregar nuevas columnas, renombrar columnas existentes y eliminar columnas que ya no se necesitan. [cite: 43]

### [cite_start]Criterios de Aceptación [cite: 44]
1.  [cite_start]El usuario puede agregar una nueva columna especificando su nombre [cite: 45]
2.  [cite_start]El usuario puede ver la lista completa de columnas actuales [cite: 45]
3.  [cite_start]El usuario puede renombrar una columna existente [cite: 45]
4.  [cite_start]El usuario puede eliminar una columna con confirmación previa [cite: 45]
5.  [cite_start]Al eliminar una columna, se eliminan automáticamente todas sus tareas [cite: 45]
6.  [cite_start]El sistema advierte al usuario si una columna contiene tareas [cite: 45]
7.  [cite_start]Las columnas mantienen un orden específico (Kanban) [cite: 45]
8.  [cite_start]El nombre de la columna es campo obligatorio [cite: 45]
9.  [cite_start]El sistema evita crear columnas duplicadas [cite: 45]
10. [cite_start]El proyecto se guarda automáticamente después de cambios de columnas [cite: 45]

---

# [cite_start]SPRINT 3: GESTIÓN BÁSICA DE TAREAS [cite: sprint3]
## [cite_start]Temas: Tareas (Crear, Editar) [cite: sprint3]

---

## [cite_start]HU-003: Crear Tarea [cite: 16]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-003 | 🔴 Crítica | Media |
[cite_start][cite: 17]

### [cite_start]Descripción [cite: 18]
> [cite_start]Como usuario, quiero crear tareas en las columnas del proyecto para organizar el trabajo que necesita realizarse.El sistema debe permitir crear tareas con título obligatorio, descripción opcional, selección de prioridad, selección de columna destino, y asignación opcional a un usuario. [cite: 19]

### [cite_start]Criterios de Aceptación [cite: 20]
1.  [cite_start]El usuario puede crear una nueva tarea especificando título obligatorio [cite: 21]
2.  [cite_start]El título de la tarea es campo obligatorio, no puede estar vacío [cite: 21]
3.  [cite_start]El usuario puede especificar descripción (campo opcional) [cite: 21]
4.  [cite_start]El usuario puede seleccionar prioridad: Baja, Media, Alta, Urgente [cite: 21]
5.  [cite_start]La prioridad por defecto es "Media" cuando no se especifica [cite: 21]
6.  [cite_start]El usuario debe seleccionar la columna destino para la tarea [cite: 21]
7.  [cite_start]El usuario puede asignar la tarea a un usuario (campo opcional) [cite: 21]
8.  [cite_start]Cada tarea recibe un ID único (UUID) asignado automáticamente [cite: 21]
9.  [cite_start]El estado inicial de la tarea es "Pendiente" [cite: 21]
10. [cite_start]Se registran automáticamente fechas de creación y modificación [cite: 21]
11. [cite_start]El proyecto se guarda automáticamente después de crear la tarea [cite: 21]
12. [cite_start]El sistema muestra mensaje de confirmación cuando la tarea se crea [cite: 21]

---

## [cite_start]HU-004: Editar Tarea [cite: 22]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-004 | 🔴 Crítica | Alta |
[cite_start][cite: 23]

### [cite_start]Descripción [cite: 24]
> [cite_start]Como usuario, quiero editar tareas existentes para poder modificar sus detalles, estado, prioridad, asignación y otros atributos.El sistema debe permitir editar todos los atributos de una tarea después de su creación, incluyendo moverla entre columnas. [cite: 25]

### [cite_start]Criterios de Aceptación [cite: 26]
1.  [cite_start]El usuario puede cambiar el título de la tarea [cite: 27]
2.  [cite_start]El usuario puede cambiar la descripción de la tarea [cite: 27]
3.  [cite_start]El usuario puede cambiar la prioridad de la tarea [cite: 27]
4.  [cite_start]El usuario puede cambiar el estado entre: Pendiente, En Progreso, Completada, Bloqueada [cite: 27]
5.  [cite_start]El usuario puede cambiar el usuario asignado a la tarea [cite: 27]
6.  [cite_start]El usuario puede mover la tarea a otra columna del proyecto [cite: 27]
7.  [cite_start]El usuario puede agregar nuevas etiquetas a la tarea [cite: 27]
8.  [cite_start]El usuario puede eliminar etiquetas existentes de la tarea [cite: 27]
9.  [cite_start]El usuario puede ver todos los detalles completos de la tarea [cite: 27]
10. [cite_start]El usuario puede eliminar la tarea con confirmación previa [cite: 27]
11. [cite_start]Se actualiza automáticamente la fecha de modificación después de cada cambio [cite: 27]
12. [cite_start]El proyecto se guarda automáticamente después de cada edición [cite: 27]

---

# [cite_start]SPRINT 4: VISUALIZACIÓN Y BÚSQUEDA [cite: sprint4]
## [cite_start]Temas: Tablero Kanban, Búsqueda de Tareas [cite: sprint4]

---

## [cite_start]HU-005: Buscar Tarea [cite: 28]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-005 | 🟠 Alta | Media |
[cite_start][cite: 29]

### [cite_start]Descripción [cite: 30]
> [cite_start]Como usuario, quiero buscar tareas específicas para encontrar rápidamente el trabajo que necesito.El sistema debe permitir buscar tareas por título o descripción, retornando resultados relevantes con la opción de seleccionar una tarea para editarla. [cite: 31]

### [cite_start]Criterios de Aceptación [cite: 32]
1.  [cite_start]El usuario puede ingresar un término de búsqueda [cite: 33]
2.  [cite_start]El sistema busca en títulos de tareas (búsqueda parcial, no completa) [cite: 33]
3.  [cite_start]El sistema busca en descripciones de tareas (búsqueda parcial) [cite: 33]
4.  [cite_start]La búsqueda es insensible a mayúsculas y minúsculas [cite: 33]
5.  [cite_start]El sistema muestra el número total de tareas encontradas [cite: 33]
6.  [cite_start]El sistema muestra en qué columna está cada tarea encontrada [cite: 33]
7.  [cite_start]El usuario puede seleccionar una tarea de los resultados para editar [cite: 33]
8.  [cite_start]Se muestra un mensaje claro si no hay resultados de búsqueda [cite: 33]
9.  [cite_start]El término de búsqueda puede estar vacío (retorna todas las tareas) [cite: 33]
10. [cite_start]La búsqueda es eficiente incluso con muchas tareas en el proyecto [cite: 33]

---

## [cite_start]HU-006: Ver Tablero [cite: 34]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-006 | 🔴 Crítica | Media |
[cite_start][cite: 35]

### [cite_start]Descripción [cite: 36]
> [cite_start]Como usuario, quiero ver el tablero Kanban del proyecto para visualizar claramente el estado actual del trabajo.El sistema debe mostrar todas las columnas y tareas en un formato visual similar a Trello, con información clara de cada tarea. [cite: 37]

### [cite_start]Criterios de Aceptación [cite: 38]
1.  [cite_start]Se muestran todas las columnas del proyecto actual [cite: 39]
2.  [cite_start]Se muestran todas las tareas dentro de cada columna [cite: 39]
3.  [cite_start]Se muestra el título de cada tarea en el tablero [cite: 39]
4.  [cite_start]Se muestra el ID de la tarea (primeros 8 caracteres del UUID) [cite: 39]
5.  [cite_start]Se muestra el usuario asignado o "Sin asignar" [cite: 39]
6.  [cite_start]Se muestra icono de prioridad: 🔴 Urgente, 🟠 Alta, 🟡 Media, 🟢 Baja [cite: 39]
7.  [cite_start]Se muestra el conteo total de tareas en cada columna [cite: 39]
8.  [cite_start]Se muestra un mensaje "(vacío)" en columnas sin tareas [cite: 39]
9.  [cite_start]El layout es legible, bien organizado y visualmente claro [cite: 39]
10. [cite_start]El usuario puede volver al menú anterior desde la vista del tablero [cite: 39]

---

# [cite_start]SPRINT 5: ANÁLISIS Y EXPORTACIÓN [cite: sprint5]
## [cite_start]Temas: Estadísticas, Exportación de Datos [cite: sprint5]

---

## [cite_start]HU-008: Ver Estadísticas [cite: 46]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-008 | 🟠 Alta | Media |
[cite_start][cite: 47]

### [cite_start]Descripción [cite: 48]
> [cite_start]Como usuario, quiero ver estadísticas detalladas del proyecto para monitorear el progreso y analizar la distribución de trabajo.El sistema debe mostrar métricas comprehensivas sobre el estado de las tareas, prioridades, asignaciones y progreso general. [cite: 49]

### [cite_start]Criterios de Aceptación [cite: 50]
1.  [cite_start]Se muestra el total de tareas del proyecto [cite: 51]
2.  [cite_start]Se muestra el conteo de tareas por estado actual [cite: 51]
3.  [cite_start]Se muestra el porcentaje de tareas por estado [cite: 51]
4.  [cite_start]Se muestra el conteo de tareas por nivel de prioridad [cite: 51]
5.  [cite_start]Se muestra el porcentaje de tareas por prioridad [cite: 51]
6.  [cite_start]Se muestra el conteo de tareas asignadas vs sin asignar [cite: 51]
7.  [cite_start]Se muestra el porcentaje de tareas asignadas [cite: 51]
8.  [cite_start]Se muestra el conteo de tareas por columna [cite: 51]
9.  [cite_start]Se muestra el progreso general del proyecto (% completadas) [cite: 51]
10. [cite_start]Se identifican y muestran las tareas retrasadas [cite: 51]

---

## [cite_start]HU-009: Exportar Datos [cite: 52]

| ID | Prioridad | Complejidad |
| :--- | :--- | :--- |
| HU-009 | 🟡 Media | Media |
[cite_start][cite: 53]

### [cite_start]Descripción [cite: 54]
> [cite_start]Como usuario, quiero exportar datos del proyecto en diferentes formatos para poder analizar la información externamente con otras herramientas.El sistema debe permitir exportar a CSV, Markdown y JSON, manteniendo la integridad de los datos. [cite: 55]

### [cite_start]Criterios de Aceptación [cite: 56]
1.  [cite_start]El usuario puede exportar tareas a formato CSV [cite: 57]
2.  [cite_start]El archivo CSV incluye: ID, Título, Descripción, Prioridad, Estado, Asignado [cite: 57]
3.  [cite_start]El usuario puede exportar el proyecto a formato Markdown [cite: 57]
4.  [cite_start]El archivo Markdown tiene estructura jerárquica legible [cite: 57]
5.  [cite_start]El usuario puede exportar el proyecto a formato JSON [cite: 57]
6.  [cite_start]Los archivos exportados tienen nombres descriptivos y significativos [cite: 57]
7.  [cite_start]La codificación de archivos es UTF-8 para caracteres especiales [cite: 57]
8.  [cite_start]Se muestra un mensaje de confirmación después de exportar [cite: 57]
9.  [cite_start]Los datos exportados son completos, precisos y consistentes [cite: 57]
10. [cite_start]El proceso es eficiente incluso con muchas tareas [cite: 57]