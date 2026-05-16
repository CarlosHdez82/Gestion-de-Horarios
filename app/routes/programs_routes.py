# ============================================================
# programs_routes.py — Rutas de Programas Académicos
# ============================================================
# Define los endpoints REST para gestionar los programas
# académicos de la universidad. Un programa pertenece a una
# facultad (ej: Ingeniería de Sistemas → Facultad de Ingeniería).
# ============================================================

from fastapi import APIRouter
from typing import List

# ProgramCreate  → modelo para recibir datos de entrada (POST/PUT)
# ProgramResponse → modelo para estructurar la respuesta (GET)
from app.models.programs_model import ProgramCreate, ProgramResponse
from app.controllers.programs_controller import ProgramsController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/programs" → todas las rutas inician con /programs
# tags=["Programs"]  → agrupa los endpoints en /docs (Swagger UI)
# ------------------------------------------------------------
router = APIRouter(prefix="/programs", tags=["Programs"])

# Instancia del controlador que contiene la lógica de negocio
programs_controller = ProgramsController()

# ------------------------------------------------------------
# POST /programs/
# Crea un nuevo programa académico.
# El cuerpo del request debe cumplir el esquema ProgramCreate.
# ------------------------------------------------------------
@router.post("/")
async def create_program(program: ProgramCreate):
    """Crea un nuevo programa académico"""
    return programs_controller.create_program(program)

# ------------------------------------------------------------
# GET /programs/{id}
# Busca y retorna un programa específico por su ID.
# {id} es un parámetro de ruta que FastAPI extrae de la URL.
# ------------------------------------------------------------
@router.get("/{id}", response_model=ProgramResponse)
async def get_program(id: int):
    """Obtiene los detalles de un programa por su ID"""
    return programs_controller.get_program(id)

# ------------------------------------------------------------
# GET /programs/
# Retorna la lista completa de programas registrados.
# response_model valida y serializa la respuesta automáticamente.
# ------------------------------------------------------------
@router.get("/", response_model=List[ProgramResponse])
async def get_programs():
    """Lista todos los programas registrados en la CUL"""
    return programs_controller.get_programs()

# ------------------------------------------------------------
# PUT /programs/{id}
# Actualiza completamente un programa existente.
# Recibe el ID por la URL y los nuevos datos por el cuerpo del request.
# ------------------------------------------------------------
@router.put("/{id}")
async def update_program(id: int, program: ProgramCreate):
    """Actualiza la información de un programa existente"""
    return programs_controller.update_program(id, program)

# ------------------------------------------------------------
# DELETE /programs/{id}
# Elimina permanentemente un programa por su ID.
# ------------------------------------------------------------
@router.delete("/{id}")
async def delete_program(id: int):
    """Elimina un programa"""
    return programs_controller.delete_program(id)