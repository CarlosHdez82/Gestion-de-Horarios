from fastapi import APIRouter
from app.models.programs_model import Programs
from app.controllers.programs_controller import ProgramsController

router = APIRouter()

programs_controller = ProgramsController()

@router.post("/create_program")
async def create_program(program: Programs):
    return programs_controller.create_program(program)

@router.get("/get_program/{program_id}", response_model=Programs)
async def get_program(program_id: int):
    return programs_controller.get_program(program_id)

@router.get("/get_programs/")
async def get_programs():
    return programs_controller.get_programs()

@router.put("/update_program/{program_id}", response_model=Programs)
async def update_program(program_id: int, program: Programs):
    return programs_controller.update_program(program_id, program)

@router.delete("/delete_program/{program_id}", response_model=Programs)
async def delete_program(program_id: int):
    return programs_controller.delete_program(program_id)