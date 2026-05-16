# ============================================================
# users_routes.py — Rutas de Usuarios y Autenticación
# ============================================================
# Define los endpoints REST para gestionar usuarios del sistema
# y manejar la autenticación. Combina operaciones CRUD con
# funcionalidades especiales como login y cambio de contraseña.
#
# IMPORTANTE: El orden de las rutas importa en FastAPI.
# Las rutas estáticas (/login, /change-password, /teachers)
# deben declararse ANTES de las rutas dinámicas (/{id}),
# de lo contrario FastAPI intentará interpretar "login" o
# "teachers" como un ID numérico y fallará.
# ============================================================

from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

# UserCreate  → modelo para recibir datos de entrada (POST/PUT)
# UserResponse → modelo para estructurar la respuesta (GET)
from app.models.users_model import UserCreate, UserResponse

# LoginRequest → modelo con email y password para autenticación
from app.models.login_model import LoginRequest
from app.controllers.users_controller import UsersController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/users"                    → todas las rutas inician con /users
# tags=["Users & Authentication"]    → agrupa los endpoints en /docs
# ------------------------------------------------------------
router = APIRouter(prefix="/users", tags=["Users & Authentication"])

# Instancia del controlador que contiene la lógica de negocio
users_controller = UsersController()

# ------------------------------------------------------------
# Modelo interno para cambio de contraseña
# Se define aquí porque es exclusivo de este módulo y no
# requiere un archivo de modelo separado.
# ------------------------------------------------------------
class ChangePasswordRequest(BaseModel):
    user_id: int           # ID del usuario que cambia su contraseña
    current_password: str  # Contraseña actual para verificar identidad
    new_password: str      # Nueva contraseña a establecer

# ------------------------------------------------------------
# 1. POST /users/login
# Autentica un usuario con email y contraseña.
# Retorna un token JWT si las credenciales son válidas.
# Es el punto de entrada al sistema para todos los usuarios.
# ------------------------------------------------------------
@router.post("/login")
async def login_user(credentials: LoginRequest):
    """Autenticación para obtener acceso al sistema de horarios"""
    return users_controller.login_user(credentials.email, credentials.password)

# ------------------------------------------------------------
# 2. PUT /users/change-password
# Permite a un usuario cambiar su propia contraseña.
# Declarada ANTES de /{id} para evitar conflictos de rutas,
# ya que FastAPI resuelve rutas en el orden en que se registran.
# ------------------------------------------------------------
@router.put("/change-password")
async def change_password(data: ChangePasswordRequest):
    """Permite al usuario cambiar su propia contraseña"""
    return users_controller.change_password(
        data.user_id,
        data.current_password,
        data.new_password
    )

# ------------------------------------------------------------
# 3. GET /users/teachers
# Retorna únicamente los usuarios con rol docente.
# Declarada ANTES de /{id} para evitar que FastAPI interprete
# "teachers" como un parámetro numérico de ID.
# ------------------------------------------------------------
@router.get("/teachers")
async def get_teachers():
    """Lista solo los usuarios con rol docente"""
    return users_controller.get_teachers()

# ------------------------------------------------------------
# 4. GET /users/
# Retorna la lista completa de usuarios registrados.
# response_model valida y serializa la respuesta automáticamente.
# ------------------------------------------------------------
@router.get("/", response_model=List[UserResponse])
async def get_users():
    """Lista todos los usuarios registrados en la plataforma"""
    return users_controller.get_users()

# ------------------------------------------------------------
# 5. GET /users/{id}
# Busca y retorna un usuario específico por su ID.
# {id} es un parámetro de ruta que FastAPI extrae de la URL.
# ------------------------------------------------------------
@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int):
    """Busca un usuario por su ID"""
    return users_controller.get_user(id)

# ------------------------------------------------------------
# 6. POST /users/
# Crea un nuevo usuario en el sistema.
# El cuerpo del request debe cumplir el esquema UserCreate.
# ------------------------------------------------------------
@router.post("/")
async def create_user(user: UserCreate):
    """Registra un nuevo usuario en la base de datos de la CUL"""
    return users_controller.create_user(user)

# ------------------------------------------------------------
# 7. PUT /users/{id}
# Actualiza completamente la información de un usuario existente.
# Recibe el ID por la URL y los nuevos datos por el cuerpo del request.
# ------------------------------------------------------------
@router.put("/{id}")
async def update_user(id: int, user: UserCreate):
    """Actualiza la información de un usuario"""
    return users_controller.update_user(id, user)

# ------------------------------------------------------------
# 8. DELETE /users/{id}
# Elimina permanentemente un usuario del sistema por su ID.
# response_model retorna los datos del usuario eliminado
# como confirmación de la operación.
# ------------------------------------------------------------
@router.delete("/{id}", response_model=UserResponse)
async def delete_user(id: int):
    """Elimina definitivamente un usuario del sistema"""
    return users_controller.delete_user(id)