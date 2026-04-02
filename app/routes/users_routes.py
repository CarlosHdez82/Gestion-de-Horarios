from fastapi import APIRouter
from app.models.users_model import Users
from app.controllers.users_controller import UsersController

router = APIRouter()

users_controller = UsersController()

@router.post("/create_user")
async def create_user(user: Users):
    return users_controller.create_user(user)

@router.get("/get_user/{user_id}", response_model=Users)
async def get_user(user_id: int):
    return users_controller.get_user(user_id)

@router.get("/get_users/")
async def get_users():
    return users_controller.get_users()

@router.put("/update_user/{user_id}", response_model=Users)
async def update_user(user_id: int, user: Users):
    return users_controller.update_user(user_id, user)

@router.delete("/delete_user/{user_id}", response_model=Users)
async def delete_user(user_id: int):
    return users_controller.delete_user(user_id)