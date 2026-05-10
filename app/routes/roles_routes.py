from fastapi import APIRouter
from typing import List
from app.models.roles_model import Roles, RoleCreate
from app.controllers.roles_controller import RolesController

router = APIRouter(prefix="/roles", tags=["Roles"])
roles_controller = RolesController()

@router.post("/")
async def create_role(role: RoleCreate): # <--- Ahora sí encontrará RoleCreate
    return roles_controller.create_role(role)

@router.get("/", response_model=List[Roles])
async def get_roles():
    return roles_controller.get_roles()

@router.get("/{id}", response_model=Roles)
async def get_role(id: int):
    return roles_controller.get_role(id)

@router.put("/{id}")
async def update_role(id: int, role: RoleCreate):
    return roles_controller.update_role(id, role)

@router.delete("/{id}")
async def delete_role(id: int):
    return roles_controller.delete_role(id)