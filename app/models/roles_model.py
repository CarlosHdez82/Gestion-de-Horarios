from pydantic import BaseModel
from typing import Optional

# Este es el que te faltaba
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Este es el que usas para las respuestas (el que incluye ID)
class Roles(RoleCreate):
    id: int

    class Config:
        from_attributes = True