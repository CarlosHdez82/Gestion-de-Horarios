from fastapi import APIRouter
from app.models.teacherspecialties_model import TeacherSpecialties
from app.controllers.teacherspecialties_controller import TeacherSpecialtiesController

router = APIRouter()

teacherspecialties_controller = TeacherSpecialtiesController()

@router.post("/create_relation")
async def create_relation(relation: TeacherSpecialties):
    return teacherspecialties_controller.create_relation(relation)

@router.get("/get_relation/{teacher_id}/{specialty_id}", response_model=TeacherSpecialties)
async def get_relation(teacher_id: int, specialty_id: int):
    return teacherspecialties_controller.get_relation(teacher_id, specialty_id)

@router.get("/get_relations/")
async def get_relations():
    return teacherspecialties_controller.get_relations()

@router.put("/update_relation/{teacher_id}/{specialty_id}", response_model=TeacherSpecialties)
async def update_relation(teacher_id: int, specialty_id: int, relation: TeacherSpecialties):
    return teacherspecialties_controller.update_relation(teacher_id, specialty_id, relation)

@router.delete("/delete_relation/{teacher_id}/{specialty_id}", response_model=TeacherSpecialties)
async def delete_relation(teacher_id: int, specialty_id: int):
    return teacherspecialties_controller.delete_relation(teacher_id, specialty_id)