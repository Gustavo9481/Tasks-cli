# MODULO: models/
# .. ............................. model_task ............................. ..󰌠
"""
Data Tranfer Object -> class Task: objeto contenedor de la data de una tarea
Se usa pydantic para asegurar el tipo de datos.
Los objetos Literal(typing) contienen los valores permitidos para dichas
propiedades.
ïconos de uso a futuro 󰗠 
"""

from typing import Optional, Literal
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
        - id (Optional[str]): Identificador opcional, generado por la base de
          datos.
        - status (Status): Estado de la tarea. Valores válidos definidos en
          `Status` (Literal).
        - tag (Tag): Etiqueta de la tarea. Valores válidos definidos en
          `Tag` (Literal).
        - content (str): Contenido o descripción de la tarea.
        - priority (Priority): Prioridad de la tarea. Valores válidos definidos
          en `Priority` (Literal).
        - details (Optional[str]): Detalles o notas extensas para la tarea.
    """

    id: Optional[int] = None
    status: Status = "pending"
    tag: Tag = "personal"
    content: str
    priority: Priority = "baja"
    details: Optional[str] = None

    def __str__(self) -> str:
        """Devuelve una representación en cadena de la tarea para facilitar su
        lectura.

        Returns:
            - str: Cadena de caracteres con la información de la tarea.
        """
        return f"{self.status} - {self.tag} | {self.content} | {self.priority}"
