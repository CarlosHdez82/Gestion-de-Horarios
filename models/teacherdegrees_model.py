from pydantic import BaseModel

class TeacherDegrees(BaseModel):
    teacherdegree_id: int = None
    teacher_id: int
    degree_type: str
    title: str
    institution: str