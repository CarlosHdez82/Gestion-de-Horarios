from pydantic import BaseModel

class Programs(BaseModel):
    program_id: int = None
    name: str
    faculty_id: int
    is_active: bool = True
    created_at: str = None
    updated_at: str = None