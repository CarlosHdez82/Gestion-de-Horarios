# ============================================================
# roles_model.py — Modelos de Roles de Usuario
# ============================================================
# Define la estructura de datos para los roles del sistema
# usando Pydantic. Los roles determinan el nivel de acceso
# y los permisos de cada usuario (ej: Administrador, Docente).
#
# Patrón Create → Response:
# - RoleCreate: campos de entrada para crear/actualizar (POST/PUT)
# - Roles:      hereda de RoleCreate, agrega el ID generado por la BD (GET)
#
# Nota: este modelo usa un patrón simplificado de dos clases
# en lugar del patrón Base → Create → Response, ya que los
# roles son entidades simples con pocos campos.
# ============================================================

from pydantic import BaseModel
from typing import Optional

# ------------------------------------------------------------
# Modelo de Creación — usado en POST y PUT
# Define los campos necesarios para crear o actualizar un rol.
# ------------------------------------------------------------
class RoleCreate(BaseModel):
    name: str                           # Nombre del rol (ej: "Administrador", "Docente")
    description: Optional[str] = None  # Descripción opcional del rol y sus permisos

# ------------------------------------------------------------
# Modelo de Respuesta — usado en GET
# Hereda todos los campos de RoleCreate y agrega el ID
# que genera automáticamente la base de datos.
# ------------------------------------------------------------
class Roles(RoleCreate):
    id: int     # Identificador único generado por la BD

    class Config:
        # from_attributes = True permite que Pydantic lea los datos
        # directamente desde objetos ORM (filas de la base de datos),
        # en lugar de requerir un diccionario como entrada.
        from_attributes = True