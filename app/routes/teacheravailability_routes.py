# ============================================================
# teacheravailability_routes.py — Rutas de Disponibilidad Docente
# ============================================================
# Define los endpoints REST para gestionar la disponibilidad
# horaria de los docentes. Cada bloque representa un día y
# franja horaria en que un docente está disponible para dictar
# clases dentro de un periodo académico específico.
# ============================================================

from fastapi import APIRouter
from typing import List

# TeacherAvailabilityCreate  → modelo para recibir datos de entrada (POST/PUT)
# TeacherAvailabilityResponse → modelo para estructurar la respuesta (GET)
# AvailabilityGridItem        → modelo especial para el grid del frontend (Svelte)
from app.models.teacheravailability_model import (
    TeacherAvailabilityCreate,
    TeacherAvailabilityResponse,
    AvailabilityGridItem
)
from app.controllers.teacheravailability_controller import AvailabilityController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/availability"         → todas las rutas inician con /availability
# tags=["Teacher Availability"]  → agrupa los endpoints en /docs (Swagger UI)
# ------------------------------------------------------------
router = APIRouter(prefix="/availability", tags=["Teacher Availability"])

# Instancia del controlador que contiene la lógica de negocio
controller = AvailabilityController()

# ------------------------------------------------------------
# GET /availability/
# Retorna todos los bloques de disponibilidad registrados
# en el sistema, sin filtrar por docente ni periodo.
# ------------------------------------------------------------
@router.get("/", response_model=List[TeacherAvailabilityResponse])
async def get_availabilities():
    """Obtiene la lista global de bloques de disponibilidad registrados"""
    return controller.get_availabilities()

# ------------------------------------------------------------
# GET /availability/teacher/{teacher_id}/{period_id}
# Endpoint especial diseñado para el grid de disponibilidad en Svelte.
# Retorna los bloques ya marcados para un docente en un periodo,
# estructurados en el formato que necesita el componente visual.
# Recibe dos parámetros de ruta: teacher_id y period_id.
# ------------------------------------------------------------
@router.get("/teacher/{teacher_id}/{period_id}", response_model=List[AvailabilityGridItem])
async def get_availability_by_teacher(teacher_id: int, period_id: int):
    """
    Especial para el Grid de Svelte:
    Trae los bloques ya marcados para un docente en un periodo.
    """
    return controller.get_availability_by_teacher(teacher_id, period_id)

# ------------------------------------------------------------
# POST /availability/
# Registra un nuevo bloque de disponibilidad.
# Indica que un docente está disponible en un día y franja
# horaria específicos dentro de un periodo académico.
# El cuerpo del request debe cumplir el esquema TeacherAvailabilityCreate.
# ------------------------------------------------------------
@router.post("/")
async def create_availability(data: TeacherAvailabilityCreate):
    """Registra un bloque de tiempo (día y hora) como disponible"""
    return controller.create_availability(data)

# ------------------------------------------------------------
# PUT /availability/{id}
# Actualiza un bloque de disponibilidad existente.
# Recibe el ID por la URL y los nuevos datos por el cuerpo del request.
# ------------------------------------------------------------
@router.put("/{id}")
async def update_availability(id: int, data: TeacherAvailabilityCreate):
    """Actualiza un bloque de disponibilidad existente"""
    return controller.update_availability(id, data)

# ------------------------------------------------------------
# DELETE /availability/{id}
# Elimina un bloque de disponibilidad específico por su ID.
# ------------------------------------------------------------
@router.delete("/{id}")
async def delete_availability(id: int):
    """Elimina un bloque de disponibilidad específico"""
    return controller.delete_availability(id)

# ------------------------------------------------------------
# DELETE /availability/clear/{teacher_id}/{period_id}
# Limpia completamente el grid de disponibilidad de un docente
# para un periodo específico. Útil cuando el docente necesita
# redefinir toda su disponibilidad desde cero.
# Recibe dos parámetros de ruta: teacher_id y period_id.
# ------------------------------------------------------------
@router.delete("/clear/{teacher_id}/{period_id}")
async def clear_teacher_availability(teacher_id: int, period_id: int):
    """Limpia todo el grid del docente para ese periodo"""
    return controller.clear_teacher_availability(teacher_id, period_id)