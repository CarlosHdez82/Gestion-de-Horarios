from pydantic import BaseModel

class Programs(BaseModel):
    program_id: int = None
    name: str
    faculty_id: int