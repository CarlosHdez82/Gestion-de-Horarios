from pydantic import BaseModel

class TeacherSpecialties(BaseModel):
    teacher_id: int = None
    specialty_id: int = None