from pydantic import BaseModel

class Subjects(BaseModel):
    id: int = None
    name: str
    code: str
    credits: int
    program_id: int
    is_active: bool = True