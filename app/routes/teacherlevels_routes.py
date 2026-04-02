from fastapi import APIRouter
from app.models.teacherlevels_model import TeacherLevels
from app.controllers.teacherlevels_controller import TeacherLevelsController

router = APIRouter()

teacherlevels_controller = TeacherLevelsController()

@router.post("/create_teacherlevel")
async def create_teacherlevel(teacherlevel: TeacherLevels):
    return teacherlevels_controller.create_teacherlevel(teacherlevel)

@router.get("/get_teacherlevel/{teacherlevel_id}", response_model=TeacherLevels)
async def get_teacherlevel(teacherlevel_id: int):
    return teacherlevels_controller.get_teacherlevel(teacherlevel_id)

@router.get("/get_teacherlevels/")
async def get_teacherlevels():
    return teacherlevels_controller.get_teacherlevels()

@router.put("/update_teacherlevel/{teacherlevel_id}", response_model=TeacherLevels)
async def update_teacherlevel(teacherlevel_id: int, teacherlevel: TeacherLevels):
    return teacherlevels_controller.update_teacherlevel(teacherlevel_id, teacherlevel)

@router.delete("/delete_teacherlevel/{teacherlevel_id}", response_model=TeacherLevels)
async def delete_teacherlevel(teacherlevel_id: int):
    return teacherlevels_controller.delete_teacherlevel(teacherlevel_id)