# MODULO: repositories/
# .. ......................... connection_manager ......................... ..󰌠
"""
Decorador gestor de conexión a base de datos.
"""

import sqlite3
import logging
from typing import Callable, Any

# Configuración básica del logger.
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


def connection_manager(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorador para manejar la conexión a la base de datos SQLite y el cursor

    Abre una conexión a la base de datos SQLite, crea un cursor, ejecuta la
    función decorada pasando el cursor como argumento y luego cierra el cursor
    Además, captura cualquier error de la base de datos que pueda ocurrir
    durante la ejecución de la función decorada.

    Args:
        - func (Callable[..., Any]): Función a decorar. Debe aceptar un
          argumento adicional 'cursor' que será proporcionado automáticamente
          por eldecorador.

    Returns:
        - (Callable[..., Any]) La función decorada con manejo automático de la
          conexión a la base de datos.

    Raises:
        - sqlite3.Error: Si ocurre un error al acceder a la base de datos.
    """

    def db_decorator(self, *args: Any, **kwargs: Any) -> Any:
        """
        Función envoltorio que gestiona la conexión y el cursor de SQLite.

        Espera que 'self' tenga un atributo 'db_path' que apunte a la ruta
        del archivo de la base de datos SQLite.
        """
        try:
            with sqlite3.connect(self.db_path) as db_connect:
                cursor = db_connect.cursor()
                try:
                    # Aseguramos que el cursor se pase como argumento de
                    # palabra clave.
                    return func(self, *args, cursor=cursor, **kwargs)
                finally:
                    cursor.close()
        except sqlite3.Error as e:
            # Registra el error con el módulo logging, incluyendo el traceback.
            logging.error(f"Error al acceder a la base de datos: {e}", exc_info=True)

            return None

    return db_decorator
