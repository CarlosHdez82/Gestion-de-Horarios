from pydantic import BaseModel
from datetime import time

class Specialties(BaseModel):
    specialty_id: int = None
    name: str
    is_active: bool = True
    created_at: str = None
    updated_at: str = None