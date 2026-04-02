from fastapi import APIRouter, HTTPException
from controllers.roles_controller import *
from models.roles_model import Roles

router = APIRouter()

roles_controller = RolesController()

@router.post("/create_role/", response_model=Roles)
async def create_role(role: Roles):
    return roles_controller.create_role(role)

@router.get("/get_role/{role_id}", response_model=Roles)
async def get_role(role_id: int):
    return roles_controller.get_role(role_id)

@router.get("/get_roles/")
async def get_roles():
    return roles_controller.get_roles()

@router.put("/update_role/{role_id}", response_model=Roles)
async def update_role(role_id: int, role: Roles):
    return roles_controller.update_role(role_id, role)

@router.delete("/delete_role/{role_id}", response_model=Roles)
async def delete_role(role_id: int):
    return roles_controller.delete_role(role_id)