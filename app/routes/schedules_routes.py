# ============================================================
# schedules_routes.py — Rutas de Horarios
# ============================================================
# Define los endpoints REST para gestionar los horarios
# académicos. Un horario representa la asignación de una
# materia a un docente, en un salón y franja horaria específicos.
# ============================================================

from fastapi import APIRouter
from typing import List

# ScheduleCreate  → modelo para recibir datos de entrada (POST/PUT)
# ScheduleResponse → modelo para estructurar la respuesta (GET)
from app.models.schedules_model import ScheduleCreate, ScheduleResponse
from app.controllers.schedules_controller import SchedulesController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/schedules" → todas las rutas inician con /schedules
# tags=["Schedules"]  → agrupa los endpoints en /docs (Swagger UI)
# ------------------------------------------------------------
router = APIRouter(prefix="/schedules", tags=["Schedules"])

# Instancia del controlador que contiene la lógica de negocio
controller = SchedulesController()

# ------------------------------------------------------------
# POST /schedules/
# Crea un nuevo bloque de horario.
# Representa la asignación de una materia a un docente en una
# franja horaria y salón determinados.
# El cuerpo del request debe cumplir el esquema ScheduleCreate.
# ------------------------------------------------------------
@router.post("/")
async def create_schedule(schedule: ScheduleCreate):
    """Registra un nuevo bloque de horario (Asignación de clase)."""
    return controller.create_schedule(schedule)

# ------------------------------------------------------------
# GET /schedules/
# Retorna la lista completa de horarios generados.
# response_model valida y serializa la respuesta automáticamente.
# ------------------------------------------------------------
@router.get("/", response_model=List[ScheduleResponse])
async def get_schedules():
    """Obtiene la lista completa de horarios generados para la CUL."""
    return controller.get_schedules()

# ------------------------------------------------------------
# PUT /schedules/{id}
# Actualiza un bloque de horario existente.
# Permite modificar docente, salón, materia u horario asignado.
# Recibe el ID por la URL y los nuevos datos por el cuerpo del request.
# ------------------------------------------------------------
@router.put("/{id}")
async def update_schedule(id: int, schedule: ScheduleCreate):
    """Actualiza un bloque de horario (cambio de docente, salón o materia)"""
    return controller.update_schedule(id, schedule)

# ------------------------------------------------------------
# DELETE /schedules/{id}
# Elimina permanentemente un bloque de horario por su ID.
# ------------------------------------------------------------
@router.delete("/{id}")
async def delete_schedule(id: int):
    """Elimina un bloque de horario específico"""
    return controller.delete_schedule(id)