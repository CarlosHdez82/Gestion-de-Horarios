from fastapi import APIRouter
from typing import List
# Importamos los nombres exactos: Create para la entrada, Response para la salida
from app.models.academicperiods_model import AcademicPeriodCreate, AcademicPeriodResponse 
from app.controllers.academicperiods_controller import PeriodsController

router = APIRouter(prefix="/academic-periods", tags=["Academic Periods"])
periods_controller = PeriodsController()

@router.get("/", response_model=List[AcademicPeriodResponse])
async def get_periods():
    """Lista todos los periodos académicos (Ej: 2026-1, 2026-2)"""
    return periods_controller.get_periods()

@router.get("/{id}", response_model=AcademicPeriodResponse)
async def get_period(id: int):
    """Obtiene los detalles de un periodo específico"""
    return periods_controller.get_period(id)

@router.post("/")
async def create_period(period: AcademicPeriodCreate):
    """Registra un nuevo periodo académico en el sistema"""
    return periods_controller.create_period(period)

@router.put("/{id}")
async def update_period(id: int, period: AcademicPeriodCreate):
    """Actualiza un periodo (cambio de nombre o estado activo/inactivo)"""
    return periods_controller.update_period(id, period)

@router.delete("/{id}")
async def delete_period(id: int):
    """Elimina un periodo académico"""
    return periods_controller.delete_period(id)