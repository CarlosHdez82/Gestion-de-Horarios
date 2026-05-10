from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProgramBase(BaseModel):
    name: str
    faculty_id: int

class ProgramCreate(ProgramBase):
    pass

class ProgramResponse(ProgramBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True