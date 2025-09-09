# MODULO: controllers
# .. ............................................................ interface ..
"""
Gestor de interface. Contiene la clase Interface quecrea la interfaz usando la
herramienta 'textual' para la terminal.
"""
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import (Button, DataTable, Footer, Header, Input, Label,
                           Static)

from decorators import require_valid_id
from dinamic_colors import (dinamic_priority_colors, dinamic_status_colors,
                            get_priority_style, get_status_style)
from models.model_task import Task
from services.task_service import TaskService
from screens import AskIdScreen, AddTaskScreen, AskTaskEdit



class Interface(App):
    """Una app de Textual que muestra una tabla con estilos dinámicos."""
    BINDINGS = [
        ("q", "quit", "Salir"),
        ("n", "add_task", "Nueva Tarea"),
        ("e", "edit_task", "Editar Tarea"),
        ("d", "delete_task", "Eliminar Tarea"),
        ("m", "check_or_uncheck_task", "Marcar/Desmarcar"),
    ]
    CSS_PATH = "styles.css"
    TITLE = "TASKS CLI - Tabla de Tareas"

    def compose(self) -> ComposeResult:
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
        """Limpia y vuelve a cargar la tabla de tareas con datos frescos."""
        table = self.query_one(DataTable)
        service = TaskService()
        table.clear()
        tareas = service.get_tasks_for_ui()
        for row_data in tareas[1:]:
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
        """Configura la tabla al iniciar la app."""
        table = self.query_one(DataTable)
        headers = ("ID", "Status", "Tag", "Contenido", "Prioridad")
        for label in headers:
            if label == "Contenido":
                table.add_column(label, width=100)
            elif label == "Tag":
                table.add_column(label, width=20)
            else:
                table.add_column(label)
        self._update_table()

    # --- Lógica de Acciones ---

    def action_add_task(self) -> None:
        """Muestra la pantalla modal para añadir una nueva tarea."""
        self.push_screen(AddTaskScreen(), self.notification_add_task)

    def notification_add_task(self, new_task_data: dict | None) -> None:
        """Crea la nueva tarea después de recibir los datos del modal."""
        if new_task_data:
            if not new_task_data["content"]:
                self.app.notify("El contenido no puede estar vacío.", title="Error", severity="error")
                return
            service = TaskService()
            service.new_task_service(Task(**new_task_data))
            self.app.notify(f"Tarea '{new_task_data['content']}' agregada.", title="Nueva Tarea")
            self._update_table()

    def action_check_or_uncheck_task(self) -> None:
        """Pide un ID para marcar/desmarcar una tarea."""
        self.push_screen(AskIdScreen(), self.notification_check_or_uncheck_task)

    @require_valid_id
    def notification_check_or_uncheck_task(self, task_id: int) -> None:
        """Cambia el estado de la tarea y refresca la tabla."""
        service = TaskService()
        service.check_or_uncheck_task_service(task_id)
        self.app.notify(f"Tarea ID: {task_id} ha cambiado de estado.", title="Status Actualizado")
        self._update_table()

    def action_delete_task(self) -> None:
        """Pide un ID para eliminar una tarea."""
        self.push_screen(AskIdScreen(), self.notification_delete_task)

    @require_valid_id
    def notification_delete_task(self, task_id: int) -> None:
        """Elimina la tarea y refresca la tabla."""
        service = TaskService()
        service.delete_task_service(task_id)
        self.app.notify(f"Tarea ID: {task_id} Eliminada.", title="Tarea Eliminada", severity="warning")
        self._update_table()

    def action_edit_task(self) -> None:
        """Pide un ID para empezar el proceso de edición."""
        self.push_screen(AskIdScreen(), self._start_edit_process)

    @require_valid_id
    def _start_edit_process(self, task_id: int) -> None:
        """Obtiene la tarea y muestra la pantalla de edición."""
        service = TaskService()
        task_to_edit = service.get_task_by_id_service(task_id)
        if task_to_edit:
            self.push_screen(AskTaskEdit(task_to_edit), self._save_edit_changes)

    def _save_edit_changes(self, updated_data: dict | None) -> None:
        """Guarda los cambios de la edición y refresca la tabla."""
        if updated_data:
            task_id = updated_data.pop("id")
            new_data = updated_data
            service = TaskService()
            service.update_task_service(task_id, new_data)
            self.app.notify(f"Tarea ID: '{task_id}' ha sido actualizada.", title="Tarea Editada")
            self._update_table()

# EXE:
if __name__ == "__main__":
    app = Interface()
    app.run()
