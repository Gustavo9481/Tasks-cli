# MODULO: repositories/
# .. ........................... repository_db ............................ ..󰌠
"""
Contiene la clase RepositoryDB, la cual posee los métodos de consultas a la
base de datos.
"""
import sqlite3
import repositories.querys as sql
from pathlib import Path
from typing import List, Tuple, Any
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
    # .. ............................................. new_task
    @connection_manager
    def new_task(self, task_instance: Task, cursor: sqlite3.Cursor) -> None:
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
        )

        cursor.execute(sql.NEW_TASK, values)
        # return cursor.lastrowid
        return

    # FUNC:
    # .. ................................... filter_task_status
    @connection_manager
    def filter_task_status(
        self, status_task: str, cursor: sqlite3.Cursor
    ) -> List[Tuple[Any, ...]]:
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
        cursor.execute(sql.FILTER_TASK_STATUS, (status_task,))
        task_list_filter_by_status = cursor.fetchall()

        return task_list_filter_by_status

    # FUNC:
    # .. ...................................... filter_task_tag
    @connection_manager
    def filter_task_tag(
        self, tag_task: str, cursor: sqlite3.Cursor
    ) -> List[Tuple[Any, ...]]:
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
        cursor.execute(sql.FILTER_TASK_TAG, (tag_task,))
        task_list_filter_by_tag = cursor.fetchall()

        return task_list_filter_by_tag

    # FUNC:
    # .. ................................. filter_task_priority
    @connection_manager
    def filter_task_priority(
        self, priority_task: str, cursor: sqlite3.Cursor
    ) -> List[Tuple[Any, ...]]:
        """Filtar una tarea por prioridad.

        Args:
            - priority_task (Status): La prioridad por la cual filtrar las
                tareas (e.g., "baja", "media", "alta").
            - cursor (sqlite3.Cursor): Objeto cursor de la base de datos,
                proporcionado automáticamente por el decorador.

        Returns:
            - List[Tuple[Any, ...]]: Una lista de tuplas, donde cada tupla
                representauna fila de la tarea encontrada.
        """
        cursor.execute(sql.FILTER_TASK_PRIORITY, (priority_task,))
        task_list_filter_by_priority = cursor.fetchall()

        return task_list_filter_by_priority

    # FUNC:
    # .. .......................................... update_task
    @connection_manager
    def update_task(
        self, id_task: int, new_data: dict[str, str], cursor: sqlite3.Cursor
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

        # Crea un string como: "content = ?, priority = ?, etc...
        set_clause = ", ".join([f"{key} = ?" for key in new_data.keys()])

        # Crea una tupla como: ('Nuevo contenido', 'alta', 5)
        values = tuple(new_data.values()) + (id_task,)

        # Se arma el string de la consulta.
        query = f"{sql.UPDATE_TASK} {set_clause} WHERE id = ?;"

        cursor.execute(query, values)

        """
        data: List = [status_task, tag_task, content_task, priority_task]
        select_task = cursor.execute(sql.SELECT_TASK,(id_task,)).fetchone()
        cursor.execute(sql.UPDATE_TASK, (*data, id_task))
        """

    # FUNC:
    # .. ................................ check_or_uncheck_task
    @connection_manager
    def check_or_uncheck_task(
            self,
            id_task: int,
            cursor: sqlite3.Cursor) -> None:
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


# TEST:
repo = RepositoryDB("data_dev.db")
repo.create_table()
tarea = Task(content="GUScode nuevo contenido")
repo.new_task(tarea)
