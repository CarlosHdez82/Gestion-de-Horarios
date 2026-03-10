from pydantic import BaseModel

class Roles(BaseModel):
    role_id: int = None
    name: str