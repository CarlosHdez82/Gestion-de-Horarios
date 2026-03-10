from pydantic import BaseModel

class ClassroomTypes(BaseModel):
    id: int = None
    name: str