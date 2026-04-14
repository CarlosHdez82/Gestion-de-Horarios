from pydantic import BaseModel
from typing import Optional

class TeacherAvailability(BaseModel):
    id: Optional[int] = None
    teacher_id: int
    period_id: int
    day_of_week: str
    start_time: str
    end_time: str
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    # Campos para mostrar en la tabla (JOINs)
    teacher_name: Optional[str] = None
    period_name: Optional[str] = None

    class Config:
        from_attributes = True