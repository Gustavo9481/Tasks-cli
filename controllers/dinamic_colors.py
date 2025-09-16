# MODULO: controllers
# .. ....................................................... dinamic_colors ..󰌠
"""
Módulo para gestionar y proveer estilos dinámicos para la interfaz.

Este módulo centraliza la creación de objetos `Text` de la librería Rich,
combinando los íconos colores definidos en la configuración para representar
visualmente diferentes estados de la aplicación (status, prioridad, etc.).
"""
# OK:

from rich.text import Text
from config.config_loader import UI_COLORS, UI_ICONS


# Diccionario que mapea el estado de una tarea a un objeto Text estilizado.
STATUS_STYLES: dict[str, Text] = {
    "pending": Text(UI_ICONS.get('pendiente', ' '), style=UI_COLORS.get('red')),
    "in_progress": Text(UI_ICONS.get('en_proceso', ' '), style=UI_COLORS.get('blue')),
    "completed": Text(UI_ICONS.get('completada', ' '), style=UI_COLORS.get('green'))
}

# Diccionario que mapea la prioridad de una tarea a un objeto Text estilizado.
PRIORITY_STYLES: dict[str, Text] = {
    "alta": Text(UI_ICONS.get('alta', ' '), style=UI_COLORS.get('red')),
    "media": Text(UI_ICONS.get('media', ' '), style=UI_COLORS.get('orange')),
    "baja": Text(UI_ICONS.get('baja', ' '), style=UI_COLORS.get('green'))
}

# Estilo para el ícono de nota.
NOTE_STYLE: Text = Text(
    UI_ICONS.get('nota', '>'), style=UI_COLORS.get('green')
)


def _get_styled_text(text_key: str, style_map: dict[str, Text]) -> Text | str:
    """Función interna para buscar un estilo en un mapa de estilos.

    Args:
        text_key: La clave que identifica el estilo a buscar (ej. "pending").
        style_map: El diccionario donde se buscará el estilo.

    Returns:
        El objeto Text estilizado si se encuentra la clave, o la clave
        original como texto plano si no se encuentra.
    """
    return style_map.get(text_key, text_key)


def get_status_style(status_text: str) -> Text | str:
    """Devuelve un objeto Text estilizado para un estado de tarea.

    Args:
        status_text: El texto del estado a estilizar (ej. "completed").

    Returns:
        Un objeto Text con el ícono y color correspondientes.
    """
    return _get_styled_text(status_text, STATUS_STYLES)


def get_priority_style(priority_text: str) -> Text | str:
    """Devuelve un objeto Text estilizado para una prioridad de tarea.

    Args:
        priority_text: El texto de la prioridad a estilizar (ej. "alta").

    Returns:
        Un objeto Text con el ícono y color correspondientes.
    """
    return _get_styled_text(priority_text, PRIORITY_STYLES)


def dinamic_status_colors(legend_text: Text) -> Text:
    """Construye y añade una leyenda de estados a un objeto Text.

    Esta función modifica el objeto `legend_text` que se le pasa.

    Args:
        legend_text: El objeto Text al que se le añadirá la leyenda.

    Returns:
        El mismo objeto Text modificado con la leyenda de estados.
    """
    legend_text.append("Status:    ")
    legend_text.append(
        f"{UI_ICONS.get('pendiente', ' ')} pendiente",
        style=UI_COLORS.get('red')
    )
    legend_text.append(" | ", style="dim")
    legend_text.append(
        f"{UI_ICONS.get('en_proceso', ' ')} en proceso",
        style=UI_COLORS.get('blue')
    )
    legend_text.append(" | ", style="dim")
    legend_text.append(
        f"{UI_ICONS.get('completada', ' ')} completada",
        style=UI_COLORS.get('green')
    )

    return legend_text


def dinamic_priority_colors(legend_text: Text) -> Text:
    """Construye y añade una leyenda de prioridades a un objeto Text.

    Esta función modifica el objeto `legend_text` que se le pasa.

    Args:
        legend_text: El objeto Text al que se le añadirá la leyenda.

    Returns:
        El mismo objeto Text modificado con la leyenda de prioridades.
    """
    legend_text.append("Prioridad: ")
    legend_text.append(
        f"{UI_ICONS.get('alta', ' ')} alta",
        style=UI_COLORS.get('red')
    )
    legend_text.append(" | ", style="dim")
    legend_text.append(
        f"{UI_ICONS.get('media', ' ')} media",
        style=UI_COLORS.get('orange')
    )
    legend_text.append(" | ", style="dim")
    legend_text.append(
        f"{UI_ICONS.get('baja', ' ')} baja",
        style=UI_COLORS.get('green')
    )

    return legend_text


def dinamic_notes_leyend(legend_text: Text) -> Text:
    """Construye y añade una leyenda sobre notas a un objeto Text.

    Nota: Esta función modifica el objeto `legend_text` que se le pasa.

    Args:
        legend_text: El objeto Text al que se le añadirá la leyenda.

    Returns:
        El mismo objeto Text modificado con la leyenda de notas.
    """
    legend_text.append("Notas:     ")
    legend_text.append(
        f"{UI_ICONS.get('nota', '>')}",
        style=UI_COLORS.get('green')
    )
    legend_text.append(" -> Presiona 'v' para ver detalles.")

    return legend_text
