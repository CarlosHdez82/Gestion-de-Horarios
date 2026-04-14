from fastapi import APIRouter, HTTPException
from app.models.teachers_model import TeacherCreate, TeacherResponse
from app.controllers.teachers_controller import TeachersController

router = APIRouter()
teacher_ctrl = TeachersController()

# Usamos rutas limpias (sin / al final) para evitar el error 307
@router.get("/get_teachers", response_model=list[TeacherResponse])
async def get_teachers():
    return teacher_ctrl.get_teachers()

@router.get("/get_teacher/{teacher_id}", response_model=TeacherResponse)
async def get_teacher(teacher_id: int):
    return teacher_ctrl.get_teacher(teacher_id)

@router.post("/create_teacher")
async def create_teacher(teacher: TeacherCreate):
    return teacher_ctrl.create_teacher(teacher)

@router.put("/update_teacher/{teacher_id}")
async def update_teacher(teacher_id: int, teacher: TeacherCreate):
    return teacher_ctrl.update_teacher(teacher_id, teacher)

@router.delete("/delete_teacher/{teacher_id}")
async def delete_teacher(teacher_id: int):
    return teacher_ctrl.delete_teacher(teacher_id)