# MODULO: controllers
# .. ....................................................... dinamic_colors ..󰌠

from rich.text import Text
from config.config_loader import UI_COLORS, UI_ICONS


# DATA:
# diccionarios contenedores de íconos y estilos.

STATUS_STYLES: dict = {
    "pending": Text(UI_ICONS['pendiente'], style=UI_COLORS['red']),
    "in_progress": Text(UI_ICONS['en_proceso'], style=UI_COLORS['blue']),
    "completed": Text(UI_ICONS['completada'], style=UI_COLORS['green'])
}

PRIORITY_STYLES: dict = {
    "alta": Text(UI_ICONS['alta'], UI_COLORS['red']),
    "media": Text(UI_ICONS['media'], UI_COLORS['orange']),
    "baja": Text( UI_ICONS['baja'], UI_COLORS['green'])
}


# FUNC:
def _get_styled_text(text_key: str, style_map: dict) -> Text | str:
    """Función interna y genérica para buscar estilos."""
    return style_map.get(text_key, text_key)


# FUNC:
def get_status_style(status_texto: str) -> Text | str:
    """Devuelve el objeto Text estilizado para un status."""
    return _get_styled_text(status_texto, STATUS_STYLES)


# FUNC:
def get_priority_style(prioridad_texto: str) -> Text | str:
    """Devuelve el objeto Text estilizado para una prioridad."""
    return _get_styled_text(prioridad_texto, PRIORITY_STYLES)


# FUNC:
def dinamic_status_colors(leyenda_texto: Text) -> Text | str:
    # 2. Usamos .append() para añadir cada parte con su propio estilo.
    leyenda_texto.append("Status:    ")
    leyenda_texto.append(f"{UI_ICONS['pendiente']} pendiente", style=UI_COLORS['red'])
    leyenda_texto.append(" | ", style="dim") # El separador un poco atenuado
    leyenda_texto.append(f"{UI_ICONS['en_proceso']} en proceso", style=UI_COLORS['blue'])
    leyenda_texto.append(" | ", style="dim")
    leyenda_texto.append(f"{UI_ICONS['completada']} completada", style=UI_COLORS['green'])

    return leyenda_texto

# FUNC:
def dinamic_priority_colors(leyenda_texto: Text) -> Text | str:

    leyenda_texto.append("Prioridad: ")
    leyenda_texto.append(f"{UI_ICONS['alta']} alta", style=UI_COLORS['red'])
    leyenda_texto.append(" | ", style="dim") # El separador un poco atenuado
    leyenda_texto.append(f"{UI_ICONS['media']} media", style=UI_COLORS['orange'])
    leyenda_texto.append(" | ", style="dim")
    leyenda_texto.append(f"{UI_ICONS['baja']} baja", style=UI_COLORS['green'])

    return leyenda_texto
