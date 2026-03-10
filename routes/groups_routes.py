from fastapi import APIRouter
from models.groups_model import Groups
from controllers.groups_controller import GroupsController

router = APIRouter()

groups_controller = GroupsController()

@router.post("/create_group")
async def create_group(group: Groups):
    return groups_controller.create_group(group)

@router.get("/get_group/{id}", response_model=Groups)
async def get_group(id: int):
    return groups_controller.get_group(id)

@router.get("/get_groups/")
async def get_groups():
    return groups_controller.get_groups()

@router.put("/update_group/{id}", response_model=Groups)
async def update_group(id: int, group: Groups):
    return groups_controller.update_group(id, group)

@router.delete("/delete_group/{id}", response_model=Groups)
async def delete_group(id: int):
    return groups_controller.delete_group(id)