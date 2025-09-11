# MODULO: controllers
# .. .............................................................. screens ..󰌠
"""
Pantallas de textual específicas para solicitar datos al usuario.
"""
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Button, Input, Label, Markdown, TextArea
from textual.containers import Vertical, Horizontal
from models.model_task import Task


# CLASS:
class AskIdScreen(ModalScreen):
    """Pantalla modal para preguntar por el ID de la tarea.

    Esta pantalla es usada en las funciones de:
        - check_uncheck_task: cambiar estatus de tarea.
        - edita_task: editar tarea.
        - delete_task: eliminar tarea.
    """

    # FUNC:
    def compose(self) -> ComposeResult:
        """Crea la composición de widgets para la pantalla AskIdScreen.

        Define la estructura visual de la pantalla, que consiste
        en un contenedor vertical que alinea una etiqueta que pide el ID y un
        campo de entrada para que el usuario lo introduzca.

        Returns:
            - ComposeResult: Objeto que describe la composición de widgets que
              Textual renderizará.
        """
        with Vertical(classes="dialog"):
            yield Label("Introduce el ID de la tarea y presiona Enter:", classes="label")
            yield Input(id="id_input")


    # FUNC:
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Maneja el evento de envío de entrada del usuario.

        Este método es llamado automáticamente por Textual cuando el usuario
        presiona Enter en un widget Input dentro de esta pantalla.
        Captura el valor introducido y cierra la pantalla, pasando dicho valor
        al callback que la invocó.

        Args:
            - event (Input.Submitted): Objeto de evento que contiene la entrada
              enviada por el usuario.
        """
        self.dismiss(event.value)



# CLASS:
class AddTaskScreen(ModalScreen):
    """Pantalla modal para añadir una nueva tarea.

    Solicita al usuario todos los datos necesarios para crear una nueva tarea.
    Es un componente específico para la funcionalidad de nueva tarea.
    """

    # FUNC:
    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label("Contenido de la tarea:")
            yield Input(id="content_input", placeholder="Descripción...")
            yield Label("Tag (personal, proyecto, trabajo, calendario):")
            yield Input(id="tag_input", value="personal")
            yield Label("Prioridad (baja, media, alta):")
            yield Input(id="priority_input", value="baja")
            yield Label("Detalles (opcional):")
            yield TextArea(id="details_input", placeholder="Notas adicionales...")
            with Horizontal(classes="buttons"):
                yield Button("Crear Tarea", variant="primary", id="submit")
                yield Button("Cancelar", id="cancel")


    # FUNC:
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            new_task_data = {
                "content": self.query_one("#content_input", Input).value,
                "tag": self.query_one("#tag_input", Input).value,
                "priority": self.query_one("#priority_input", Input).value,
                "details": self.query_one("#details_input", TextArea).text,
            }
            self.dismiss(new_task_data)
        else:
            self.dismiss(None)



# CLASS:
class AskTaskEdit(ModalScreen):
    """Pantalla modal para EDITAR una tarea existente."""

    # FUNC:
    def __init__(self, task_to_edit: Task):
        super().__init__()
        self.task_to_edit = task_to_edit


    # FUNC:
    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label(f"Editando Tarea ID: {self.task_to_edit.id}")
            yield Label("Contenido de la tarea:")
            yield Input(id="content_input", value=self.task_to_edit.content)
            yield Label("Tag (personal, proyecto, trabajo, calendario):")
            yield Input(id="tag_input", value=self.task_to_edit.tag)
            yield Label("Prioridad (baja, media, alta):")
            yield Input(id="priority_input", value=self.task_to_edit.priority)
            yield Label("Detalles (opcional):")
            initial_text = self.task_to_edit.details if self.task_to_edit.details else ""
            yield TextArea(initial_text, id="details_input")

            with Horizontal(classes="buttons"):
                yield Button("Guardar Cambios", variant="primary", id="submit")
                yield Button("Cancelar", id="cancel")


    # FUNC:
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            updated_data = {
                "content": self.query_one("#content_input", Input).value,
                "tag": self.query_one("#tag_input", Input).value,
                "priority": self.query_one("#priority_input", Input).value,
                "details": self.query_one("#details_input", TextArea).text,
            }
            if self.task_to_edit:
                updated_data["id"] = self.task_to_edit.id
            self.dismiss(updated_data)
        else:
            self.dismiss(None)



# CLASS:
class FilterTasksScreen(ModalScreen):
    """Pantalla modal para filtrar tareas."""

    # FUNC:
    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label(
                "Filtrar Tareas (deja en blanco para no usar un filtro)",
                id="filter_label_1"
            )

            yield Label(
                "Filtrar por Status (pending, in_progress, completed):",
                id="filter_label_2"
            )
            yield Input(id="status_filter", placeholder="E.g., pending")

            yield Label("Filtrar por Tag:", id="filter_label_3")
            yield Input(id="tag_filter", placeholder="E.g., personal")

            yield Label("Filtrar por Prioridad (baja, media, alta):",
                        id="filter_label_4")
            yield Input(id="priority_filter", placeholder="E.g., alta")

            with Horizontal(classes="buttons"):
                yield Button("Filtrar", variant="primary", id="submit")
                yield Button("Cancelar", id="cancel")


    # FUNC:
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            # Recopilamos los criterios de filtro en un diccionario
            filter_data = {
                "status": self.query_one("#status_filter", Input).value,
                "tag": self.query_one("#tag_filter", Input).value,
                "priority": self.query_one("#priority_filter", Input).value,
            }
            # Cerramos la pantalla y pasamos los criterios
            self.dismiss(filter_data)
        else:
            self.dismiss(None)



class ViewDetailsScreen(ModalScreen):
    """Pantalla modal para mostrar los detalles de una tarea en Markdown."""

    def __init__(self, details_content: str, task_id: int):
        super().__init__()
        self.details_content = details_content
        self.task_id = task_id

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label(f"Detalles de la Tarea ID: {self.task_id}")

            # El widget de Markdown renderizará el texto.
            # Si no hay detalles, muestra un mensaje por defecto.
            markdown_text = self.details_content if self.details_content else "*No hay detalles para esta tarea.*"
            with Vertical(id="markdown_container"):
                yield Markdown(markdown_text)

            with Horizontal(classes="buttons"):
                yield Button("Cerrar", variant="primary", id="close_details")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Cierra la pantalla modal cuando se presiona el botón."""
        self.dismiss()
