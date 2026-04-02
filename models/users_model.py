from pydantic import BaseModel

class Users(BaseModel):
    user_id: int = None
    first_name: str
    last_name: str
    email: str
    password_hash: str
    role_id: int = None
    is_active: bool = True
    created_at: str = None
    updated_at: str = None