from fastapi import APIRouter
from models.teachers_model import Teachers
from controllers.teachers_controller import TeachersController

router = APIRouter()

teachers_controller = TeachersController()

@router.post("/create_teacher")
async def create_teacher(teacher: Teachers):
    return teachers_controller.create_teacher(teacher)

@router.get("/get_teacher/{teacher_id}", response_model=Teachers)
async def get_teacher(teacher_id: int):
    return teachers_controller.get_teacher(teacher_id)

@router.get("/get_teachers/")
async def get_teachers():
    return teachers_controller.get_teachers()

@router.put("/update_teacher/{teacher_id}", response_model=Teachers)
async def update_teacher(teacher_id: int, teacher: Teachers):
    return teachers_controller.update_teacher(teacher_id, teacher)

@router.delete("/delete_teacher/{teacher_id}", response_model=Teachers)
async def delete_teacher(teacher_id: int):
    return teachers_controller.delete_teacher(teacher_id)