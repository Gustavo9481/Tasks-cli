# MODULO: repositories
# .. ........................................................ repository_db ..󰌠
"""Define la capa de acceso a datos para la base de datos de tareas.

Este módulo contiene la clase RepositoryDB, que implementa todos los métodos
necesarios para interactuar con la base de datos SQLite (crear, leer,
actualizar, eliminar tareas).
"""
import sqlite3
import repositories.querys as sql
from pathlib import Path
from repositories.connection_manager import connection_manager
from models.model_task import Task


class RepositoryDB:
    """Gestiona todas las operaciones de la base de datos para las tareas.

    Esta clase abstrae las consultas SQL y proporciona una interfaz clara para
    que la capa de servicio interactúe con la base de datos.
    """

    def __init__(self, db_name: str):
        """Inicializa el repositorio y establece la ruta a la base de datos.

        Args:
            - db_name (str): El nombre del archivo de la base de datos
              (ej. "tasks-cli.db").
        """
        project_dir = Path(__file__).parent.parent
        self.db_path = project_dir / db_name

    def task_format_list(self, rows_list: list) -> list[Task]:
        """Convierte una lista de filas de la BD en una lista de objetos Task.

        Este método auxiliar actúa como una capa de mapeo, transformando los
        datos crudos de la base de datos (lista de tuplas) en una lista de
        objetos `Task` validados por Pydantic.

        Args:
            - rows_list (list): Lista de filas (tuplas) obtenida de una
              consulta a la base de datos.

        Returns:
            - list[Task]: Lista de objetos `Task` completamente formados.
        """
        return [
            Task(
                id=row[0],
                status=row[1],
                tag=row[2],
                content=row[3],
                priority=row[4],
                details=row[5],
            )
            for row in rows_list
        ]


    # .. ......................................................... create_table
    @connection_manager
    def create_table(self, cursor=sqlite3.Cursor) -> None:
        """Asegura que la tabla 'tasks_table' exista en la base de datos.

        Ejecuta la sentencia SQL para crear la tabla si esta no existe.
        La gestión de la conexión y el commit es manejada por el decorador.

        Args:
            - cursor (sqlite3.Cursor): Cursor de la base de datos, inyectado 
              por el decorador `connection_manager`.
        """
        cursor.execute(sql.CREATE_TABLE)


    # .. ........................................................ get_all_tasks
    @connection_manager
    def get_all_tasks(self, cursor: sqlite3.Cursor) -> list[Task]:
        """Recupera todas las tareas de la base de datos.

        Si la tabla no existe o hay un error, devuelve una lista vacía.

        Args:
            - cursor (sqlite3.Cursor): Cursor de la base de datos, inyectado 
              por el decorador.

        Returns:
            - list[Task]: Una lista de objetos `Task` que representan todas las
              tareas en la base de datos. Estará vacía si sqlite3 devuelve
              error.
        """
        try:
            cursor.execute(sql.GET_ALL_TASKS)
            all_rows = cursor.fetchall()
            return self.task_format_list(all_rows)
        except sqlite3.Error:
            return []


    # .. ............................................................. new_task
    @connection_manager
    def new_task(self, task_instance: Task, cursor: sqlite3.Cursor) -> int:
        """Inserta una nueva tarea en la base de datos.

        Args:
            - task_instance (Task): Objeto `Task` con los datos a insertar.
            - cursor (sqlite3.Cursor): Cursor de la base de datos, inyectado
              por el decorador.

        Returns:
            - int: ID de la fila de la tarea recién creada.
        """
        values = (
            task_instance.status,
            task_instance.tag,
            task_instance.content,
            task_instance.priority,
            task_instance.details,
        )

        cursor.execute(sql.NEW_TASK, values)

        new_id = cursor.lastrowid
        # Comprobación que new_id no es None (mypy).
        assert new_id is not None, "No se pudo obtener el ID de la nueva tarea."
        return new_id


    # .. ......................................................... filter_tasks
    @connection_manager
    def filter_tasks(
            self,
            cursor: sqlite3.Cursor,
            status: str | None = None,
            tag: str | None = None,
            priority: str | None = None
    ) -> list[Task]:
        """Filtra tareas dinámicamente por status, tag y/o prioridad.

        Utiliza un patrón Strategy para seleccionar la consulta SQL adecuada
        basándose en los filtros proporcionados. Si no se proporciona ningún
        filtro, devuelve todas las tareas.

        Args:
            - cursor (sqlite3.Cursor): Cursor de la base de datos, inyectado
              por el decorador.
            - status (str | None): Estado por el cual filtrar.
            - tag (str | None): Etiqueta por la cual filtrar.
            - priority (str | None): Prioridad por la cual filtrar.

        Returns:
            - list[Task]: Lista de objetos `Task` que coinciden con los
              criterios de filtrado.
        """
        # El diccionario mapea una clave de filtros activos a una estrategia
        strategy_map = {
        # (tiene_status, tiene_tag, tiene_prioridad): (consulta, [orden_parametros])
            (True, False, False): (sql.FILTER_TASK_STATUS, ['status']),
            (False, True, False): (sql.FILTER_TASK_TAG, ['tag']),
            (False, False, True): (sql.FILTER_TASK_PRIORITY, ['priority']),
            (True, True, False): (sql.FILTER_BY_STATUS_AND_TAG, ['status', 'tag']),
            (True, False, True): (sql.FILTER_BY_STATUS_AND_PRIORITY, ['status', 'priority']),
            (False, True, True): (sql.FILTER_BY_TAG_AND_PRIORITY, ['tag', 'priority']),
            (True, True, True): (sql.FILTER_BY_ALL, ['status', 'tag', 'priority']),
        }

        # 1. Creamos la clave para el diccionario
        key = (bool(status), bool(tag), bool(priority))

        # 2. Seleccionamos la estrategia
        if not any(key):
            # Caso especial: no hay filtros, obtener todo
            query = sql.GET_ALL_TASKS
            params = []
        else:
            query, param_names = strategy_map[key]

            # 3. Construimos la lista de parámetros en el orden correcto
            all_params = {'status': status, 'tag': tag, 'priority': priority}
            params = [all_params[name] for name in param_names]

        # 4. Ejecutamos la consulta seleccionada
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        return self.task_format_list(rows)


    # .. .......................................................... update_task
    @connection_manager
    def update_task(
        self, task_id: int, new_data: dict[str, str], cursor: sqlite3.Cursor
    ) -> None:
        """Actualiza uno o más campos de una tarea existente de forma dinámica.

        Construye la sentencia SQL dinámicamente a partir de los datos
        proporcionados en el diccionario `new_data`.

        Args:
            - task_id (int): ID de la tarea a actualizar.
            - new_data (dict[str, str]): Diccionario con los campos a
              actualizar y sus nuevos valores.
              Ejemplo: {"content": "Nuevo contenido", "priority": "alta"}
            - cursor (sqlite3.Cursor): Cursor de la base de datos, inyectado
              por el decorador.
        """
        if not new_data:
            print("No hay datos para actualizar la tarea.")
            return

        # Crea un str ej.: "content = ?, priority = ?, etc...".
        set_clause = ", ".join([f"{key} = ?" for key in new_data.keys()])
        # Crea una tupla como: ('Nuevo contenido', 'alta', 5).
        values = tuple(new_data.values()) + (task_id,)
        # Se arma el string de la consulta.
        query = f"{sql.UPDATE_TASK} {set_clause} WHERE id = ?;"

        cursor.execute(query, values)


    # .. ................................................ check_or_uncheck_task
    @connection_manager
    def check_or_uncheck_task(
            self, 
            id_task: int, 
            cursor: sqlite3.Cursor
    ) -> None:
        """Cambia el estado de una tarea de forma cíclica.

        Verifica primero si la tarea existe. Si existe, utiliza la consulta
        `UPDATE_STATUS_TOGGLE` para rotar el estado.

        Args:
            - id_task (int): ID de la tarea cuyo estado se va a cambiar.
            - cursor (sqlite3.Cursor): Cursor de la base de datos, inyectado
              por el decorador.
        """
        select_task = cursor.execute(sql.SELECT_TASK, (id_task,)).fetchone()

        if select_task is None:
            print("El id de la tarea no es correcto o no existe")
            return

        cursor.execute(sql.UPDATE_STATUS_TOGGLE, (id_task,))


    # .. ....................................................... get_task_by_id
    @connection_manager
    def get_task_by_id(
            self, 
            id_task: int, 
            cursor: sqlite3.Cursor
    ) -> Task | None:
        """Recupera una única tarea por su ID.

        Args:
            - id_task (int): ID de la tarea a recuperar.
            - cursor (sqlite3.Cursor): Cursor de la base de datos, inyectado
              por el decorador.

        Returns:
            - Task | None: Objeto `Task` si se encuentra la tarea, o `None`
              si no existe ninguna tarea con ese ID.
        """
        cursor.execute(sql.GET_TASK_BY_ID, (id_task,))
        row = cursor.fetchone()

        if row:
            return self.task_format_list([row])[0]
        else:
            return None


    # .. .......................................................... delete_task
    @connection_manager
    def delete_task(self, id_task: int, cursor: sqlite3.Cursor) -> None:
        """Elimina una tarea de la base de datos por su ID.

        Args:
            - id_task (int): ID de la tarea a eliminar.
            - cursor (sqlite3.Cursor): Cursor de la base de datos, inyectado
              por el decorador.
        """
        cursor.execute(sql.DELETE_TASK, (id_task,))
