# Arquitectura del Proyecto

La arquitectura de **Tasks-CLI** está diseñada siguiendo los principios de
**Separación de Responsabilidades (SoC)**, lo que busca desarrollar un  sistema
robusto, mantenible y fácil de testear.

Se implementa un patrón de **arquitectura por capas**, donde cada capa tiene un
rol bien definido y se comunica con las demás a través de interfaces claras.

## Diagrama de Arquitectura

El siguiente diagrama muestra las capas principales de la aplicación y el flujo
de dependencias. La comunicación es unidireccional (de arriba hacia abajo),
asegurando que las capas superiores no conozcan los detalles de implementación
de las inferiores.



<p align="center">
    <img src="/images/arquitectura.svg"
        alt="Diagrama UML Task"
        width="450" align="center"/>
</p>



## Descripción de las Capas

### 1. Capa de Controladores (`controllers/`)

*   **Responsabilidad:** Gestionar toda la interacción con el usuario.
Es la única capa que "sabe" que estamos en una terminal.
*   **Componentes Clave:**
    *   `interface.py`: Contiene la clase principal `Interface` (la app de Textual),
    que genera y gestiona la UI, los atajos de teclado y las acciones.
    *   `screens.py`: Define las pantallas modales (`AskIdScreen`, `AddTaskScreen`, etc.)
    que se usan para capturar datos del usuario de forma aislada.
*   **Flujo:** Recibe las acciones del usuario, las traduce en llamadas a la capa
de **Servicios** y, cuando recibe datos de vuelta, los formatea para mostrarlos
en la terminal. **Nunca interactúa directamentecon el Repositorio.**

### 2. Capa de Servicios (`services/`)

*   **Responsabilidad:** Contener la lógica de negocio de la aplicación.
*   **Componentes Clave:**
    *   `task_service.py`: La clase `TaskService` implementa las operaciones
    como "crear una nueva tarea" o "filtrar tareas".
*   **Flujo:** Es llamado por la capa de Controladores. Administra las operaciones
validando datos, creando objetos del Modelo y utilizando la capa de **Repositorios**
para persistir o recuperar información. No sabe nada sobre la interfaz de
usuario ni sobre consultas SQL.

### 3. Capa de Repositorios (`repositories/`)

*   **Responsabilidad:** Abstraer y gestionar todo el acceso a la base de datos.
Es la única capa que sabe cómo y dónde se guardan los datos.
*   **Componentes Clave:**
    *   `repository_db.py`: La clase `RepositoryDB` implementa los métodos para
    cada operación en la base de datos (CRUD: Create, Read, Update, Delete).
    *   `querys.py`: Centraliza todas las sentencias SQL como constantes,
    mejorando la legibilidad y el mantenimiento.
    *   `connection_manager.py`: Proporciona un decorador (`@connection_manager`)
    que gestiona automáticamente el ciclo de vida de la conexión a la base de
    datos, manteniendo los métodos limpios y enfocados en su tarea.
*   **Flujo:** Es utilizado exclusivamente por la capa de **Servicios**.
Recibe órdenes, ejecuta las consultas SQL correspondientes y devuelve los datos
crudos o los transforma en objetos del **Modelo**.

### 4. Capa de Modelos (`models/`)

*   **Responsabilidad:** Definir la estructura de los datos de la aplicación.
Actúa como un **Data Transfer Object (DTO)**.
*   **Componentes Clave:**
    *   `model_task.py`: Define la clase `Task` usando `Pydantic` para la
    validación automática de tipos y restricciones.
*   **Flujo:** Los objetos `Task` son utilizados por todas las capas para
asegurar un transporte de datos consistente y seguro a través de la aplicación.

## Flujo de Ejemplo: Añadir una Nueva Tarea

1.  **Usuario:** Presiona la tecla `n` en la terminal.

2.  **Controlador (`Interface`):** El `action_add_task` es invocado. Muestra la pantalla `AddTaskScreen`.

3.  **Controlador (`AddTaskScreen`):** El usuario rellena los datos y presiona "Crear". La pantalla se cierra y devuelve un diccionario con los datos a `Interface`.

4.  **Controlador (`Interface`):** El método `notification_add_task` recibe los datos y llama a `TaskService.new_task_service()`.

5.  **Servicio (`TaskService`):** Recibe los datos, crea un objeto `Task` validado por Pydantic.

6.  **Servicio (`TaskService`):** Llama a `RepositoryDB.new_task()`, pasándole el objeto `Task`.

7.  **Repositorio (`RepositoryDB`):** El decorador `@connection_manager` abre una conexión. El método `new_task` extrae los datos del objeto `Task`, ejecuta la `INSERT` query y hace commit.

8.  **Retorno:** El control vuelve a través de las capas. La `Interface`
finalmente llama a `_update_table()` para refrescar la UI con la nueva tarea.
