# MODULO: repositories
# .. ............................................................... querys ..󰌠
"""Centraliza todas las sentencias SQL utilizadas en la aplicación.

Este módulo actúa como una única fuente de consultas SQL, lo que facilita su
mantenimiento y lectura. Previene la dispersión de sentencias SQL a través de
la lógica de la aplicación.
"""

# .. ......................................................... create_table ..󰌠
# Crea la tabla 'tasks_table' si no existe, definiendo su estructura.
CREATE_TABLE: str = """
    CREATE TABLE IF NOT EXISTS tasks_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL,
        tag TEXT NOT NULL,
        content TEXT NOT NULL,
        priority TEXT NOT NULL,
        details TEXT
    );
"""


# .. ........................................................ get_all_tasks ..󰌠
# Obtiene todas las tareas de la base de datos.
GET_ALL_TASKS = """
    SELECT id, status, tag, content, priority, details
    FROM tasks_table;
"""


# .. ............................................................. new_task ..󰌠
# Inserta una nueva tarea en la tabla.
# Placeholders: status, tag, content, priority, details
NEW_TASK: str = """
    INSERT INTO tasks_table (
        status, tag, content, priority, details
    ) VALUES (?, ?, ?, ?, ?);
"""


# .. ......................................................... filter_tasks ..󰌠
# --- Filtrado por 1 Criterio ---
# Selecciona tareas que coincidan con un 'status' específico.
FILTER_TASK_STATUS: str = """
    SELECT id, status, tag, content, priority, details
    FROM tasks_table
    WHERE status = ?;
"""

# Selecciona tareas que coincidan con un 'tag' específico.
FILTER_TASK_TAG: str = """
    SELECT id, status, tag, content, priority, details
    FROM tasks_table
    WHERE tag = ?;
"""

# Selcciona tareas que coincidan con uns 'priority' específica.
FILTER_TASK_PRIORITY: str = """
    SELECT id, status, tag, content, priority, details
    FROM tasks_table
    WHERE priority = ?;
"""

# --- Filtrado por 2 Criterios ---
# Selecciona tareas por 'status' y 'tag' específicos.
FILTER_BY_STATUS_AND_TAG: str = """
    SELECT id, status, tag, content, priority, details
    FROM tasks_table
    WHERE status = ?
    AND tag = ?;
"""

# Selecciona tareas por 'status' y 'priority' específicos.
FILTER_BY_STATUS_AND_PRIORITY: str = """
    SELECT id, status, tag, content, priority, details
    FROM tasks_table
    WHERE status = ?
    AND priority = ?;
"""

# Selecciona tareas por 'tag' y 'priority' específicos.
FILTER_BY_TAG_AND_PRIORITY: str = """
    SELECT id, status, tag, content, priority, details
    FROM tasks_table
    WHERE tag = ?
    AND priority = ?;
"""

# --- Filtrado por 3 Criterios ---
# Selecciona tareas por 'status', 'tag' y 'priority' específicos.
FILTER_BY_ALL: str = """
    SELECT id, status, tag, content, priority, details
    FROM tasks_table
    WHERE status = ?
    AND tag = ?
    AND priority = ?;
"""


# .. .......................................................... update_task ..󰌠
# Query base para actualizar una tarea. Se completa dinámicamente.
UPDATE_TASK: str = "UPDATE tasks_table SET"


# .. ................................................ check_or_uncheck_task ..󰌠
# Selecciona una tarea por su 'id'.
SELECT_TASK: str = "SELECT * FROM tasks_table WHERE id = ?"

# Actualiza el 'status' de una tarea específica por su 'id'.
UPDATE_STATUS: str = "UPDATE tasks_table SET status = ? WHERE id = ?;"

# Cambia el 'status' de una tarea de forma cíclica.
# (pending -> in_progress -> completed -> pending)
UPDATE_STATUS_TOGGLE = """
    UPDATE tasks_table
    SET status = CASE
        WHEN status = 'pending' THEN 'in_progress'
        WHEN status = 'in_progress' THEN 'completed'
        WHEN status = 'completed' THEN 'pending'
        ELSE status
    END
    WHERE id = ?;
"""


# .. ....................................................... get_task_by_id ..󰌠
# Selecciona una tarea por su 'id'.
GET_TASK_BY_ID = """
    SELECT id, status, tag, content, priority, details 
    FROM tasks_table 
    WHERE id = ?;
"""


# .. .......................................................... delete_task ..󰌠
# Elimina una tarea de la tabla identificada por su 'id'.
DELETE_TASK = "DELETE FROM tasks_table WHERE id= ?;"
