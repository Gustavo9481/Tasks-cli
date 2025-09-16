# MODULO: models
# .. ............................. model_task ............................. ..󰌠
"""Define el modelo de datos principal para una Tarea.

Este módulo contiene la clase `Task`, que actúa como un Data Transfer Object
(DTO) y modelo de validación usando Pydantic. También define los tipos 
`Literal` para restringir los valores permitidos en los campos de la tarea.
"""
# OK: 

from typing import Optional, Literal
from pydantic import BaseModel


Status = Literal["pending", "in_progress", "completed"]
Tag = Literal["personal", "proyecto", "trabajo", "calendario"]
Priority = Literal["baja", "media", "alta"]


class Task(BaseModel):
    """Representa una única tarea y define su esquema de datos.

    Utiliza Pydantic para la validación automática, asegurando que cualquier
    objeto `Task` en la aplicación sea siempre consistente y contenga datos
    válidos.

    Attributes:
        - id (Optional[int]): El identificador único de la tarea, generado por
          la base de datos. Es `None` para tareas nuevas aún no guardadas.
        - status (Status): El estado actual de la tarea. Default: "pending".
        - tag (Tag): La categoría o etiqueta de la tarea. Default: "personal".
        - content (str): La descripción principal de lo que se debe hacer.
        - priority (Priority): Nivel de prioridad de la tarea. Default: "baja".
        - details (Optional[str]): Notas o información adicional sobre la
          tarea, que puede contener formato Markdown. Default: `None`.
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
            str: Cadena de caracteres con la información de la tarea.
        """
        return f"{self.status} - {self.tag} | {self.content} | {self.priority}"
