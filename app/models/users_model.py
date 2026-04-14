from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- 1. MODELO BASE ---
# Contiene lo que es COMÚN para todas las operaciones.
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # Valida automáticamente que sea un correo real
    role_id: int
    is_active: bool = True

# --- 2. MODELO PARA CREACIÓN (ENTRADA) ---
# Hereda de UserBase. Se usa cuando registramos a alguien desde Svelte.
class UserCreate(UserBase):
    password: str  # Recibimos la clave plana para encriptarla en el controlador

# --- 3. MODELO PARA RESPUESTA (SALIDA) ---
# Hereda de UserBase. Es lo que la API devuelve a la tabla del Frontend.
class UserResponse(UserBase):
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # Esto permite que FastAPI convierta los datos de PostgreSQL (objetos) 
        # directamente a este formato JSON.
        from_attributes = True