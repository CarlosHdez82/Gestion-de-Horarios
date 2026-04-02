from pydantic import BaseModel

class TeacherSpecialties(BaseModel):
    teacher_id: int = None
    specialty_id: int = None
    is_active: bool = True
    created_at: str = None
    updated_at: str = None