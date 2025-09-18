# MODULO: config
# .. ........................................................ config_loader ..󰌠
"""Módulo para cargar y hacer disponible la configuración de la aplicación.

El módulo se encarga de leer el archivo 'settings.toml' y extraer los datos de
él, dando la posibilidad de usar esos datos para establecer la configuración de
la aplicación facilitando la importación desde otros módulos.
"""
import tomllib
from pathlib import Path
from typing import Any


# Ruta al archivo de configuración, construida de forma relativa al script.
_CONFIG_FILE_PATH = Path(__file__).parent / "settings.toml"

# Carga el contenido del archivo .toml en un diccionario.
_config_data: dict[str, Any]
with open(_CONFIG_FILE_PATH, "rb") as f:
    _config_data = tomllib.load(f)


# .. .................................... Carga de valores de configuración ..󰌠
# Expone el nombre de la base de datos. Usa un valor por defecto 'tasks.db' si
# no se encuentra.
DATABASE_NAME = _config_data.get("database_name", "tasks.db")

# Expone las configuraciones de la interfaz de usuario (colores e íconos).
_ui_config = _config_data.get("ui", {})
UI_COLORS = _ui_config.get("colors", {})
UI_ICONS = _ui_config.get("icons", {})
