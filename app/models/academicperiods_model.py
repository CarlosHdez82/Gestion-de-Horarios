from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- 1. MODELO BASE ---
# Lo que define esencialmente a un periodo en tu sistema.
class AcademicPeriodBase(BaseModel):
    name: str  # Ejemplo: "2026-1", "2026-2"
    is_active: bool = True

# --- 2. MODELO PARA CREACIÓN ---
# Se usa cuando el Administrador registra un nuevo periodo.
class AcademicPeriodCreate(AcademicPeriodBase):
    # Usamos pass porque por ahora solo necesitamos el nombre y el estado.
    pass

# --- 3. MODELO PARA RESPUESTA ---
# Lo que el Frontend recibe para llenar selectores o tablas.
class AcademicPeriodResponse(AcademicPeriodBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True