from pydantic import BaseModel

class TeacherAvailability(BaseModel):
    id: int = None
    teacher_id: int
    period_id: int
    day_of_week: str
    start_time: str
    end_time: str
    is_active: bool = True
    created_at: str = None
    updated_at: str = None