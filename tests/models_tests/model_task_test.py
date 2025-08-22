# MODULO: test/
# .. .......................... model_task_tests .......................... ..󰌠
"""
Tests unitarios para la clase Task.
total de pruebas: 9.
"""

import pytest
from typing import Literal
from pydantic import ValidationError
from models.model_task import Task


# TEST: 01
def test_task_creation_with_defaults():
    """Comprueba la creación de una instancia Tarea con valores defaults.

    El test verifica que la creación de una instancia de Task especificando
    sólo el valor de content(contenido de la tarea o descripción), la tarea se
    crea correctamente con los valores por defecto en sus otras propiedades.
    """
    content_text: str = "Contenido de prueba: creación por defecto"
    test_instance = Task(content=content_text)

    assert test_instance.id is None
    assert test_instance.status == "pending"
    assert test_instance.tag == "personal"
    assert test_instance.content == content_text
    assert test_instance.priority == "baja"


# TEST: 02
def test_task_creation_with_no_defaults():
    """Comprueba la creación de una instancia de Tarea con valores distintos a
    los defaults.

    El test verifica que si la tarea se crea con valores distintos a los
    defaults pero aceptados en sus propiedades status, tag y priority, la tarea
    se crea correctamente. Los valores aceptados se especifican en
    models/model_task.py en las listas Literal [Status, Tag, Priority].
    """
    diferent_status: str = "completed"
    diferent_tag: str = "trabajo"
    diferent_priority: str = "alta"
    content_text: str = "Contenido de prueba: creación con valores diferentes"

    test_instance = Task(
                            status=diferent_status,
                            content=content_text,
                            tag=diferent_tag,
                            priority=diferent_priority
                        )

    assert test_instance.id is None
    assert test_instance.status ==diferent_status
    assert test_instance.content == content_text
    assert test_instance.tag == diferent_tag
    assert test_instance.priority == diferent_priority


# TEST: 03
def test_task_creation_with_invalid_status():
    """Comprueba error al crear una tarea con un status inválido.

    Este test verifica que si la tarea es creada con un valor de status no
    válido, la tarea no se crea. Los valores válidos se definen en el módulo
    models/model_task.py en la lista Literal Status.
    """
    status_invalid: str = "invalid"
    content_text: str = "Contenido de prueba: status inválido"

    with pytest.raises(ValidationError) as excinfo:
        test_instance = Task(status=status_invalid, content=content_text)


def test_task_creation_with_invalid_tag():
    # TEST: creación de tarea con tag inválido.
    tag_invalid: str = "invalid"
    content_text: str = "Contenido de prueba: tag inválido"

    with pytest.raises(ValidationError) as excinfo:
        test_instance = Task(tag=tag_invalid, content=content_text)


def test_task_creation_with_invalid_content_type_integer():
    # TEST: creación de tarea con contenido de tipo inválido (int).
    content_invalid: int = 1234567890

    with pytest.raises(ValidationError) as excinfo:
        test_instance = Task(content=content_invalid)


def test_task_creation_with_invalid_content_type_float():
    # TEST: creación de tarea con contenido de tipo inválido (float).
    content_invalid: float = 1.234567890

    with pytest.raises(ValidationError) as excinfo:
        test_instance = Task(content=content_invalid)


def test_task_creation_with_invalid_content_type_boolean():
    # TEST: creación de tarea con contenido de tipo inválido (bool).
    content_invalid: bool = True

    with pytest.raises(ValidationError) as excinfo:
        test_instance = Task(content=content_invalid)


def test_task_creation_with_missing_content():
    # TEST: creación de tarea sin definir el contenido.
    with pytest.raises(ValidationError):
        test_instance = Task(status="pending", tag="personal", priority="baja")


def test_task_creation_with_invalid_priority():
    # TEST: creación de tarea con prioridad inválida.
    priority_invalid: str = "invalid"
    content_text: str = "Contenido de prueba: prioridad inválida"

    with pytest.raises(ValidationError) as excinfo:
        test_instance = Task(content=content_text, priority=priority_invalid)
