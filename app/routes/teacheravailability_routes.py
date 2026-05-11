from fastapi import APIRouter
from typing import List
# Importamos los nombres exactos de tu modelo de disponibilidad
from app.models.teacheravailability_model import TeacherAvailabilityCreate, TeacherAvailabilityResponse, AvailabilityGridItem
from app.controllers.teacheravailability_controller import AvailabilityController

# Prefijo estandarizado para la gestión de disponibilidad
router = APIRouter(prefix="/availability", tags=["Teacher Availability"])
controller = AvailabilityController()

@router.get("/", response_model=List[TeacherAvailabilityResponse])
async def get_availabilities():
    """Obtiene la lista global de bloques de disponibilidad registrados"""
    return controller.get_availabilities()

@router.get("/teacher/{teacher_id}/{period_id}", response_model=List[AvailabilityGridItem])
async def get_availability_by_teacher(teacher_id: int, period_id: int):
    """
    Especial para el Grid de Svelte: 
    Trae los bloques ya marcados para un docente en un periodo.
    """
    return controller.get_availability_by_teacher(teacher_id, period_id)

@router.post("/")
async def create_availability(data: TeacherAvailabilityCreate):
    """Registra un bloque de tiempo (día y hora) como disponible"""
    return controller.create_availability(data)

@router.put("/{id}")
async def update_availability(id: int, data: TeacherAvailabilityCreate):
    """Actualiza un bloque de disponibilidad existente"""
    return controller.update_availability(id, data)

@router.delete("/{id}")
async def delete_availability(id: int):
    """Elimina un bloque de disponibilidad específico"""
    return controller.delete_availability(id)

@router.delete("/clear/{teacher_id}/{period_id}")
async def clear_teacher_availability(teacher_id: int, period_id: int):
    """Limpia todo el grid del docente para ese periodo"""
    return controller.clear_teacher_availability(teacher_id, period_id)