from pydantic import BaseModel

class Classrooms(BaseModel):
    id: int = None
    name: str
    capacity: int
    location: str
    type_id: int
    is_active: bool = True