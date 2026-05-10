from fastapi import APIRouter
from typing import List
# Importamos los nombres EXACTOS que tienes en tu modelo
from app.models.programs_model import ProgramCreate, ProgramResponse 
from app.controllers.programs_controller import ProgramsController

router = APIRouter(prefix="/programs", tags=["Programs"])
programs_controller = ProgramsController()

@router.post("/")
async def create_program(program: ProgramCreate):
    """Crea un nuevo programa académico"""
    return programs_controller.create_program(program)

@router.get("/{id}", response_model=ProgramResponse) # <-- Cambiado de Programs a ProgramResponse
async def get_program(id: int):
    """Obtiene los detalles de un programa por su ID"""
    return programs_controller.get_program(id)

@router.get("/", response_model=List[ProgramResponse]) # <-- Cambiado de Programs a ProgramResponse
async def get_programs():
    """Lista todos los programas registrados en la CUL"""
    return programs_controller.get_programs()

@router.put("/{id}")
async def update_program(id: int, program: ProgramCreate):
    """Actualiza la información de un programa existente"""
    return programs_controller.update_program(id, program)

@router.delete("/{id}")
async def delete_program(id: int):
    """Elimina un programa"""
    return programs_controller.delete_program(id)