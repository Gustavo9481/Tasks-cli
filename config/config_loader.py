# MODULO: config
# .. ........................................................ config_loader ..󰌠
"""Módulo para cargar y exponer la configuración de la aplicación.

Este módulo lee el archivo `settings.toml` y expone las configuraciones
necesarias (como el nombre de la base de datos y los ajustes de la UI)
como constantes para que otros módulos puedan importarlas fácilmente.
"""

# OK: 

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
