# MODULO: repositories
# .. ............................................................ database ..󰌠
"""Módulo para gestionar la ruta de la base de datos de la aplicación.

Utiliza la biblioteca `platformdirs` para determinar la ruta apropiada para
almacenar los datos de la aplicación, asegurando que sea persistente y esté
en la ubicación correcta según el sistema operativo.
"""
from pathlib import Path
from platformdirs import PlatformDirs


# Se utiliza el nombre del autor y de la aplicación para crear un directorio
# único y evitar conflictos con otras aplicaciones.
_dirs = PlatformDirs(appname="tasks-cli", appauthor="GUScode")

# Se construye la ruta completa a la base de datos, asegurando que el
# directorio de datos del usuario exista.
_data_dir = _dirs.user_data_path
_data_dir.mkdir(parents=True, exist_ok=True)

# Se define la ruta de la base de datos de producción.
DATABASE_PATH = _data_dir / "tasks-cli.db"
# Se define la ruta de la base de datos para las pruebas.
TEST_DATABASE_PATH = _data_dir / "tasks-cli-tests.db"