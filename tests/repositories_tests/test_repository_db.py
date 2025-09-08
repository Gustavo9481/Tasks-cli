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
    # 01
    Path(db_path).unlink(missing_ok=True)
    repo = RepositoryDB(db_name=db_path)

    repo.create_table()
    # 02
    yield repo
    # 03
    Path(db_path).unlink(missing_ok=True)

    # 01: Asegurarse de que no haya una base de datos de prueba antigua
    # 02: Entregar la instancia al test
    # 03: Limpiar base de datos después del test


# TEST: 01
def test_create_table(test_repo: RepositoryDB) -> None:
    """
    Comprueba la correcta creación de la tabla 'tasks_table'.

    Este test verifica que el método create_table() realmente crea la tabla
    en la base de datos. Se conecta directamente a la base de datos para
    inspeccionar su esquema y confirmar la existencia de la tabla.
    """
    # 01
    db_connection = sqlite3.connect(test_repo.db_path)
    cursor = db_connection.cursor()

    test_repo.create_table()

    # Consulta para verificar la existencia de la tabla.
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name='tasks_table';
    """)
    # 02
    result = cursor.fetchone()

    db_connection.close()
    # 03
    assert result is not None
    # 04
    assert result[0] == "tasks_table"

    # 01: conectar a la base de datos del fixture.
    # 02: se almacena el resultado de la consulta en 'result'.
    # 03: la tabla debe existir, por lo que el resultado NO debe ser None.
    # 04: el nombre de la tabla debe ser 'tasks_table'.


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

    # 01
    cursor.execute("""
            SELECT status, tag, content, priority, details
            FROM tasks_table;
    """)

    inserted_row = cursor.fetchone()
    db_connection.close()
    # 02
    assert inserted_row is not None
    # 03
    assert inserted_row[0] == task_to_insert.status
    assert inserted_row[1] == task_to_insert.tag
    assert inserted_row[2] == task_to_insert.content
    assert inserted_row[3] == task_to_insert.priority
    assert inserted_row[4] == task_to_insert.details

    # 01: consulta para extraer la única línea que debe existir en la tabla.
    # 02: verifica si inserted_row no está vacía, NO debe ser 'None'.
    # 03: se verifican el orden y los valores de inserted_row contra
    #     task_to_insert


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

    # 01
    filtered_tasks = test_repo.filter_task_status(status="completed")
    # 02
    assert len(filtered_tasks) == 2
    # 03
    for task in filtered_tasks:
        assert task.status == "completed"
    # 04
    contents = {task.content for task in filtered_tasks}
    assert "Tarea completada 1" in contents
    assert "Tarea completada 2" in contents

    # 01: Aplicación del método de consulta filter_task_status.
    # 02: Verificación de que se han filtrado 2 tareas de forma correcta.
    # 03: Verificación del status correcto en cada tarea filtrada.
    # 04: Verificación del content correcto en cada tarea filtrada.


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

    # 01
    filtered_tasks = test_repo.filter_task_tag(tag="proyecto")
    # 02
    assert len(filtered_tasks) == 2
    # 03
    for task in filtered_tasks:
        assert task.tag == "proyecto"
    # 04
    contents = {task.content for task in filtered_tasks}
    assert "Tarea proyecto 1" in contents
    assert "Tarea proyecto 2" in contents

    # 01: Aplicación del método de consulta filter_task_tag.
    # 02: Verificación de que se han filtrado 2 tareas de forma correcta.
    # 03: Verificación del tag correcto en cada tarea filtrada.
    # 04: Verificación del content correcto en cada tarea filtrada.


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

    # 01
    filtered_tasks = test_repo.filter_task_priority(priority="alta")
    # 02
    assert len(filtered_tasks) == 2
    # 03
    for task in filtered_tasks:
        assert task.priority == "alta"
    # 04
    contents = {task.content for task in filtered_tasks}
    assert "Tarea Alta 1" in contents
    assert "Tarea Alta 2" in contents

    # 01: Aplicación del método de consulta filter_task_priority.
    # 02: Verificación de que se han filtrado 2 tareas de forma correcta.
    # 03: Verificación de la prioridad correcto en cada tarea filtrada.
    # 04: Verificación del content correcto en cada tarea filtrada.


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
    # 01
    task_id = test_repo.new_task(original_task)
    assert task_id is not None

    # 02
    new_data = {
        "content": "Contenido actualizado de la tarea",
        "priority": "alta",
        "details": "Nuevos detalles extensos para la tarea actualizada.",
    }
    # 03
    test_repo.update_task(task_id, new_data)
    # 04
    updated_task = test_repo.get_task_by_id(task_id)

    # 05
    assert updated_task is not None
    assert updated_task.id == task_id
    assert updated_task.content == new_data["content"]
    assert updated_task.priority == new_data["priority"]
    assert updated_task.details == new_data["details"]
    assert updated_task.status == original_task.status  # Status no actualizado.
    assert updated_task.tag == original_task.tag  # Tag no actualizado.

    # 01: Inserción de la tarea y obtención de su id.
    # 02: Creación de la nueva tarea, con los cambios en propiedades
    #     específicas.
    # 03: Ejecución del método updated_task, usando los nuevos valores y el id
    #     de la tarea original para que Consulta actualizada.
    # 04: Se recupera la tarea actualizada.
    # 05: Verificación de los datos, tanto los que deben actializarse como los
    #     que deben mantenerse.


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

    # 01
    test_repo.check_or_uncheck_task(task_id)
    # 02
    updated_task = test_repo.get_task_by_id(task_id)
    # 03
    assert updated_task is not None
    assert updated_task.id == task_id
    assert updated_task.status == "in_progress"  # Debería haber cambiado a 'completed'

    # 04
    test_repo.check_or_uncheck_task(task_id)
    # 05
    re_updated_task = test_repo.get_task_by_id(task_id)
    assert re_updated_task is not None
    assert re_updated_task.id == task_id
    assert re_updated_task.status == "completed"

    # 01: Ejecución del método check_or_uncheck_task (pending -> completed).
    # 02: Obtención de la tarea modificada.
    # 03: Verificación de que el status sea el correcto (completed).
    # 04: Ejecución del método check_or_uncheck_task nuevamente para segunda
    #     comprobación (completed -> pending).
    # 05: Verificación de que el status haya cambiado nuevamente a pending.


# TEST: 08
def test_delete_task(test_repo: RepositoryDB) -> None:
    """
    Comprueba que el método delete_task elimina correctamente una tarea
    de la base de datos.
    """
    # 01
    task_to_delete = Task(content="Tarea para eliminar", priority="baja")
    task_id = test_repo.new_task(task_to_delete)
    # 02
    assert task_id is not None
    # 03
    test_repo.delete_task(task_id)
    # 04
    deleted_task = test_repo.get_task_by_id(task_id)
    # 05
    assert deleted_task is None

    # 01: Se crea una tarea provisoria para eliminarla luego.
    # 02: Verificación de que se haya insertado la tarea provisoria.
    # 03: Se elimina la tarea usando delete_task.
    # 04: Se intenta recuperar la tarea eliminada.
    # 05: Comprobación de la eliminación de la tarea, se espera None.
