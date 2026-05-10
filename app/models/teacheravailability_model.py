from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- 1. MODELO BASE ---
class TeacherAvailabilityBase(BaseModel):
    teacher_id: int
    period_id: int
    day_of_week: str  # 'Lunes', 'Martes', etc.
    block_label: str  # '06:00 - 08:00'

# --- 2. MODELO PARA CREACIÓN ---
class TeacherAvailabilityCreate(TeacherAvailabilityBase):
    pass

# --- 3. MODELO PARA RESPUESTA ---
class TeacherAvailabilityResponse(TeacherAvailabilityBase):
    id: int
    # --- CAMPOS NUEVOS PARA QUE PASEN AL FRONTEND ---
    teacher_name: Optional[str] = None
    period_name: Optional[str] = None
    # -----------------------------------------------
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True