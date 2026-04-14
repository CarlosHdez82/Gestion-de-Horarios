from pydantic import BaseModel
from typing import Optional

class Subjects(BaseModel):
    id: Optional[int] = None
    name: str
    code: str
    credits: int
    program_id: int
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # Este campo es vital para el GET con JOIN
    program_name: Optional[str] = None

    class Config:
        from_attributes = True