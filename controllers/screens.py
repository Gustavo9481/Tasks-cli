# MODULO: controllers
# .. .............................................................. screens ..󰌠
"""
Pantallas de textual específicas para solicitar datos al usuario.
"""
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Button, Input, Label
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
            yield Input(id="details_input", placeholder="Notas adicionales...")
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
                "details": self.query_one("#details_input", Input).value,
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
            yield Input(
                id="details_input",
                value=self.task_to_edit.details if self.task_to_edit.details else ""
            )
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
                "details": self.query_one("#details_input", Input).value,
            }
            if self.task_to_edit:
                updated_data["id"] = self.task_to_edit.id
            self.dismiss(updated_data)
        else:
            self.dismiss(None)
