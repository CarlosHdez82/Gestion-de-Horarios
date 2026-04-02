from pydantic import BaseModel

class Schedules(BaseModel):
    id: int = None
    teacher_id: int
    subject_id: int
    period_id: int
    day_of_week: str
    start_time: str
    end_time: str
    created_at: str = None
    is_active: bool = True
    updated_at: str = None