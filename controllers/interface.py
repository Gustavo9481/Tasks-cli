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
from screens import AskIdScreen, AddTaskScreen, AskTaskEdit, FilterTasksScreen, ViewDetailsScreen



class Interface(App):
    """Una app de Textual que muestra una tabla con estilos dinámicos."""
    BINDINGS = [
        ("q", "quit", "Salir"),
        ("n", "add_task", "Nueva Tarea"),
        ("e", "edit_task", "Editar Tarea"),
        ("f", "filter_tasks", "Filtrar Tareas"),
        ("d", "delete_task", "Eliminar Tarea"),
        ("m", "check_or_uncheck_task", "Marcar/Desmarcar"),
        ("r", "reset_filters", "Refrescar tareas"),
        ("v", "view_details", "Ver Detalles")
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
            notes_indicator = Text(styled_row[5], justify="center")
            styled_row[1] = styled_status
            styled_row[4] = styled_priority
            styled_row[5] = notes_indicator
            table.add_row(*styled_row)

    def on_mount(self) -> None:
        """Configura la tabla al iniciar la app."""
        table = self.query_one(DataTable)
        headers = ("ID", "Status", "Tag", "Contenido", "Prioridad", "Notas")
        for label in headers:
            if label == "Contenido":
                table.add_column(label, width=90)
            elif label == "Tag":
                table.add_column(label, width=20)
            elif label == "Nota":
                table.add_column(label, width=10)
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

    # FUNC:
    def action_filter_tasks(self) -> None:
        """Filtra las tareas según los parámetros que ingrese el usuario. """
        self.push_screen(FilterTasksScreen(), self.notification_filter_tasks)


    def notification_filter_tasks(self, filter_data: dict | None) -> None:
        """
        Recibe los criterios de filtro, llama al servicio y actualiza la tabla.
        """
        if filter_data:
            # 1. Limpiamos el diccionario: si un valor está vacío, lo convertimos
            #    a None para que el servicio no lo use como filtro.
            filters = {
                key: value if value else None
                for key, value in filter_data.items()
            }

            # 2. Llamamos al servicio con los filtros desempaquetados
            service = TaskService()
            filtered_tasks_objects = service.filter_tasks_service(**filters)

            # 3. Formateamos los resultados para la tabla (incluyendo cabeceras)
            headers = ("ID", "Status", "Tag", "Contenido", "Prioridad")
            results_for_ui = [headers]
            for task in filtered_tasks_objects:
                results_for_ui.append(
                    (task.id, task.status, task.tag, task.content, task.priority)
                )

            # 4. Actualizamos la tabla con los datos filtrados
            table = self.query_one(DataTable)
            table.clear() # Limpiamos filas anteriores

            # Añadimos solo las filas filtradas
            for row_data in results_for_ui[1:]:
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

            self.app.notify(f"Mostrando {len(filtered_tasks_objects)} tareas filtradas.")



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


    # FUNC:
    def action_view_details(self) -> None:
        """Pide un ID para ver los detalles de una tarea."""
        self.push_screen(AskIdScreen(), self._show_details_screen)


    @require_valid_id
    def _show_details_screen(self, task_id: int) -> None:
        """
        Obtiene la tarea y muestra la pantalla de detalles.
        """
        # El decorador ya ha validado que el ID es un entero y existe.
        service = TaskService()
        task = service.get_task_by_id_service(task_id)

        # Aunque el decorador ya lo valida, es una buena práctica comprobar
        # que el objeto se ha recuperado correctamente.
        if task:
            # Llama a la nueva pantalla, pasándole el contenido de los detalles.
            self.push_screen(
                ViewDetailsScreen(
                    details_content=task.details,
                    task_id=task.id
                )
            )

    
    def action_reset_filters(self) -> None:
        """Limpia los filtros y muestra todas las tareas."""
        # Simplemente llamamos a nuestro método de refresco, que por
        # defecto ya carga todas las tareas.
        self._update_table()
        self.app.notify("Filtros limpiados. Mostrando todas las tareas.")



# EXE:
if __name__ == "__main__":
    app = Interface()
    app.run()
