# ============================================================
# faculties_routes.py — Rutas de Facultades
# ============================================================
# Define los endpoints REST para gestionar las facultades
# de la universidad. Una facultad agrupa programas académicos
# (ej: Facultad de Ingeniería, Facultad de Ciencias de la Salud).
# ============================================================

from fastapi import APIRouter
from typing import List

# FacultyCreate  → modelo para recibir datos de entrada (POST/PUT)
# FacultyResponse → modelo para estructurar la respuesta (GET)
from app.models.faculties_model import FacultyCreate, FacultyResponse
from app.controllers.faculties_controller import FacultiesController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/faculties" → todas las rutas inician con /faculties
# tags=["Faculties"]  → agrupa los endpoints en /docs (Swagger UI)
# ------------------------------------------------------------
router = APIRouter(prefix="/faculties", tags=["Faculties"])

# Instancia del controlador que contiene la lógica de negocio
faculties_controller = FacultiesController()

# ------------------------------------------------------------
# POST /faculties/
# Crea una nueva facultad.
# El cuerpo del request debe cumplir el esquema FacultyCreate.
# ------------------------------------------------------------
@router.post("/")
async def create_faculty(faculty: FacultyCreate):
    """Registra una nueva facultad en la CUL"""
    return faculties_controller.create_faculty(faculty)

# ------------------------------------------------------------
# GET /faculties/{id}
# Busca y retorna una facultad específica por su ID.
# {id} es un parámetro de ruta que FastAPI extrae de la URL.
# ------------------------------------------------------------
@router.get("/{id}", response_model=FacultyResponse)
async def get_faculty(id: int):
    """Obtiene la información de una facultad específica"""
    return faculties_controller.get_faculty(id)

# ------------------------------------------------------------
# GET /faculties/
# Retorna la lista completa de facultades registradas.
# response_model valida y serializa la respuesta automáticamente.
# ------------------------------------------------------------
@router.get("/", response_model=List[FacultyResponse])
async def get_faculties():
    """Lista todas las facultades registradas"""
    return faculties_controller.get_faculties()

# ------------------------------------------------------------
# PUT /faculties/{id}
# Actualiza completamente una facultad existente.
# Recibe el ID por la URL y los nuevos datos por el cuerpo del request.
# ------------------------------------------------------------
@router.put("/{id}", response_model=FacultyResponse)
async def update_faculty(id: int, faculty: FacultyCreate):
    """Actualiza el nombre o estado de una facultad"""
    return faculties_controller.update_faculty(id, faculty)

# ------------------------------------------------------------
# DELETE /faculties/{id}
# Elimina permanentemente una facultad por su ID.
# Nota: solo es posible si la facultad no tiene programas asociados.
# ------------------------------------------------------------
@router.delete("/{id}")
async def delete_faculty(id: int):
    """Elimina una facultad (Si no tiene programas asociados)"""
    return faculties_controller.delete_faculty(id)