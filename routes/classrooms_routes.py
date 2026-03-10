from fastapi import APIRouter
from models.classrooms_model import Classrooms
from controllers.classrooms_controller import ClassroomsController

router = APIRouter()
controller = ClassroomsController()

@router.post("/create_classroom")
async def create_classroom(classroom: Classrooms):
    return controller.create_classroom(classroom)

@router.get("/get_classroom/{id}", response_model=Classrooms)
async def get_classroom(id: int):
    return controller.get_classroom(id)

@router.get("/get_classrooms/")
async def get_classrooms():
    return controller.get_classrooms()

@router.put("/update_classroom/{id}", response_model=Classrooms)
async def update_classroom(id: int, classroom: Classrooms):
    return controller.update_classroom(id, classroom)

@router.delete("/delete_classroom/{id}", response_model=Classrooms)
async def delete_classroom(id: int):
    return controller.delete_classroom(id)