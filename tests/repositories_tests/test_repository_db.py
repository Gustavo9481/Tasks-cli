# MODULO: tests/
# ------------- test_repository_db ------->
"""
Pruebas unitarias para el módlo repositories/repository_db.py.
"""
import pytest
import sqlite3
from pathlib import Path
from models.model_task import Task, Status, Tag, Priority
from repositories.repository_db import RepositoryDB


@pytest.fixture
def test_repo() -> RepositoryDB:
    """Pytest fixture para configurar y limpiar la base de datos de prueba.

    Crea una instancia de RepositoryDB con una base de datos de prueba en
    memoria y la limpia después de que el test se completa.

    Yields:
        - RepositoryDB: Una instancia de RepositoryDB conectada a la base de 
            datos de prueba.
    """
    db_path: str = "tasks_tests.db"
    Path(db_path).unlink(missing_ok=True)   # 01
    repo = RepositoryDB(db_name=db_path)

    repo.create_table()

    yield repo   # 02

    Path(db_path).unlink(missing_ok=True)   # 03

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
    db_connection = sqlite3.connect(test_repo.db_path)   # 01
    cursor = db_connection.cursor()

    test_repo.create_table()

    # Consulta para verificar la existencia de la tabla.
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name='tasks_table';
    """)

    result = cursor.fetchone()   # 02

    db_connection.close()

    assert result is not None   # 03

    assert result[0] == "tasks_table"   # 04

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
        details="Detalles de prueba: test_new_task"
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


    assert inserted_row is not None   # 02
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

    # Creamos un escenario con una mezcla de tareas.
    # Dos con prioridad 'alta', una 'media' y una 'baja'.
    test_repo.new_task(Task(content="Tarea pendiente", status="pending"))
    test_repo.new_task(Task(content="Tarea completada 1", status="completed"))
    test_repo.new_task(Task(content="Tarea pendiente", status="pending"))
    test_repo.new_task(Task(content="Tarea completada 2", status="completed"))


    # --- Actuar ---
    # Llamamos al método de filtrado que queremos probar.
    filtered_tasks = test_repo.filter_task_status(status="completed")

    # --- Verificar ---
    # 1. Verificamos que la cantidad de tareas devueltas sea la correcta.
    #    Deberían ser exactamente 2.
    assert len(filtered_tasks) == 2

    # 2. Verificamos que CADA tarea en la lista tenga la prioridad correcta.
    #    Esto nos asegura que el filtro no solo trae la cantidad correcta,
    #    sino también los elementos correctos.
    for task in filtered_tasks:
        assert task.status == "completed"

    # 3. (Opcional pero recomendado) Verificamos el contenido para estar
    #    100% seguros de que son las tareas que esperamos.
    contents = {task.content for task in filtered_tasks}
    assert "Tarea completada 1" in contents
    assert "Tarea completada 2" in contents


# TEST: 04
def test_filter_task_by_tag(test_repo: RepositoryDB) -> None:

    # Creamos un escenario con una mezcla de tareas.
    # Dos con prioridad 'alta', una 'media' y una 'baja'.
    test_repo.new_task(Task(content="Tarea trabajo", tag="trabajo"))
    test_repo.new_task(Task(content="Tarea proyecto 1", tag="proyecto"))
    test_repo.new_task(Task(content="Tarea trabajo", tag="trabajo"))
    test_repo.new_task(Task(content="Tarea proyecto 2", tag="proyecto"))


    # --- Actuar ---
    # Llamamos al método de filtrado que queremos probar.
    filtered_tasks = test_repo.filter_task_tag(tag="proyecto")

    # --- Verificar ---
    # 1. Verificamos que la cantidad de tareas devueltas sea la correcta.
    #    Deberían ser exactamente 2.
    assert len(filtered_tasks) == 2

    # 2. Verificamos que CADA tarea en la lista tenga la prioridad correcta.
    #    Esto nos asegura que el filtro no solo trae la cantidad correcta,
    #    sino también los elementos correctos.
    for task in filtered_tasks:
        assert task.tag == "proyecto"

    # 3. (Opcional pero recomendado) Verificamos el contenido para estar
    #    100% seguros de que son las tareas que esperamos.
    contents = {task.content for task in filtered_tasks}
    assert "Tarea proyecto 1" in contents
    assert "Tarea proyecto 2" in contents


# TEST: 05
def test_filter_task_by_priority(test_repo: RepositoryDB) -> None:

    # Creamos un escenario con una mezcla de tareas.
    # Dos con prioridad 'alta', una 'media' y una 'baja'.
    test_repo.new_task(Task(content="Tarea Alta 1", priority="alta"))
    test_repo.new_task(Task(content="Tarea Media 1", priority="media"))
    test_repo.new_task(Task(content="Tarea Alta 2", priority="alta"))
    test_repo.new_task(Task(content="Tarea Baja 1", priority="baja"))

    # --- Actuar ---
    # Llamamos al método de filtrado que queremos probar.
    filtered_tasks = test_repo.filter_task_priority(priority="alta")

    # --- Verificar ---
    # 1. Verificamos que la cantidad de tareas devueltas sea la correcta.
    #    Deberían ser exactamente 2.
    assert len(filtered_tasks) == 2

    # 2. Verificamos que CADA tarea en la lista tenga la prioridad correcta.
    #    Esto nos asegura que el filtro no solo trae la cantidad correcta,
    #    sino también los elementos correctos.
    for task in filtered_tasks:
        assert task.priority == "alta"

    # 3. (Opcional pero recomendado) Verificamos el contenido para estar
    #    100% seguros de que son las tareas que esperamos.
    contents = {task.content for task in filtered_tasks}
    assert "Tarea Alta 1" in contents
    assert "Tarea Alta 2" in contents


# TEST: 06
def test_update_task(test_repo: RepositoryDB) -> None:
    """Comprueba la correcta actualización de los campos de una tarea, 
    incluyendo el campo 'details'.
    """
    # --- Preparar ---
    # 1. Creamos una tarea inicial con algunos datos.
    original_task = Task(
        content="Tarea para actualizar",
        tag="personal",
        priority="baja",
        details="Detalles originales de la tarea."
    )
    # 2. La insertamos y obtenemos su ID.
    task_id = test_repo.new_task(original_task)
    assert task_id is not None # Aseguramos que se insertó y tiene ID

    # --- Actuar ---
    # Definimos los nuevos datos, incluyendo el campo 'details'.
    new_data = {
        "content": "Contenido actualizado de la tarea",
        "priority": "alta",
        "details": "Nuevos detalles extensos para la tarea actualizada."
    }
    test_repo.update_task(task_id, new_data)

    # --- Verificar ---
    # 1. Recuperamos la tarea actualizada de la base de datos.
    updated_task = test_repo.get_task_by_id(task_id)

    # 2. Comprobamos que la tarea existe y que los campos se actualizaron correctamente.
    assert updated_task is not None
    assert updated_task.id == task_id
    assert updated_task.content == new_data["content"]
    assert updated_task.priority == new_data["priority"]
    assert updated_task.details == new_data["details"]
    # Los campos no actualizados deben mantener sus valores originales
    assert updated_task.status == original_task.status # Status no se actualizó
    assert updated_task.tag == original_task.tag       # Tag no se actualizó


# TEST: 07
def test_check_or_uncheck_task(test_repo: RepositoryDB) -> None:
    """
    Comprueba que el método check_or_uncheck_task alterna correctamente
    el estado de una tarea entre 'pending' y 'completed'.
    """
    # --- Preparar ---
    # 1. Creamos una tarea con estado inicial 'pending'.
    initial_task = Task(content="Tarea para marcar/desmarcar", status="pending")
    task_id = test_repo.new_task(initial_task)
    assert task_id is not None

    # --- Actuar (Primera vez: de pending a completed) ---
    test_repo.check_or_uncheck_task(task_id)

    # --- Verificar (Primera vez) ---
    updated_task = test_repo.get_task_by_id(task_id)
    assert updated_task is not None
    assert updated_task.id == task_id
    assert updated_task.status == "completed" # Debería haber cambiado a 'completed'

    # --- Actuar (Segunda vez: de completed a pending) ---
    test_repo.check_or_uncheck_task(task_id)

    # --- Verificar (Segunda vez) ---
    re_updated_task = test_repo.get_task_by_id(task_id)
    assert re_updated_task is not None
    assert re_updated_task.id == task_id
    assert re_updated_task.status == "pending" # Debería haber cambiado de nuevo a 'pending'


# TEST: 08
def test_delete_task(test_repo: RepositoryDB) -> None:
    """
    Comprueba que el método delete_task elimina correctamente una tarea
    de la base de datos.
    """
    # --- Preparar ---
    # 1. Creamos una tarea que vamos a eliminar.
    task_to_delete = Task(content="Tarea para eliminar", priority="baja")
    task_id = test_repo.new_task(task_to_delete)
    assert task_id is not None # Aseguramos que se insertó y tiene ID

    # --- Actuar ---
    # 2. Llamamos al método delete_task.
    test_repo.delete_task(task_id)

    # --- Verificar ---
    # 3. Intentamos recuperar la tarea eliminada.
    deleted_task = test_repo.get_task_by_id(task_id)

    # 4. Comprobamos que la tarea ya no existe en la base de datos.
    assert deleted_task is None # Debería ser None si se eliminó correctamente
