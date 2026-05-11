from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class AcademicPeriodBase(BaseModel):
    name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True

class AcademicPeriodCreate(AcademicPeriodBase):
    pass

class AcademicPeriodResponse(AcademicPeriodBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
