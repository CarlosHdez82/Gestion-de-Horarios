from pydantic import BaseModel
from datetime import time

class Specialties(BaseModel):
    specialty_id: int = None
    name: str