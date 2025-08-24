# MODULO: repositories/
# .. ............................... querys ............................... ..󰌠
# """
# Módulo contenedor de las cadenas de texto correspondientes a las consultas
# sql para repository_db.
# """


# .. ......................................................... create_table ..󰌠
# Verifica si la tabla tasks_table existe en la base de datos, si no existe la
# crea.
CREATE_TABLE: str = """
    CREATE TABLE IF NOT EXISTS tasks_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL,
        tag TEXT NOT NULL,
        content TEXT NOT NULL,
        priority TEXT NOT NULL
    );
"""


# .. ............................................................. new_task ..󰌠
# Inserta un nuevo registro (tarea) en la tabla tasks_table.
NEW_TASK: str = """
    INSERT INTO tasks_table (
        status, tag, content, priority
    ) VALUES (?, ?, ?, ?);
"""


# .. ................................................... filter_task_status ..󰌠
# Filtra los registros de la tabla tasks_table por campo 'status'.
FILTER_TASK_STATUS: str = "SELECT * FROM tasks_table WHERE status = ?;"


# .. ...................................................... filter_task_tag ..󰌠
# Fltra los registros de la tabla tasks_table por campo 'tag'.
FILTER_TASK_TAG: str = "SELECT * FROM tasks_table WHERE tag = ?;"


# .. ................................................. filter_task_priority ..󰌠
# Filtra los registros de la tabla tasks_table por campo 'priority'.
FILTER_TASK_PRIORITY: str = "SELECT * FROM tasks_table WHERE priority = ?;"


# .. .......................................................... update_task ..󰌠
# Actualiza un registro seleccionado por id de la tabla tasks_table.
'''
UPDATE_TASK: str = """
    UPDATE tasks_table SET status = ?, tag = ?, content = ?, priority = ?
    WHERE id = ?;
"""
'''
UPDATE_TASK: str = "UPDATE tasks_table SET"

# .. ................................................ check_or_uncheck_task ..󰌠
# Selecciona un registro de la tabla tasks_table por su 'id'.
SELECT_TASK: str = "SELECT * FROM tasks_table WHERE id = ?"

# Actualiza seleccionado estado 'status' de un registro seleccionado por id de
# la tabla tasks_table.
UPDATE_STATUS: str = "UPDATE tasks_table SET status = ? WHERE id = ?;"

UPDATE_STATUS_TOGGLE = """
    UPDATE tasks_table
    SET status = CASE
    WHEN status = 'completed' THEN 'pending'
    ELSE 'completed'
    END
    WHERE id = ?;
"""


# .. .......................................................... delete_task ..󰌠
# Elimina el registro seleccionado por id de la tabla tasks_table.
DELETE_TASK = "DELETE FROM tasks_table WHERE id= ?;"
