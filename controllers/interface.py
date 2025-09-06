# MODULO: controllers
# .. ............................................................ interface ..󰌠
"""
Gestor de interface. Contiene la clase Interface quecrea la interfaz usando la
herramienta 'textual' para la terminal.
"""
from rich.text import Text
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Static, DataTable, Footer, Input, Label
from services.task_service import TaskService
from dinamic_colors import get_status_style, get_priority_style, dinamic_status_colors, dinamic_priority_colors

# --- La Pantalla Modal (sin cambios) ---
class AskIdScreen(ModalScreen):
    """Una pantalla modal para preguntar por el ID de la tarea."""
    def compose(self) -> ComposeResult:
        yield Label("Introduce el ID de la tarea y presiona Enter:", classes="label")
        yield Input(id="id_input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)


# CLASS:
class Interface(App):
    """Una app de Textual que muestra una tabla con estilos dinámicos."""
    # --- 1. DEFINIR LOS ATORNOS DE TECLADO ---
    BINDINGS = [
        ("q", "quit", "salir  "),
        ("n", "add_task", "nueva tarea   "),
        ("d", "delete_task", "borrar   "),
        ("e", "edit_task", "editar   "),
        ("s", "filtrar_status", "filtrar status   "),
        ("t", "filtrar_tag", "filtrar tag   "),
        ("p", "filtrar_prioridad", "filtrar prioridad   ")
    ]
    CSS_PATH = "styles.css"
    TITLE = "Tabla de Tareas"

    def compose(self) -> ComposeResult:

        # 1. Creamos un objeto Text base.
        leyenda_texto_status = Text()
        leyenda_texto_priority = Text()
        dinamic_status_colors(leyenda_texto_status)
        dinamic_priority_colors(leyenda_texto_priority)

        yield Header()
        yield Static(leyenda_texto_status, id="leyenda")
        yield Static(leyenda_texto_priority, id="prioridad")
        yield DataTable()
        yield Footer()

    def _update_table(self) -> None:
        """Limpia y vuelve a cargar la tabla de tareas con las actualizaciones hechas.

        Se usará éste método para refrescar las tareas en diversas funcionalidades.
        """
        table = self.query_one(DataTable)
        service = TaskService()

        table.clear()   # Limpieza de la tabla anterior.

        # carga de las tareas actualizadas.
        tareas = service.get_tasks_for_ui()

        for row_data in tareas[1:]:   # salta la cabecera de tareas.
            styled_row = list(row_data)
            status_texto = styled_row[1]
            prioridad_texto = styled_row[4]

            styled_status = get_status_style(status_texto)
            styled_status.justify = "center"

            styled_priority = get_priority_style(prioridad_texto)
            styled_priority.justify = "center"

            styled_row[1] = styled_status
            styled_row[4] = styled_priority

            table.add_row(*styled_row)



    def on_mount(self) -> None:
        """Se llama cuando la app se monta, para poblar la tabla."""
        table = self.query_one(DataTable)

        headers = ("ID", "status", "tag", "contenido", "prioridad")

        for label in headers:
            if label == "contenido":
                table.add_column(label, width=100)
            elif label == "tag":
                table.add_column(label, width=20)
            else:
                table.add_column(label)

        self._update_table()


    # FUNC: delete_task y notificación.
    def action_delete_task(self) -> None:
        """Muestra la pantalla modal para pedir el ID a eliminar. """
        self.push_screen(AskIdScreen(), self.notification_delete_task)


    def notification_delete_task(self, task_id: str) -> None:
        """Notofocación para la eliminación de tarea. """
        try:
            id_to_delete = int(task_id)   # BUG: chequear si la conversión es necesaria.
            service = TaskService()
            service.delete_task_by_id(id_to_delete)

            self.app.notify(
                f"Tarea ID: '{id_to_delete}' Eliminada",                   # 01
                title="Eliminar tarea...󰙏 ",                               # 02
                severity="error",                                          # 03
                timeout=4                                                  # 04
            )
            self._update_table()

        except ValueError:
            self.app.notify(
                f"El ID {task_id} no es un número válido.",
                title="Erroer de entrada.",
                severity="error",
                timeout=3
            )



    # FUNC: edit_task y notificación.
    def action_edit_task(self) -> None:
        self.push_screen(AskIdScreen(), self.notification_edit_task)

    def notification_edit_task(self, task_id: str) -> None:
        """Notificación para la edición de tarea. """
        if task_id:
            self.app.notify(
                f"Tarea ID: '{task_id}' Modificada",                       # 01
                title="Se han realizado los cambios...󰙏 ",                 # 02
                severity="information",                                    # 03
                timeout=4                                                  # 04
            )

        # NOTE: opciones de las notificaciones:
        # 01: Mensaje.
        # 02: Título de la notificación.
        # 03: Nivel: information, warning, error.
        # 04: Segundos antes de desaparecer.


# EXE:
if __name__ == "__main__":
    app = Interface()
    app.run()
