from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    # Validamos que sea un email real y eliminamos espacios accidentales
    email: EmailStr = Field(..., example="docente@cul.edu.co")
    
    # Validamos una longitud mínima para evitar ataques de fuerza bruta simples
    password: str = Field(..., min_length=6, example="contraseña123")

class LoginResponse(BaseModel):
    # Lo que devolverás a Svelte después de un login exitoso
    access_token: str
    token_type: str = "bearer"
    user: dict # Aquí enviarás nombre, rol y programa del docente