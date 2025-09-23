# Repositorio: RepositoryDB

## `repositories.repository_db`

Este módulo define la capa de acceso a datos para la base de datos de tareas.

### Clase `RepositoryDB`

<p align="center">
    <img src="../../../images/class_RepositoryDB.svg"
        alt="Diagrama UML RepositoryDB"
        width="500" align="center"/>
</p>


::: repositories.repository_db.RepositoryDB
    options:
        show_root_heading: false
        show_source: false
        members:
            - __init__
            - task_format_list
            - create_table
            - get_all_tasks
            - new_task
            - filter_tasks
            - update_task
            - check_or_uncheck_task
            - get_task_by_id
            - delete_task
