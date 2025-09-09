# MODULO: repositories/
# .. ........................... repository_db ............................ ..󰌠
"""
Contiene la clase RepositoryDB, la cual posee los métodos de consultas a la
base de datos.
"""

import sqlite3
import repositories.querys as sql
from pathlib import Path
from repositories.connection_manager import connection_manager
from models.model_task import Task


# CLASS:
class RepositoryDB:
    """Clase contenedora de los métodos de consulta sql a la base de datos.

    Inicializa el repositorio con un nombre de base de datos específico.

    Args:
        - db_name (str): El nombre del archivo de la base de datos
          (ej. "tasks-cli.db").
    """

    def __init__(self, db_name: str):
        project_dir = Path(__file__).parent.parent
        self.db_path = project_dir / db_name

    def task_format_list(self, rows_list: list) -> list[Task]:
        """Convierte filas crudas de la BD en una lista de objetos Task.

        Esta función es un método de ayuda crucial que actúa como una capa de
        traducción. Su propósito es tomar los datos "crudos" que devuelve la
        base de datos (una lista de tuplas) y transformarlos en una lista de
        objetos `Task` estructurados y seguros.

        Al centralizar esta lógica aquí, nos aseguramos de que el resto de la
        aplicación no tenga que preocuparse por el orden de las columnas de la
        base de datos, sino que pueda trabajar directamente con objetos `Task`
        claros y predecibles.

        Args:
            - rows_list (list): La lista de filas (tuplas) obtenida de la base
              de datos tras una consulta a la tabla `tasks_table`.

        Returns:
            - list[Task]: Una lista de objetos `Task` completamente formados.
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

    # FUNC:
    # .. ......................................... create_table
    @connection_manager
    def create_table(self, cursor=sqlite3.Cursor) -> None:
        """Verifica si la tabla existe, si no, la crea.

        No es necesario un commit explícito aquí si el decorador usa
        'with sqlite3.connect', ya que maneja el commit/rollback de forma
        automática.

        Args:
            - cursor (sqlite3.Cursor): cursor de connexión sqlite.

        Returns:
            - None.
        """
        cursor.execute(sql.CREATE_TABLE)



    # FUNC:
    @connection_manager
    def get_all_tasks(self, cursor: sqlite3.Cursor) -> list[Task]:
        """Recupera todas las tareas de la base de datos.

        Args:
            - cursor (sqlite3.Cursor): Proporcionado por el decorador.

        Returns:
            - list[Task]: Una lista de todos los objetos Task en la base de datos.
        """
        cursor.execute(sql.GET_ALL_TASKS)
        all_rows = cursor.fetchall()
        return self.task_format_list(all_rows)


    # FUNC:
    # .. ............................................. new_task
    @connection_manager
    def new_task(self, task_instance: Task, cursor: sqlite3.Cursor) -> int:
        """Crea una nueva tarea en la base de datos.

        Args:
            - task_instance (Task): Objeto Task que contiene los datos de la
              nueva tarea.
            - cursor (sqlite3.Cursor): Objeto cursor de la base de datos,
              proporcionado automáticamente por el decorador.

        Returns:
            - int: El ID de la tarea recién creada en la base de datos.
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
        # Le aseguramos a mypy (y a nosotros mismos) que new_id no será None.
        assert new_id is not None, "No se pudo obtener el ID de la nueva tarea."
        return new_id

    # FUNC:
    # .. ................................... filter_task_status
    @connection_manager
    def filter_task_status(self, status: str, cursor: sqlite3.Cursor) -> list[Task]:
        """Filtar una tarea por status.

        Args:
            - status_task (Status): El estado por el cual filtrar las tareas
              (e.g., "pending", "completed").
            - cursor (sqlite3.Cursor): Objeto cursor de la base de datos,
              proporcionado automáticamente por el decorador.

        Returns:
            - List[Tuple[Any, ...]]: Una lista de tuplas, donde cada tupla
              representauna fila de la tarea encontrada.
        """
        cursor.execute(sql.FILTER_TASK_STATUS, (status,))
        filtered_rows = cursor.fetchall()

        task_list = self.task_format_list(filtered_rows)

        return task_list

    # FUNC:
    # .. ...................................... filter_task_tag
    @connection_manager
    def filter_task_tag(self, tag: str, cursor: sqlite3.Cursor) -> list[Task]:
        """Filtar una tarea por tag.

        Args:
            - tag_task (Status): El tag por el cual filtrar las tareas
              (e.g., "personal", "proyecto", "trabajo", "calendario").
            - cursor (sqlite3.Cursor): Objeto cursor de la base de datos,
              proporcionado automáticamente por el decorador.

        Returns:
            - List[Tuple[Any, ...]]: Una lista de tuplas, donde cada tupla
              representauna fila de la tarea encontrada.
        """
        cursor.execute(sql.FILTER_TASK_TAG, (tag,))
        filtered_rows = cursor.fetchall()

        task_list = self.task_format_list(filtered_rows)

        return task_list

    # FUNC:
    # .. ................................. filter_task_priority
    @connection_manager
    def filter_task_priority(self, priority: str, cursor: sqlite3.Cursor) -> list[Task]:
        """Filtar una tarea por prioridad.

        Args:
            - priority (Status): La prioridad por la cual filtrar las
              tareas (e.g., "baja", "media", "alta").
            - cursor (sqlite3.Cursor): Objeto cursor de la base de datos,
              proporcionado automáticamente por el decorador.

        Returns:
            - List[Tuple[Any, ...]]: Una lista de tuplas, donde cada tupla
              representauna fila de la tarea encontrada.
        """
        cursor.execute(sql.FILTER_TASK_PRIORITY, (priority,))
        filtered_rows = cursor.fetchall()

        task_list = self.task_format_list(filtered_rows)

        return task_list

    # FUNC:
    # .. .......................................... update_task
    @connection_manager
    def update_task(
        self, task_id: int, new_data: dict[str, str], cursor: sqlite3.Cursor
    ) -> None:
        """Actualizar status, tag, contenido o prioridad de una tarea.

        Args:
            - id_task (int): El ID de la tarea a actualizar.
            - new_data (dict[str, str]): Un diccionario con los campos a
              actualizar y sus nuevos valores.
              Ejemplo: {"content": "Nuevo contenido", "priority": "alta"}
            - cursor (sqlite3.Cursor): Cursor de la base de datos.

        Returns:
            - None.
        """
        if not new_data:
            print("No hay datos para actualizar la tarea.")
            return

        # 01
        set_clause = ", ".join([f"{key} = ?" for key in new_data.keys()])
        # 02
        values = tuple(new_data.values()) + (task_id,)
        # 03
        query = f"{sql.UPDATE_TASK} {set_clause} WHERE id = ?;"

        cursor.execute(query, values)

        # 01: Crea un str ej.: "content = ?, priority = ?, etc...".
        # 02: Crea una tupla como: ('Nuevo contenido', 'alta', 5).
        # 03: Se arma el string de la consulta.

    # FUNC:
    # .. ................................ check_or_uncheck_task
    @connection_manager
    def check_or_uncheck_task(self, id_task: int, cursor: sqlite3.Cursor) -> None:
        """Marcar como completada o desmaracar como pendiente una tarea.

        Args:
            - id_task (int): número de identificación de la tarea.
            - cursor (sqlite3.Cursor): Objeto cursor de la base de datos,
              proporcionado automáticamente por el decorador.

        Returns:
            - None.
        """
        select_task = cursor.execute(sql.SELECT_TASK, (id_task,)).fetchone()

        if select_task is None:
            print("El id de la tarea no es correcto o no existe")
            return

        cursor.execute(sql.UPDATE_STATUS_TOGGLE, (id_task,))

    # FUNC:
    # .. ....................................... get_task_by_id
    @connection_manager
    def get_task_by_id(self, id_task: int, cursor: sqlite3.Cursor) -> Task | None:
        """Selecciona una tarea existente por su id.

        Args:
            - id_task (int): número de identificación de la tarea.
            - cursor (sqlite3.Cursor): Objeto cursor de la base de datos,
              proporcionado automáticamente por el decorador.

        Returns:
            - Task | None.
        """
        cursor.execute(sql.GET_TASK_BY_ID, (id_task,))
        row = cursor.fetchone()

        if row:
            return self.task_format_list([row])[0]
        else:
            return None

    # FUNC:
    # .. .......................................... delete_task
    @connection_manager
    def delete_task(self, id_task: int, cursor: sqlite3.Cursor) -> None:
        """Eliminar una tarea existente.

        Args:
            - id_task (int): número de identificación de la tarea.
            - cursor (sqlite3.Cursor): Objeto cursor de la base de datos,
              proporcionado automáticamente por el decorador.

        Returns:
            - None.
        """
        cursor.execute(sql.DELETE_TASK, (id_task,))
