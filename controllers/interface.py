# MODULO: controllers
# .. ............................................................ interface ..
"""Punto de entrada y controlador principal de la interfaz de Textual.

Este módulo define la clase `Interface`, que hereda de `textual.app.App`.
Define la composición de la UI, gestiona los eventos del usuario (bindings)
y coordina las diferentes pantallas (modales) de la aplicación.
"""
from typing import Any
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    Static
)
from .decorators import require_valid_id
from .dinamic_colors import (
    dinamic_priority_colors,
    dinamic_status_colors,
    dinamic_notes_leyend,
    get_priority_style,
    get_status_style
)
from .screens import (
    AskIdScreen,
    AddTaskScreen,
    AskTaskEdit,
    FilterTasksScreen,
    ViewDetailsScreen
)
from config.config_loader import UI_COLORS
from models.model_task import Task
from services.task_service import TaskService


class Interface(App):
    """Clase principal de la interfaz Textual para la app 'Tasks-cli' de lista
    de tareas.

    Como clase principal, se encarga de:
    - Componer la layout inicial con widgets (Header, DataTable, Footer).
    - Definir los atajos de teclado globales (BINDINGS).
    - Lanzar acciones (`action_*`) que muestran pantallas modales para la
      interacción con el usuario.
    - Recibir los resultados de las pantallas modales y ejecutar la lógica
      de negocio correspondiente a través de `TaskService`.
    """

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
    CSS_PATH = "../config/styles.css"
    TITLE = "TASKS CLI - Lista de Tareas  "


    def compose(self) -> ComposeResult:
        """Compone el layout inicial de la aplicación.

        Este método de Textual se llama una vez al iniciar la app para
        renderizar los widgets estáticos como el Header, Footer y DataTable.
        """
        leyenda_texto_status = Text()
        leyenda_texto_priority = Text()
        leyenda_texto_notas = Text()
        dinamic_status_colors(leyenda_texto_status)
        dinamic_priority_colors(leyenda_texto_priority)
        dinamic_notes_leyend(leyenda_texto_notas)
        yield Header()
        yield Static(leyenda_texto_status, id="leyenda")
        yield Static(leyenda_texto_priority, id="prioridad")
        yield Static(leyenda_texto_notas, id="notas")
        yield DataTable()
        yield Footer()


    def _update_table(self) -> None:
        """Refresca el contenido del widget DataTable.

        El método se encarga de limpiar la tabla, obtener la lista
        actualizada de tareas desde el `TaskService`, aplicar estilos dinámicos
        y volver a poblar las filas.
        """
        table = self.query_one(DataTable)
        service = TaskService()
        table.clear()
        tareas = service.get_tasks_for_ui()

        for row_data in tareas[1:]:
            styled_row = list(row_data)
            status_texto = styled_row[1]
            prioridad_texto = styled_row[4]
            styled_status = get_status_style(status_texto)
            if isinstance(styled_status, Text):
                styled_status.justify = "center"
            styled_priority = get_priority_style(prioridad_texto)
            if isinstance(styled_priority, Text):
                styled_priority.justify = "center"
            notes_indicator = Text(
                styled_row[5], 
                justify="center", 
                style=UI_COLORS['green']
            )
            styled_row[1] = styled_status
            styled_row[4] = styled_priority
            styled_row[5] = notes_indicator
            table.add_row(*styled_row)


    def on_mount(self) -> None:
        """Se ejecuta cuando la app se monta en el DOM.

        Este método de Textual se usa para realizar configuraciones iniciales,
        como definir las cabeceras de la tabla y cargar los datos por primera vez.
        """
        table = self.query_one(DataTable)
        table.cursor_type = "row"
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


    # .. ................... Acciones y Notificaciones .................... ..󰌠
    # Sección con la lógica necesaria para las funciones de la app.

    # .. ............................................................. add_task
    def action_add_task(self) -> None:
        """Maneja el atajo de teclado 'n' para añadir una nueva tarea.

        Esta acción abre la pantalla modal `AddTaskScreen` y le asigna el método
        `notification_add_task` como callback para procesar el resultado.
        """
        self.push_screen(
            AddTaskScreen(),
            self.notification_add_task
        )

    def notification_add_task(self, new_task_data: dict | None) -> None:
        """Callback que procesa los datos recibidos de `AddTaskScreen`.

        Este método es llamado por Textual cuando la pantalla `AddTaskScreen`
        se cierra.
        Valida los datos, utiliza `TaskService` para crear la tarea y actualiza
        la tabla visual.

        Args:
            - new_task_data (dict | None): Diccionario con los datos de la
              tarea enviado desde el modal. Es `None` si el usuario canceló la
              operación.
        """
        if new_task_data:
            if not new_task_data["content"]:
                self.app.notify(
                    "El contenido no puede estar vacío.",
                    title="Error",
                    severity="error"
                )
                return
            service = TaskService()
            service.new_task_service(Task(**new_task_data))
            self.app.notify(
                f"Tarea '{new_task_data['content']}' agregada.",
                title="Nueva Tarea"
            )
            self._update_table()


    # .. ................................................ check_or_uncheck_task
    def action_check_or_uncheck_task(self) -> None:
        """Maneja el atajo 'm' para marcar/desmarcar una tarea (cambiar status)

        Abre la pantalla modal `AskIdScreen` para solicitar el ID de la tarea
        y asigna `notification_check_or_uncheck_task` como callback.
        """
        self.push_screen(
            AskIdScreen(),
            self.notification_check_or_uncheck_task
        )

    @require_valid_id
    def notification_check_or_uncheck_task(self, task_id: int) -> None:
        """Callback que cambia el estado de la tarea.

        Es llamado por Textual al cerrar `AskIdScreen`. Utiliza `TaskService`
        para cambiar el estado de la tarea y refresca la tabla.

        Args:
            - task_id (int): ID de la tarea a modificar, validado por el
              decorador `@require_valid_id`.
        """
        service = TaskService()
        service.check_or_uncheck_task_service(task_id)
        self.app.notify(
            f"Tarea ID: {task_id} ha cambiado de estado.",
            title="Status Actualizado"
        )
        self._update_table()


    # .. .......................................................... delete_task
    def action_delete_task(self) -> None:
        """Maneja el atajo 'd' para eliminar una tarea.

        Abre la pantalla modal `AskIdScreen` para solicitar el ID y asigna
        `notification_delete_task` como callback.
        """
        self.push_screen(AskIdScreen(), self.notification_delete_task)

    @require_valid_id
    def notification_delete_task(self, task_id: int) -> None:
        """Callback que elimina la tarea especificada.

        Es llamado por Textual al cerrar `AskIdScreen`. Emplea `TaskService`
        para eliminar la tarea y actualiza la tabla.

        Args:
             - task_id (int): ID de la tarea a eliminar, validado por el
               decorador `@require_valid_id`.
        """
        service = TaskService()
        service.delete_task_service(task_id)
        self.app.notify(
            f"Tarea ID: {task_id} Eliminada.", 
            title="Tarea Eliminada", 
            severity="warning"
        )
        self._update_table()


    # .. ......................................................... filter_tasks
    def action_filter_tasks(self) -> None:
        """Maneja el atajo 'f' para filtrar tareas.

        Abre la pantalla modal `FilterTasksScreen` y asigna
        `notification_filter_tasks` como callback.
        """
        self.push_screen(
            FilterTasksScreen(), 
            self.notification_filter_tasks
        )

    def notification_filter_tasks(self, filter_data: dict | None) -> None:
        """Callback que recibe los criterios de filtro y actualiza la tabla.

        Limpia y estandariza los datos del filtro, llama al servicio para
        obtener las tareas filtradas y actualiza el `DataTable` con los
        resultados.

        Args:
            - filter_data (dict | None): Diccionario con los filtros a aplicar.
              Ej: `{'status': 'pending', 'priority': 'alta'}`.
              Es `None` si el usuario canceló la pantalla de filtros.
        """
        if filter_data:
            # 1. formato para el diccionario: si un valor está vacío se
            # convierte a None para que el servicio no lo use como filtro.
            filters = {
                key: value if value else None
                for key, value in filter_data.items()
            }

            # 2. Llamada al servicio con los filtros desempaquetados.
            service = TaskService()
            filtered_tasks_objects = service.filter_tasks_service(**filters)

            # 3. Formateo de los resultados para la tabla
            # (incluyendo cabeceras).
            headers = ("ID", "Status", "Tag", "Contenido", "Prioridad")
            results_for_ui: list[Any] = [headers]
            for task in filtered_tasks_objects:
                results_for_ui.append(
                    (task.id,
                     task.status,
                     task.tag,
                     task.content,
                     task.priority
                     )
                )

            # 4. Actualización de la tabla con los datos filtrados.
            table = self.query_one(DataTable)
            # Limpia las filas anteriores.
            table.clear()

            # Añadimos solo las filas filtradas
            for row_data in results_for_ui[1:]:
                styled_row = list(row_data)
                status_texto = styled_row[1]
                prioridad_texto = styled_row[4]
                styled_status = get_status_style(status_texto)
                if isinstance(styled_status, Text):
                    styled_status.justify = "center"
                styled_priority = get_priority_style(prioridad_texto)
                if isinstance(styled_priority, Text):
                    styled_priority.justify = "center"
                styled_row[1] = styled_status
                styled_row[4] = styled_priority
                table.add_row(*styled_row)

            self.app.notify(
                f"Mostrando {len(filtered_tasks_objects)} tareas filtradas."
            )


    # .. ............................................................ edit_task
    def action_edit_task(self) -> None:
        """Maneja el atajo 'e' para iniciar la edición de una tarea.

        Abre `AskIdScreen` para obtener el ID de la tarea a editar y asigna
        `_start_edit_process` como callback.
        """
        self.push_screen(
            AskIdScreen(),
            self._start_edit_process
        )

    @require_valid_id
    def _start_edit_process(self, task_id: int) -> None:
        """Callback que obtiene la tarea y muestra la pantalla de edición.

        Es llamado al cerrar `AskIdScreen`. Obtiene el objeto de la tarea
        y abre la pantalla `AskTaskEdit`, pasándole la tarea y asignando
        `_save_edit_changes` como el siguiente callback.

        Args:
            - task_id (int): ID de la tarea a editar, validado por
              `@require_valid_id`.
        """
        service = TaskService()
        task_to_edit = service.get_task_by_id_service(task_id)
        if task_to_edit:
            self.push_screen(
                AskTaskEdit(task_to_edit),
                self._save_edit_changes
            )

    def _save_edit_changes(self, updated_data: dict | None) -> None:
        """Callback final que guarda los cambios de la edición.

        Es llamado al cerrar `AskTaskEdit`. Si hay datos, extrae el ID,
        llama al servicio para actualizar la tarea y refresca la tabla.

        Args:
            - updated_data (dict | None): Diccionario con datos actualizados.
              Contiene un campo 'id' y los demás campos modificados. Es `None`
              si el usuario canceló la edición.
        """
        if updated_data:
            task_id = updated_data.pop("id")
            new_data = updated_data
            service = TaskService()
            service.update_task_service(task_id, new_data)
            self.app.notify(
                f"Tarea ID: '{task_id}' ha sido actualizada.",
                title="Tarea Editada"
            )
            self._update_table()


    # .. ......................................................... view_details
    def action_view_details(self) -> None:
        """Maneja el atajo 'v' para ver los detalles de una tarea.

        Abre `AskIdScreen` para obtener el ID y asigna `_show_details_screen`
        como callback.
        """
        self.push_screen(
            AskIdScreen(),
            self._show_details_screen
        )


    @require_valid_id
    def _show_details_screen(self, task_id: int) -> None:
        """Callback que obtiene la tarea y muestra la pantalla de detalles.

        Es llamado al cerrar `AskIdScreen`. Obtiene la tarea completa y
        muestra la pantalla `ViewDetailsScreen` con su contenido.

        Args:
            - task_id (int): ID de la tarea a consultar, validado por
              `@require_valid_id`.
        """
        service = TaskService()
        task = service.get_task_by_id_service(task_id)

        # Comprobación de que la tarea y sus atributos requeridos no son nulos.
        if task and task.id is not None and task.details is not None:
            # Mostrar la pantalla de detalles con la tarea extraída.
            self.push_screen(
                ViewDetailsScreen(
                    details_content=task.details,
                    task_id=task.id
                )
            )


    # .. ........................................................ reset_filters
    def action_reset_filters(self) -> None:
        """Maneja el atajo 'r' para limpiar filtros y refrescar la tabla.

        Llama directamente a `_update_table()` para recargar la lista
        completa de tareas.
        """
        self._update_table()
        self.app.notify(
            "Filtros limpiados. Mostrando todas las tareas."
        )
