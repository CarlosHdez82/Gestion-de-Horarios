from pydantic import BaseModel
from typing import Optional

class AcademicPeriods(BaseModel):
    id: Optional[int] = None
    name: str
    start_date: str
    end_date: str
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True