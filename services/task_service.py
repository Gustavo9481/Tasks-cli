# MODULO: services
# .. ............................ task_service ............................ ..
"""
Contiene la lógica de negocio de la aplicación.

Esta capa actúa como un intermediario entre la interfaz de usuario (controllers)
y la capa de acceso a datos (repositories). Orquesta las operaciones y
asegura que la lógica de la aplicación esté centralizada.
"""
from rich.text import Text
from repositories.repository_db import RepositoryDB
from models.model_task import Task
from config.config_loader import UI_ICONS

class TaskService:
    """Clase de servicio que maneja la lógica de negocio para las tareas. """

    def __init__(self):
        """El servicio crea su propia instancia del repositorio. """
        self.repository = RepositoryDB("data_dev2.db")

    # FUNC: traer todas las tareas
    def get_all_tasks(self) -> list[Task]:
        """Obtiene todos los objetos Task puros desde el repositorio."""
        return self.repository.get_all_tasks()

    def get_tasks_for_ui(self) -> list[tuple]:
        """Obtiene las tareas y las formatea para la UI, imitando el formato
        del archivo db_tareas.py original.
        """
        headers = ("ID", "Status", "Tag", "Contenido", "Prioridad", "Notas")
        task_objects = self.get_all_tasks()
        formatted_tasks = [headers]
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
        """Busca una tarea por su ID a través del repositorio."""
        return self.repository.get_task_by_id(task_id)


    # FUNC: nueva tarea.
    def new_task_service(self, task_instance: Task) -> None:
        """Servicio para crear una nueva tarea. """
        self.repository.new_task(task_instance)


    # FUNC: marcar | desmarcar tarea.
    def check_or_uncheck_task_service(self, task_id: int) -> None:
        """Marca o desmarca una tarea usando su ID. 

        Args:
            - task_id (int): El ID de la tarea a marcar o desmarcar (status) 
        """
        self.repository.check_or_uncheck_task(task_id)


    # FUNC: editar trea.
    def update_task_service(self, task_id: int, new_data: dict[str, str]) -> None:
        """Servicio para actualizar una tarea existente."""
        self.repository.update_task(task_id, new_data)


    # FUNC: filtrar tareas.
    def filter_tasks_service(
        self,
        status: str | None = None,
        tag: str | None = None,
        priority: str | None = None,
    ) -> list[Task]:
        """Filtra las tareas según los criterios proporcionados, llamando
        al método correspondiente del repositorio.

        Args:
            -status (str | None, optional): El estado por el cual filtrar.
            - tag (str | None, optional): El tag por el cual filtrar.
            - priority (str | None, optional): La prioridad por la cual filtrar.

        Returns:
            - list[Task]: Una lista de objetos Task que coinciden con los filtros.
        """
        return self.repository.filter_tasks(
            status=status,
            tag=tag,
            priority=priority
        )








    # FUNC: eliminar tarea
    def delete_task_service(self, task_id: int) -> None:
        """Elimina una tarea usando su ID.

        Args:
            - task_id (int): El ID de la tarea a eliminar.
        """
        self.repository.delete_task(task_id)



# TEST: verificación directa de los servicios.
# WARN: éste bloque será eliminado al terminar el desarrollo de los servicios.

if __name__ == "__main__":
    service = TaskService()

    print("--- Verificando get_tasks_for_ui ---")
    tareas_formateadas = service.get_tasks_for_ui()
    for fila in tareas_formateadas:
        print(fila)
