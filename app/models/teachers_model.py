from pydantic import BaseModel

class Teachers(BaseModel):
    teacher_id: int = None
    first_name: str
    last_name: str
    email: str
    phone: str
    hire_date: str
    faculty_id: int
    program_id: int
    level_id: int
    role_id: int
    is_active: bool
    created_at: str = None
    updated_at: str = None