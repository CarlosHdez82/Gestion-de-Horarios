from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role_id: int
    program_id: Optional[int] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str # Solo se usa al recibir datos para crear/login

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True