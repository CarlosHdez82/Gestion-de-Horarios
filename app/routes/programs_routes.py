from fastapi import APIRouter
from typing import List
from app.models.programs_model import Programs
from app.controllers.programs_controller import ProgramsController

router = APIRouter()
programs_controller = ProgramsController()

# Creamos el programa
@router.post("/create_program")
async def create_program(program: Programs):
    return programs_controller.create_program(program)

# Obtenemos un programa específico (Mantenemos response_model=Programs)
@router.get("/get_program/{program_id}", response_model=Programs)
async def get_program(program_id: int):
    return programs_controller.get_program(program_id)

# Obtenemos todos los programas (IMPORTANTE: Usar List[Programs])
@router.get("/get_programs", response_model=List[Programs])
async def get_programs():
    return programs_controller.get_programs()

# Actualizamos programa
# Quitamos response_model=Programs porque el controlador devuelve un mensaje de éxito {"mensaje": "..."}, no el objeto completo.
@router.put("/update_program/{program_id}")
async def update_program(program_id: int, program: Programs):
    return programs_controller.update_program(program_id, program)

# Eliminamos programa
@router.delete("/delete_program/{program_id}")
async def delete_program(program_id: int):
    return programs_controller.delete_program(program_id)