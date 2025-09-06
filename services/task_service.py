# MODULO: services/
# .. ............................ task_service ............................ ..
"""
Contiene la lógica de negocio de la aplicación.

Esta capa actúa como un intermediario entre la interfaz de usuario (controllers)
y la capa de acceso a datos (repositories). Orquesta las operaciones y
asegura que la lógica de la aplicación esté centralizada.
"""

from repositories.repository_db import RepositoryDB
from models.model_task import Task

class TaskService:
    """
    Clase de servicio que maneja la lógica de negocio para las tareas.
    """
    def __init__(self):
        # El servicio crea su propia instancia del repositorio.
        self.repository = RepositoryDB("data_dev2.db")

    def get_all_tasks(self) -> list[Task]:
        """Obtiene todos los objetos Task puros desde el repositorio."""
        return self.repository.get_all_tasks()

    def get_tasks_for_ui(self) -> list[tuple]:
        """Obtiene las tareas y las formatea para la UI, imitando el formato
        del archivo db_tareas.py original.
        """
        headers = ("ID", "Status", "Tag", "Contenido", "Prioridad")
        task_objects = self.get_all_tasks()
        formatted_tasks = [headers]
        for task in task_objects:
            formatted_tasks.append(
                (
                    task.id,
                    task.status,
                    task.tag,
                    task.content,
                    task.priority,
                )
            )
        return formatted_tasks

    def delete_task_by_id(self, task_id: int) -> None:
        """Elimina una tarea usando su ID.

        Args:
            task_id (int): El ID de la tarea a eliminar.
        """
        # Simplemente llama al método correspondiente del repositorio.
        self.repository.delete_task(task_id)


# --- Bloque de Verificación ---
if __name__ == "__main__":
    service = TaskService()

    print("--- Verificando get_tasks_for_ui ---")
    tareas_formateadas = service.get_tasks_for_ui()
    for fila in tareas_formateadas:
        print(fila)
