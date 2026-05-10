from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FacultyBase(BaseModel):
    name: str
    is_active: bool = True

class FacultyCreate(FacultyBase):
    pass

class FacultyResponse(FacultyBase):
    id: int # Ajustado a 'id' según la nueva tabla
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True