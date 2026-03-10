from pydantic import BaseModel

class Schedules(BaseModel):
    id: int = None
    teacher_id: int
    subject_id: int
    group_id: int = None
    classroom_id: int
    period_id: int
    day_of_week: str
    start_time: str
    end_time: str
    created_at: str = None