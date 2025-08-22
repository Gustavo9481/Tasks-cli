# 󰗠 
from typing import Literal
from pydantic import BaseModel

# Restricción de datos.
Status = Literal["pending", "completed"]
Tag = Literal["personal", "proyecto", "trabajo", "calendario"]
Priority = Literal["baja", "media", "alta"]


class Task(BaseModel):
    id: int | None = None
    status: Status = "pending"
    tag: Tag = "personal"
    content: str
    priority: Priority = "baja"

    def __str__(self) -> str:
        return f"{self.status} - {self.tag} | {self.content} | {self.priority}"


"""
* `Literal`: Usamos Literal de typing para asegurarnos de que campos como
  status o tag solo puedan contener los valores que tú definiste. Esto evita 
  errores.
* Valores por defecto: status, tag, y priority ya tienen sus valores por
  defecto, así que no necesitas especificarlos al crear una tarea si no
  quieres cambiarlos.
* `id: int | None = None`: El id es opcional. Esto es útil porque cuando creas
  una nueva tarea, aún no tiene un id; la base de datos se lo asignará. 
  Cuando leas una tarea de la base de datos, sí tendrá un id.
"""
