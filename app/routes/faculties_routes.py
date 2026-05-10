from fastapi import APIRouter
from app.models.faculties_model import FacultyCreate, FacultyResponse
from app.controllers.faculties_controller import FacultiesController
from typing import List

# Agregamos prefijo y tags para una documentación impecable
router = APIRouter(prefix="/faculties", tags=["Faculties"])

faculties_controller = FacultiesController()

@router.post("/")
async def create_faculty(faculty: FacultyCreate):
    """Registra una nueva facultad en la CUL"""
    return faculties_controller.create_faculty(faculty)

@router.get("/{id}", response_model=FacultyResponse)
async def get_faculty(id: int):
    """Obtiene la información de una facultad específica"""
    return faculties_controller.get_faculty(id)

@router.get("/", response_model=List[FacultyResponse])
async def get_faculties():
    """Lista todas las facultades registradas"""
    return faculties_controller.get_faculties()

@router.put("/{id}", response_model=FacultyResponse)
async def update_faculty(id: int, faculty: FacultyCreate):
    """Actualiza el nombre o estado de una facultad"""
    return faculties_controller.update_faculty(id, faculty)

@router.delete("/{id}")
async def delete_faculty(id: int):
    """Elimina una facultad (Si no tiene programas asociados)"""
    return faculties_controller.delete_faculty(id)