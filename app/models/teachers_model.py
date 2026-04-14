from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- 1. MODELO BASE ---
# Campos comunes para el docente
class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    hire_date: str # Puedes usar 'date' si prefieres validación estricta de fecha
    faculty_id: int
    program_id: int
    level_id: int
    role_id: int
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None   

# --- 2. MODELO PARA CREACIÓN / ACTUALIZACIÓN ---
class TeacherCreate(TeacherBase):
    pass

# --- 3. MODELO PARA RESPUESTA (SALIDA) ---
class TeacherResponse(TeacherBase):
    teacher_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Campos opcionales para cuando hagamos JOINs (ej: nombre de facultad)
    faculty_name: Optional[str] = None
    program_name: Optional[str] = None
    level_name: Optional[str] = None

    class Config:
        from_attributes = True