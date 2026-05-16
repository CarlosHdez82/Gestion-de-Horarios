# ============================================================
# subjects_routes.py — Rutas de Materias
# ============================================================
# Define los endpoints REST para gestionar las materias
# académicas de la universidad. Una materia pertenece a un
# programa y tiene atributos como código, nombre y créditos.
# ============================================================

from fastapi import APIRouter
from typing import List

# SubjectCreate  → modelo para recibir datos de entrada (POST/PUT)
# SubjectResponse → modelo para estructurar la respuesta (GET)
from app.models.subjects_model import SubjectCreate, SubjectResponse
from app.controllers.subjects_controller import SubjectsController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/subjects" → todas las rutas inician con /subjects
# tags=["Subjects"]  → agrupa los endpoints en /docs (Swagger UI)
# ------------------------------------------------------------
router = APIRouter(prefix="/subjects", tags=["Subjects"])

# Instancia del controlador que contiene la lógica de negocio
subjects_controller = SubjectsController()

# ------------------------------------------------------------
# GET /subjects/
# Retorna la lista completa de materias registradas.
# response_model valida y serializa la respuesta automáticamente.
# ------------------------------------------------------------
@router.get("/", response_model=List[SubjectResponse])
async def get_subjects():
    """Lista todas las materias de la universidad"""
    return subjects_controller.get_subjects()

# ------------------------------------------------------------
# GET /subjects/{id}
# Busca y retorna una materia específica por su ID.
# {id} es un parámetro de ruta que FastAPI extrae de la URL.
# ------------------------------------------------------------
@router.get("/{id}", response_model=SubjectResponse)
async def get_subject(id: int):
    """Obtiene una materia específica por su ID"""
    return subjects_controller.get_subject(id)

# ------------------------------------------------------------
# POST /subjects/
# Crea una nueva materia en el sistema.
# El cuerpo del request debe cumplir el esquema SubjectCreate
# (código, nombre, créditos y programa al que pertenece).
# ------------------------------------------------------------
@router.post("/")
async def create_subject(subject: SubjectCreate):
    """Registra una nueva materia (usa código, nombre, créditos y programa)"""
    return subjects_controller.create_subject(subject)

# ------------------------------------------------------------
# PUT /subjects/{id}
# Actualiza completamente una materia existente.
# Recibe el ID por la URL y los nuevos datos por el cuerpo del request.
# ------------------------------------------------------------
@router.put("/{id}")
async def update_subject(id: int, subject: SubjectCreate):
    """Actualiza los datos de una materia existente"""
    return subjects_controller.update_subject(id, subject)

# ------------------------------------------------------------
# DELETE /subjects/{id}
# Elimina permanentemente una materia por su ID.
# ------------------------------------------------------------
@router.delete("/{id}")
async def delete_subject(id: int):
    """Elimina una materia del sistema"""
    return subjects_controller.delete_subject(id)