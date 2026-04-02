from pydantic import BaseModel

class Roles(BaseModel):
    role_id: int = None
    name: str
    is_active: bool = True
    created_at: str = None
    updated_at: str = None