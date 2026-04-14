from pydantic import BaseModel
from typing import Optional

class Programs(BaseModel):
    program_id: Optional[int] = None
    name: str
    faculty_id: int
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    # Campo extra para mostrar el nombre de la facultad en la tabla
    faculty_name: Optional[str] = None

    class Config:
        from_attributes = True