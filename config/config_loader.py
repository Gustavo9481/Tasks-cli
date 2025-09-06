# MODULO: config
"""
Carga la configuración del proyecto desde el archivo settings.toml.
"""
import tomllib
from pathlib import Path

# Carga del archivo con los datos de la configuración.
_CONFIG_FILE_PATH = Path(__file__).parent / "settings.toml"

with open(_CONFIG_FILE_PATH, "rb") as f:
    _config_data = tomllib.load(f)


# Definición de la base de datos.
# Uso de .get() con valor por defecto 'tasks.db' por si la clave 'database_name' no existiera.
DATABASE_NAME = _config_data.get("database_name", "tasks.db")

# Configuraciones y personalización de la interfaz.
_ui_config = _config_data.get("ui", {})
UI_COLORS = _ui_config.get("colors", {})
UI_ICONS = _ui_config.get("icons", {})

# Verificación de la carga de valores.
if __name__ == "__main__":
    print("--- Configuración Cargada ---")
    print(f"Nombre de la BD: {DATABASE_NAME}")

    print("\n[Colores de UI]")
    # Imprime todos los colores bajo un solo encabezado
    for color, value in UI_COLORS.items():
        print(f"  - {color}: {value}")

        print("\n[Iconos de UI]")
    # Imprime todos los íconos bajo un solo encabezado
    for icon, value in UI_ICONS.items():
        print(f"  - {icon}: {value}")
