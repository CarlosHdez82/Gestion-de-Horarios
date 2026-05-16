# ============================================================
# roles_routes.py — Rutas de Roles de Usuario
# ============================================================
# Define los endpoints REST para gestionar los roles del sistema.
# Los roles controlan los permisos y el nivel de acceso de cada
# usuario (ej: Administrador, Docente, Coordinador).
# ============================================================

from fastapi import APIRouter
from typing import List

# Roles      → modelo para estructurar la respuesta (GET)
# RoleCreate → modelo para recibir datos de entrada (POST/PUT)
from app.models.roles_model import Roles, RoleCreate
from app.controllers.roles_controller import RolesController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/roles" → todas las rutas inician con /roles
# tags=["Roles"]  → agrupa los endpoints en /docs (Swagger UI)
# ------------------------------------------------------------
router = APIRouter(prefix="/roles", tags=["Roles"])

# Instancia del controlador que contiene la lógica de negocio
roles_controller = RolesController()

# ------------------------------------------------------------
# POST /roles/
# Crea un nuevo rol en el sistema.
# El cuerpo del request debe cumplir el esquema RoleCreate.
# ------------------------------------------------------------
@router.post("/")
async def create_role(role: RoleCreate):
    return roles_controller.create_role(role)

# ------------------------------------------------------------
# GET /roles/
# Retorna la lista completa de roles registrados.
# response_model valida y serializa la respuesta automáticamente.
# ------------------------------------------------------------
@router.get("/", response_model=List[Roles])
async def get_roles():
    return roles_controller.get_roles()

# ------------------------------------------------------------
# GET /roles/{id}
# Busca y retorna un rol específico por su ID.
# {id} es un parámetro de ruta que FastAPI extrae de la URL.
# ------------------------------------------------------------
@router.get("/{id}", response_model=Roles)
async def get_role(id: int):
    return roles_controller.get_role(id)

# ------------------------------------------------------------
# PUT /roles/{id}
# Actualiza completamente un rol existente.
# Recibe el ID por la URL y los nuevos datos por el cuerpo del request.
# ------------------------------------------------------------
@router.put("/{id}")
async def update_role(id: int, role: RoleCreate):
    return roles_controller.update_role(id, role)

# ------------------------------------------------------------
# DELETE /roles/{id}
# Elimina permanentemente un rol por su ID.
# Nota: eliminar un rol asignado a usuarios activos puede
# causar problemas de acceso — validar antes de eliminar.
# ------------------------------------------------------------
@router.delete("/{id}")
async def delete_role(id: int):
    return roles_controller.delete_role(id)