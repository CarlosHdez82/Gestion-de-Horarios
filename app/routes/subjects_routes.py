from fastapi import APIRouter
from typing import List
# Importamos los nombres EXACTOS de tu modelo de materias
from app.models.subjects_model import SubjectCreate, SubjectResponse 
from app.controllers.subjects_controller import SubjectsController

router = APIRouter(prefix="/subjects", tags=["Subjects"])
subjects_controller = SubjectsController()

@router.get("/", response_model=List[SubjectResponse]) # <-- Antes era Subjects
async def get_subjects():
    """Lista todas las materias de la universidad"""
    return subjects_controller.get_subjects()

@router.get("/{id}", response_model=SubjectResponse) # <-- Antes era Subjects
async def get_subject(id: int):
    """Obtiene una materia específica por su ID"""
    return subjects_controller.get_subject(id)

@router.post("/")
async def create_subject(subject: SubjectCreate):
    """Registra una nueva materia (usa código, nombre, créditos y programa)"""
    return subjects_controller.create_subject(subject)

@router.put("/{id}")
async def update_subject(id: int, subject: SubjectCreate):
    """Actualiza los datos de una materia existente"""
    return subjects_controller.update_subject(id, subject)

@router.delete("/{id}")
async def delete_subject(id: int):
    """Elimina una materia del sistema"""
    return subjects_controller.delete_subject(id)