from pydantic import BaseModel
from typing import Optional

class Schedules(BaseModel):
    id: Optional[int] = None
    teacher_id: int
    subject_id: int
    period_id: int
    day_of_week: str
    start_time: str
    end_time: str
    created_at: Optional[str] = None
    is_active: bool = True
    updated_at: Optional[str] = None
    
    # Campos adicionales para mostrar en la tabla (JOINs)
    teacher_name: Optional[str] = None
    subject_name: Optional[str] = None
    period_name: Optional[str] = None

    class Config:
        from_attributes = True