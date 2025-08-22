# MODULO: models/
# .. ............................. model_task ............................. ..󰌠
"""
Data Tranfer Object -> class Task: objeto contenedor de la data de una tarea
Se usa pydantic para asegurar el tipo de datos.
Los objetos Literal(typing) contienen los valores permitidos para dichas
propiedades.
ïconos de uso a futuro 󰗠 
- [x] black
- [x] flake8
- [x] mypy
"""

from typing import Literal
from pydantic import BaseModel

# NOTE: Restricción de datos.
# Los objetos Literal contienen una lista de los valores admitidos para las
# propiedades de Task.
Status = Literal["pending", "completed"]
Tag = Literal["personal", "proyecto", "trabajo", "calendario"]
Priority = Literal["baja", "media", "alta"]


class Task(BaseModel):
    """Clase contenedora del objeto Task.

    El objeto contiene los datos para gestionar una tarea, tanto registros en
    base de datos como renderizado en interfaz.

    Attributes:
        id (int | None): Identificador opcional, generado por la base de datos.
        status (Status): Estado de la tarea. Valores válidos definidos en
        `Status` (Literal).
        tag (Tag): Etiqueta de la tarea. Valores válidos definidos en
        `Tag` (Literal).
        content (str): Contenido o descripción de la tarea.
        priority (Priority): Prioridad de la tarea. Valores válidos definidos
        en `Priority` (Literal).
    """

    id: int | None = None
    status: Status = "pending"
    tag: Tag = "personal"
    content: str
    priority: Priority = "baja"

    def __str__(self) -> str:
        """Devuelve una representación en cadena de la tarea para facilitar su
        3     lectura.
        4
        5     Returns:
        6         str: Cadena de caracteres con la información de la tarea.
        7"""
        return f"{self.status} - {self.tag} | {self.content} | {self.priority}"
