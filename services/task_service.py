# MODULO: services
# .. ............................ task_service ............................ ..
"""
Contiene la lógica de negocio de la aplicación.

Esta capa actúa como un intermediario entre la interfaz de usuario (controllers)
y la capa de acceso a datos (repositories). Orquesta las operaciones y
asegura que la lógica de la aplicación esté centralizada.
"""
from typing import Any
from repositories.repository_db import RepositoryDB
from models.model_task import Task
from config.config_loader import UI_ICONS


class TaskService:
    """Gestiona las operaciones de alto nivel relacionadas con las tareas.

    Esta clase desacopla la interfaz de usuario de los detalles de la base de
    datos. Recibe solicitudes de la UI, aplica la lógica de negocio y
    coordina las operaciones con la capa de repositorio.
    """

    def __init__(self):
        """Inicializa el servicio de tareas.

        Crea una instancia del `RepositoryDB` para interactuar con la base de
        datos. El nombre de la base de datos está definido aquí para
        configurar el repositorio que usará este servicio.
        """
        self.repository = RepositoryDB("data_dev2.db")


    def get_all_tasks(self) -> list[Task]:
        """Recupera todas las tareas como objetos `Task` puros.

        Este método se comunica con el repositorio para obtener una lista
        completa de las tareas, devolviéndolas como objetos de modelo sin
        formato.

        Returns:
            - list[Task]: Lista de objetos `Task`.
        """
        return self.repository.get_all_tasks()


    def get_tasks_for_ui(self) -> list[tuple]:
        """Prepara y formatea los datos de las tareas para ser mostrados
        correctamente en la UI.

        A diferencia de `get_all_tasks`, este método transforma la lista de
        objetos `Task` en un formato específico para el `DataTable` de Textual,
        incluyendo cabeceras y un indicador visual para las notas extras.

        Returns:
            - list[tuple[Any, ...]: Lista de tuplas donde el primer elemento es
              la fila de cabeceras y los siguientes son las filas de tareas.
        """
        headers = ("ID", "Status", "Tag", "Contenido", "Prioridad", "Notas")
        task_objects = self.get_all_tasks()
        formatted_tasks: list[tuple[Any, ...]] = [headers]
        for task in task_objects:
            details_indicator = UI_ICONS['nota'] if task.details else ""
            formatted_tasks.append(
                (
                    task.id,
                    task.status,
                    task.tag,
                    task.content,
                    task.priority,
                    details_indicator
                )
            )
        return formatted_tasks


    def get_task_by_id_service(self, task_id: int) -> Task | None:
        """Busca y devuelve una única tarea por su ID.

        Args:
            - task_id (int): ID de la tarea a buscar.

        Returns:
            - Task | None: Objeto `Task` si se encuentra, o `None` si no.
        """
        return self.repository.get_task_by_id(task_id)


    def new_task_service(self, task_instance: Task) -> None:
        """Procesa la creación de una nueva tarea.

        Recibe un objeto `Task` desde la capa de control y lo pasa al
        repositorio para su inserción en la base de datos.

        Args:
            - task_instance (Task): Objeto `Task` (sin ID) a crear.
        """
        self.repository.new_task(task_instance)


    def check_or_uncheck_task_service(self, task_id: int) -> None:
        """Orquesta el cambio de estado cíclico de una tarea.

        Delega la operación de cambiar el estado de una tarea (ej. de
        'pending' a 'in_progress') al repositorio.

        Args:
            - task_id (int): ID de la tarea a modificar.
        """
        self.repository.check_or_uncheck_task(task_id)


    def update_task_service(
            self,
            task_id: int,
            new_data: dict[str, str]
    ) -> None:
        """Procesa la actualización de una tarea existente.

        Recibe el ID de la tarea y un diccionario con los nuevos datos,
        y se los pasa al repositorio para que aplique los cambios.

        Args:
            - task_id (int): ID de la tarea a actualizar.
            - new_data (dict[str, str]): Diccionario con los campos a
              modificar y sus nuevos valores.
        """
        self.repository.update_task(task_id, new_data)


    def filter_tasks_service(
        self,
        status: str | None = None,
        tag: str | None = None,
        priority: str | None = None,
    ) -> list[Task]:
        """Filtra las tareas según los criterios proporcionados.

        Pasa los criterios de filtro directamente al repositorio para que
        ejecute la consulta de búsqueda correspondiente.

        Args:
            - status (str | None, optional): Estado por el cual filtrar.
            - tag (str | None, optional): Etiqueta por la cual filtrar.
            - priority (str | None, optional): Prioridad por la cual filtrar.

        Returns:
            - list[Task]: Lista de objetos `Task` que coinciden con los
              criterios de filtrado.
        """
        return self.repository.filter_tasks(
            status=status,
            tag=tag,
            priority=priority
        )


    def delete_task_service(self, task_id: int) -> None:
        """Procesa la eliminación de una tarea por su ID.

        Args:
            - task_id (int): ID de la tarea a eliminar.
        """
        self.repository.delete_task(task_id)
