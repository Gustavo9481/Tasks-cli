# MODULO: repositories/
# .. ......................... connection_manager ......................... ..󰌠
"""Define un decorador para la gestión automática de conexiones a SQLite.

Este módulo proporciona el decorador `connection_manager`, que abstrae el
ciclo de vida de la conexión (apertura, commit/rollback, cierre) para
los métodos que interactúan con la base de datos.
"""
import sqlite3
import logging
from typing import Callable, Any


# Configuración básica del logger.
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


def connection_manager(func: Callable[..., Any]) -> Callable[..., Any]:
    """Gestiona el ciclo de vida de la conexión a la base de datos para un
    método.

    Este decorador está diseñado para envolver métodos de una clase que
    necesitan interactuar con la base de datos. Se asume que la instancia de la
    clase (`self`) tiene un atributo `db_path` con la ruta al archivo de la
    base de datos.

    El decorador se encarga de:
    1. Abrir una conexión a la base de datos usando `sqlite3.connect`.
    2. Crear un cursor.
    3. Ejecutar el método decorado, inyectándole el `cursor` como un argumento
       de palabra clave (keyword argument).
    4. Cerrar el cursor de forma segura.
    5. Hacer commit de la transacción si tiene éxito (implícito en `with`).
    6. Capturar y registrar cualquier `sqlite3.Error`, evitando que el programa
       se detenga.

    Args:
        func (Callable): El método a decorar. Debe ser un método de instancia
            y estar preparado para recibir un argumento de palabra clave
            `cursor`.

    Returns:
        Callable: El nuevo método envuelto con la gestión de conexión.
    """

    def db_decorator(self, *args: Any, **kwargs: Any) -> Any:
        try:
            with sqlite3.connect(self.db_path) as db_connect:
                cursor = db_connect.cursor()
                try:
                    # El cursos debe pasar como argumento de palabra clave.
                    return func(self, *args, cursor=cursor, **kwargs)
                finally:
                    cursor.close()
        except sqlite3.Error as e:
            # Registra el error con el módulo logging, incluyendo el traceback.
            logging.error(
                f"Error al acceder a la base de datos: {e}",
                exc_info=True
            )

            return None

    return db_decorator
