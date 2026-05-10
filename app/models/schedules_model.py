from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScheduleBase(BaseModel):
    teacher_id: int
    subject_id: int
    period_id: int
    day_of_week: str
    block_label: str
    group_code: str = "A"

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True