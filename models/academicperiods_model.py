from pydantic import BaseModel

class AcademicPeriods(BaseModel):
    id: int = None
    name: str
    start_date: str
    end_date: str
    is_active: bool = True