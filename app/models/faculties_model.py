from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- 1. MODELO BASE ---
# Lo que es común para todas las operaciones de facultad.
class FacultyBase(BaseModel):
    name: str
    is_active: bool = True

# --- 2. MODELO PARA CREACIÓN / ACTUALIZACIÓN ---
# Se usa cuando registras una nueva facultad desde Svelte.
class FacultyCreate(FacultyBase):
    pass # Por ahora no necesitamos campos adicionales para crear

# --- 3. MODELO PARA RESPUESTA (SALIDA) ---
# Es lo que la API devuelve a la tabla del Frontend.
class FacultyResponse(FacultyBase):
    faculties_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # Permite que FastAPI lea los datos directamente de los registros de PostgreSQL
        from_attributes = True