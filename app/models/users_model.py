# ============================================================
# users_model.py — Modelos de Usuarios
# ============================================================
# Define la estructura de datos para los usuarios del sistema
# usando Pydantic. Los usuarios pueden ser administradores,
# coordinadores o docentes, según el rol asignado.
#
# Patrón Base → Create → Response:
# - Base:     campos comunes compartidos por todos los modelos
# - Create:   hereda de Base, agrega password para crear usuario
# - Response: hereda de Base, agrega campos que genera la BD (GET)
#
# SEGURIDAD: el campo password_hash solo existe en UserCreate
# y nunca en UserResponse, evitando que la contraseña
# sea expuesta en las respuestas de la API.
# ============================================================

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ------------------------------------------------------------
# Modelo Base — campos comunes del usuario
# Todos los demás modelos heredan de esta clase.
# ------------------------------------------------------------
class UserBase(BaseModel):
    first_name: str                     # Nombre del usuario
    last_name: str                      # Apellido del usuario
    email: EmailStr                     # Correo electrónico validado por Pydantic
                                        # (debe tener formato válido: usuario@dominio.com)
    role_id: int                        # ID del rol asignado (Administrador, Docente, etc.)
    program_id: Optional[int] = None    # ID del programa al que pertenece el usuario
                                        # Opcional porque no todos los roles requieren programa
                                        # (ej: un Administrador no pertenece a un programa)
    is_active: bool = True              # Indica si el usuario tiene acceso activo al sistema

# ------------------------------------------------------------
# Modelo de Creación — usado en POST y PUT
# Extiende Base agregando la contraseña, que solo se recibe
# al momento de crear o actualizar un usuario.
# NUNCA se incluye en las respuestas para proteger la seguridad.
# ------------------------------------------------------------
class UserCreate(UserBase):
    password_hash: str  # Contraseña del usuario (se hashea antes de guardar en la BD)

# ------------------------------------------------------------
# Modelo de Respuesta — usado en GET
# Extiende Base con los campos que genera automáticamente
# la base de datos. No incluye password_hash por seguridad.
# ------------------------------------------------------------
class UserResponse(UserBase):
    id: int                                 # Identificador único generado por la BD
    created_at: Optional[datetime] = None   # Fecha y hora de creación del registro
    updated_at: Optional[datetime] = None   # Fecha y hora de la última modificación

    class Config:
        # from_attributes = True permite que Pydantic lea los datos
        # directamente desde objetos ORM (filas de la base de datos),
        # en lugar de requerir un diccionario como entrada.
        from_attributes = True