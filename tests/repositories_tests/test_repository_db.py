# MODULO: tests/
# .. ......................... test_repository_db ......................... ..󰌠
"""
Pruebas unitarias para el módlo repositories/repository_db.py.
"""
import pytest
import sqlite3
from typing import Iterator
from pathlib import Path
from models.model_task import Task
from repositories.repository_db import RepositoryDB


@pytest.fixture
def test_repo() -> Iterator[RepositoryDB]:
    """Pytest fixture para configurar y limpiar la base de datos de prueba.

    Crea una instancia de RepositoryDB con una base de datos de prueba en
    memoria y la limpia después de que el test se completa.

    Yields:
        - Iterator[RepositoryDB]: Una instancia de RepositoryDB conectada a la 
          base de datos de prueba.
    """
    db_path: str = "tasks_tests.db"
    # Asegurarse de que no haya una base de datos de prueba antigua
    Path(db_path).unlink(missing_ok=True)
    repo = RepositoryDB(db_name=db_path)

    repo.create_table()
    # Entregar la instancia al test
    yield repo
    # Limpiar base de datos después del test
    Path(db_path).unlink(missing_ok=True)


# TEST: 01
def test_create_table(test_repo: RepositoryDB) -> None:
    """
    Comprueba la correcta creación de la tabla 'tasks_table'.

    Este test verifica que el método create_table() realmente crea la tabla
    en la base de datos. Se conecta directamente a la base de datos para
    inspeccionar su esquema y confirmar la existencia de la tabla.
    """
    # Conectar a la base de datos del fixture.
    db_connection = sqlite3.connect(test_repo.db_path)
    cursor = db_connection.cursor()

    test_repo.create_table()

    # Consulta para verificar la existencia de la tabla.
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name='tasks_table';
    """)
    # Se almacena el resultado de la consulta en 'result'.
    result = cursor.fetchone()

    db_connection.close()
    # La tabla debe existir, por lo que el resultado NO debe ser None.
    assert result is not None
    # El nombre de la tabla debe ser 'tasks_table'.
    assert result[0] == "tasks_table"


# TEST: 02
def test_new_task(test_repo: RepositoryDB) -> None:
    """Verifica el funcionamiento del método new_task para crear nuevas tareas.

    Este test verifica que el método new_task() inserta una fila en
    'tasks_table' y que los datos de esa fila (status, tag, content, priority)
    coinciden exactamente con los datos del objeto Task proporcionado.
    """
    task_to_insert = Task(
        tag="personal",
        content="Contenido test_new_task ->",
        priority="alta",
        details="Detalles de prueba: test_new_task",
    )

    test_repo.new_task(task_instance=task_to_insert)

    db_connection = sqlite3.connect(test_repo.db_path)
    cursor = db_connection.cursor()

    # Consulta para extraer la única línea que debe existir en la tabla.
    cursor.execute("""
            SELECT status, tag, content, priority, details
            FROM tasks_table;
    """)

    inserted_row = cursor.fetchone()
    db_connection.close()
    # Verifica si inserted_row no está vacía, NO debe ser 'None'.
    assert inserted_row is not None
    # Se verifican el orden y los valores de inserted_row contra task_to_insert
    assert inserted_row[0] == task_to_insert.status
    assert inserted_row[1] == task_to_insert.tag
    assert inserted_row[2] == task_to_insert.content
    assert inserted_row[3] == task_to_insert.priority
    assert inserted_row[4] == task_to_insert.details


# TEST: 03
def test_filter_task_by_status(test_repo: RepositoryDB) -> None:
    """Verifica el funcionamiento del método filter_task_status empleado para
    filtrar tareas por status.

    El tests crea 4 nuevas tareas, dos de ellas con los status de interes, para
    ser filtradas y comprobar el funcionamiento del método.
    """
    test_repo.new_task(Task(content="Tarea pendiente", status="pending"))
    test_repo.new_task(Task(content="Tarea completada 1", status="completed"))
    test_repo.new_task(Task(content="Tarea pendiente", status="pending"))
    test_repo.new_task(Task(content="Tarea completada 2", status="completed"))

    # Aplicación del método de consulta filter_task_status.
    filtered_tasks = test_repo.filter_tasks(status="completed")
    # Verificación de que se han filtrado 2 tareas de forma correcta.
    assert len(filtered_tasks) == 2
    # Verificación del status correcto en cada tarea filtrada.
    for task in filtered_tasks:
        assert task.status == "completed"
    # Verificación del content correcto en cada tarea filtrada.
    contents = {task.content for task in filtered_tasks}
    assert "Tarea completada 1" in contents
    assert "Tarea completada 2" in contents


# TEST: 04
def test_filter_task_by_tag(test_repo: RepositoryDB) -> None:
    """Verifica el funcionamiento del método filter_task_tag empleado para
    filtrar tareas por tag (etiqueta).

    El tests crea 4 nuevas tareas, dos de ellas con el tag de interes:
    (proyecto) para ser filtradas y comprobar el funcionamiento del método.
    """
    test_repo.new_task(Task(content="Tarea trabajo", tag="trabajo"))
    test_repo.new_task(Task(content="Tarea proyecto 1", tag="proyecto"))
    test_repo.new_task(Task(content="Tarea trabajo", tag="trabajo"))
    test_repo.new_task(Task(content="Tarea proyecto 2", tag="proyecto"))

    # Aplicación del método de consulta filter_task_tag.
    filtered_tasks = test_repo.filter_tasks(tag="proyecto")
    # Verificación de que se han filtrado 2 tareas de forma correcta.
    assert len(filtered_tasks) == 2
    # Verificación del tag correcto en cada tarea filtrada.
    for task in filtered_tasks:
        assert task.tag == "proyecto"
    # Verificación del content correcto en cada tarea filtrada.
    contents = {task.content for task in filtered_tasks}
    assert "Tarea proyecto 1" in contents
    assert "Tarea proyecto 2" in contents


# TEST: 05
def test_filter_task_by_priority(test_repo: RepositoryDB) -> None:
    """Verifica el funcionamiento del método filter_task_priority empleado para
    filtrar tareas por prioridad.

    El tests crea 4 nuevas tareas, dos de ellas con la prioridad de interes:
    (alta) para ser filtradas y comprobar el funcionamiento del método.
    """
    test_repo.new_task(Task(content="Tarea Alta 1", priority="alta"))
    test_repo.new_task(Task(content="Tarea Media 1", priority="media"))
    test_repo.new_task(Task(content="Tarea Alta 2", priority="alta"))
    test_repo.new_task(Task(content="Tarea Baja 1", priority="baja"))

    # Aplicación del método de consulta filter_task_priority.
    filtered_tasks = test_repo.filter_tasks(priority="alta")
    # Verificación de que se han filtrado 2 tareas de forma correcta.
    assert len(filtered_tasks) == 2
    # Verificación de la prioridad correcto en cada tarea filtrada.
    for task in filtered_tasks:
        assert task.priority == "alta"
    # Verificación del content correcto en cada tarea filtrada.
    contents = {task.content for task in filtered_tasks}
    assert "Tarea Alta 1" in contents
    assert "Tarea Alta 2" in contents


# TEST: 06
def test_update_task(test_repo: RepositoryDB) -> None:
    """Comprueba la correcta actualización de los campos de una tarea,
    incluyendo el campo 'details'.

    El test creará una tarea inicial 'original_task' para luego ser actualizada
    con nuevos valores, comprobando el funcionamiento del método.
    """
    original_task = Task(
        content="Tarea para actualizar",
        tag="personal",
        priority="baja",
        details="Detalles originales de la tarea.",
    )
    # Inserción de la tarea y obtención de su id.
    task_id = test_repo.new_task(original_task)
    assert task_id is not None

    # Creación de la nueva tarea, con los cambios en propiedades específicas.
    new_data = {
        "content": "Contenido actualizado de la tarea",
        "priority": "alta",
        "details": "Nuevos detalles extensos para la tarea actualizada.",
    }
    # Ejecución del método updated_task, usando los nuevos valores y el id de
    # la tarea original para que Consulta actualizada.
    test_repo.update_task(task_id, new_data)
    # Se recupera la tarea actualizada.
    updated_task = test_repo.get_task_by_id(task_id)

    # Verificación de los datos, tanto los que deben actializarse como los que
    # deben mantenerse.
    assert updated_task is not None
    assert updated_task.id == task_id
    assert updated_task.content == new_data["content"]
    assert updated_task.priority == new_data["priority"]
    assert updated_task.details == new_data["details"]
    assert updated_task.status == original_task.status  # Status no actualizado.
    assert updated_task.tag == original_task.tag  # Tag no actualizado.


# TEST: 07
def test_check_or_uncheck_task(test_repo: RepositoryDB) -> None:
    """
    Comprueba que el método check_or_uncheck_task alterna correctamente
    el estado de una tarea entre 'pending' y 'completed'.

    El test usa una tarea apara realizar dos operaciones:
        - de pending -> completed.
        - de completed -> pending.
    """
    initial_task = Task(content="Tarea para marcar/desmarcar", status="pending")
    task_id = test_repo.new_task(initial_task)
    assert task_id is not None

    # Ejecución del método check_or_uncheck_task (pending -> completed).
    test_repo.check_or_uncheck_task(task_id)
    # Obtención de la tarea modificada.
    updated_task = test_repo.get_task_by_id(task_id)
    # Verificación de que el status sea el correcto (completed).
    assert updated_task is not None
    assert updated_task.id == task_id
    # Debería haber cambiado a 'completed'
    assert updated_task.status == "in_progress"

    # Ejecución del método check_or_uncheck_task nuevamente para segunda
    # comprobación (completed -> pending).
    test_repo.check_or_uncheck_task(task_id)
    # Verificación de que el status haya cambiado nuevamente a pending.
    re_updated_task = test_repo.get_task_by_id(task_id)
    assert re_updated_task is not None
    assert re_updated_task.id == task_id
    assert re_updated_task.status == "completed"


# TEST: 08
def test_delete_task(test_repo: RepositoryDB) -> None:
    """
    Comprueba que el método delete_task elimina correctamente una tarea
    de la base de datos.
    """
    # Se crea una tarea provisoria para eliminarla luego.
    task_to_delete = Task(content="Tarea para eliminar", priority="baja")
    task_id = test_repo.new_task(task_to_delete)
    # Verificación de que se haya insertado la tarea provisoria.
    assert task_id is not None
    # Se elimina la tarea usando delete_task.
    test_repo.delete_task(task_id)
    # Se intenta recuperar la tarea eliminada.
    deleted_task = test_repo.get_task_by_id(task_id)
    # Comprobación de la eliminación de la tarea, se espera None.
    assert deleted_task is None
