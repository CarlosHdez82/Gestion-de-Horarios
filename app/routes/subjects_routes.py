from fastapi import APIRouter
from app.models.subjects_model import Subjects
from app.controllers.subjects_controller import SubjectsController

router = APIRouter()

subjects_controller = SubjectsController()

@router.post("/create_subject")
async def create_subject(subject: Subjects):
    return subjects_controller.create_subject(subject)

@router.get("/get_subject/{id}", response_model=Subjects)
async def get_subject(id: int):
    return subjects_controller.get_subject(id)

@router.get("/get_subjects/")
async def get_subjects():
    return subjects_controller.get_subjects()

@router.put("/update_subject/{id}", response_model=Subjects)
async def update_subject(id: int, subject: Subjects):
    return subjects_controller.update_subject(id, subject)

@router.delete("/delete_subject/{id}", response_model=Subjects)
async def delete_subject(id: int):
    return subjects_controller.delete_subject(id)