from fastapi import APIRouter
from models.teacherdegrees_model import TeacherDegrees
from controllers.teacherdegrees_controller import TeacherDegreesController

router = APIRouter()

teacherdegrees_controller = TeacherDegreesController()

@router.post("/create_teacherdegree")
async def create_teacherdegree(teacherdegree: TeacherDegrees):
    return teacherdegrees_controller.create_teacherdegree(teacherdegree)

@router.get("/get_teacherdegree/{teacherdegree_id}", response_model=TeacherDegrees)
async def get_teacherdegree(teacherdegree_id: int):
    return teacherdegrees_controller.get_teacherdegree(teacherdegree_id)

@router.get("/get_teacherdegrees/")
async def get_teacherdegrees():
    return teacherdegrees_controller.get_teacherdegrees()

@router.put("/update_teacherdegree/{teacherdegree_id}", response_model=TeacherDegrees)
async def update_teacherdegree(teacherdegree_id: int, teacherdegree: TeacherDegrees):
    return teacherdegrees_controller.update_teacherdegree(teacherdegree_id, teacherdegree)

@router.delete("/delete_teacherdegree/{teacherdegree_id}", response_model=TeacherDegrees)
async def delete_teacherdegree(teacherdegree_id: int):
    return teacherdegrees_controller.delete_teacherdegree(teacherdegree_id)