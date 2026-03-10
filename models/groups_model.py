from pydantic import BaseModel

class Groups(BaseModel):
    id: int = None
    section: str
    shift: str
    num_students: int
    subject_id: int = None