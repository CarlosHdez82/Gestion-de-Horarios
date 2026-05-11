from fastapi import APIRouter
from typing import List
# Importamos los nombres exactos de tu modelo de horarios
from app.models.schedules_model import ScheduleCreate, ScheduleResponse 
from app.controllers.schedules_controller import SchedulesController

# Prefijo y tags para organización en la documentación de FastAPI
router = APIRouter(prefix="/schedules", tags=["Schedules"])
controller = SchedulesController()

@router.post("/")
async def create_schedule(schedule: ScheduleCreate):
    """
    Registra un nuevo bloque de horario (Asignación de clase).
    """
    return controller.create_schedule(schedule)

@router.get("/", response_model=List[ScheduleResponse])
async def get_schedules():
    """
    Obtiene la lista completa de horarios generados para la CUL.
    """
    return controller.get_schedules()

@router.put("/{id}")
async def update_schedule(id: int, schedule: ScheduleCreate):
    """Actualiza un bloque de horario (cambio de docente, salón o materia)"""
    return controller.update_schedule(id, schedule)

@router.delete("/{id}")
async def delete_schedule(id: int):
    """Elimina un bloque de horario específico"""
    return controller.delete_schedule(id)