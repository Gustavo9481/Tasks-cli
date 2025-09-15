# MODULO: controllers
# .. ........................................................... decorators ..󰌠
"""
Contiene los decoradores personalizados para la aplicación.
"""
# OK: 
from functools import wraps
from typing import Callable, Any
from services.task_service import TaskService


def require_valid_id(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador que valida el ID y muestra notificaciones de error.

    Realiza 3 comprobaciones:
        1. Que el ID no esté vacío.
        2. Que el ID sea un número entero.
        3. Que el ID exista en la base de datos.

    Si alguna falla, muestra una notificación y detiene la ejecución.
    Si todo es correcto, llama a la función original con el ID (int).
    """
    @wraps(func)
    def wrapper(self, task_id_str: str):

        # 1. Comprobar si el string está vacío
        if not task_id_str:
            self.app.notify(
                "No se introdujo ningún ID.",
                title="Acción cancelada",
                severity="warning",
                timeout=3
            )
            return

        # 2. Comprobar si es un número entero
        try:
            task_id_int = int(task_id_str)
        except ValueError:
            self.app.notify(
                f"La entrada '{task_id_str}' no es un número válido.",
                title="Error de entrada",
                severity="error",
                timeout=3
            )
            return

        # 3. Comprobar si el ID existe en la BD
        service = TaskService()
        if service.get_task_by_id_service(task_id_int) is None:
            self.app.notify(
                f"La tarea con el ID '{task_id_int}' no existe.",
                title="Error de operación",
                severity="error",
                timeout=3
            )
            return

        # Si todas las comprobaciones pasan, ejecuta la función original
        return func(self, task_id_int)

    return wrapper
