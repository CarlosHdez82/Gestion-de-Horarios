from pydantic import BaseModel

class Faculties(BaseModel):
    faculties_id: int = None
    name: str