# ============================================================
# academicperiods_routes.py — Rutas de Periodos Académicos
# ============================================================
# Define los endpoints REST para gestionar los periodos
# académicos (ej: 2026-1, 2026-2). Sigue el patrón CRUD:
# Create, Read, Update, Delete.
# ============================================================

from fastapi import APIRouter
from typing import List

# AcademicPeriodCreate  → modelo para recibir datos de entrada (POST/PUT)
# AcademicPeriodResponse → modelo para estructurar la respuesta (GET)
from app.models.academicperiods_model import AcademicPeriodCreate, AcademicPeriodResponse
from app.controllers.academicperiods_controller import PeriodsController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/academic-periods" → todas las rutas inician con /academic-periods
# tags=["Academic Periods"]  → agrupa los endpoints en /docs (Swagger UI)
# ------------------------------------------------------------
router = APIRouter(prefix="/academic-periods", tags=["Academic Periods"])

# Instancia del controlador que contiene la lógica de negocio
periods_controller = PeriodsController()

# ------------------------------------------------------------
# GET /academic-periods/
# Retorna la lista completa de periodos académicos registrados.
# response_model valida y serializa la respuesta automáticamente.
# ------------------------------------------------------------
@router.get("/", response_model=List[AcademicPeriodResponse])
async def get_periods():
    """Lista todos los periodos académicos (Ej: 2026-1, 2026-2)"""
    return periods_controller.get_periods()

# ------------------------------------------------------------
# GET /academic-periods/{id}
# Busca y retorna un periodo específico por su ID.
# {id} es un parámetro de ruta que FastAPI extrae de la URL.
# ------------------------------------------------------------
@router.get("/{id}", response_model=AcademicPeriodResponse)
async def get_period(id: int):
    """Obtiene los detalles de un periodo específico"""
    return periods_controller.get_period(id)

# ------------------------------------------------------------
# POST /academic-periods/
# Crea un nuevo periodo académico.
# El cuerpo del request debe cumplir el esquema AcademicPeriodCreate.
# ------------------------------------------------------------
@router.post("/")
async def create_period(period: AcademicPeriodCreate):
    """Registra un nuevo periodo académico en el sistema"""
    return periods_controller.create_period(period)

# ------------------------------------------------------------
# PUT /academic-periods/{id}
# Actualiza completamente un periodo existente.
# Recibe el ID por la URL y los nuevos datos por el cuerpo del request.
# ------------------------------------------------------------
@router.put("/{id}")
async def update_period(id: int, period: AcademicPeriodCreate):
    """Actualiza un periodo (cambio de nombre o estado activo/inactivo)"""
    return periods_controller.update_period(id, period)

# ------------------------------------------------------------
# DELETE /academic-periods/{id}
# Elimina permanentemente un periodo académico por su ID.
# ------------------------------------------------------------
@router.delete("/{id}")
async def delete_period(id: int):
    """Elimina un periodo académico"""
    return periods_controller.delete_period(id)