from fastapi import APIRouter
from app.models.users_model import UserCreate, UserResponse 
from app.models.login_model import LoginRequest
from app.controllers.users_controller import UsersController
from typing import List

# Prefijo limpio y etiquetas para la documentación automática
router = APIRouter(prefix="/users", tags=["Users & Authentication"])

users_controller = UsersController()

# 1. LOGIN: Recibe email y password, devuelve el Token JWT
@router.post("/login")
async def login_user(credentials: LoginRequest):
    """Autenticación para obtener acceso al sistema de horarios"""
    return users_controller.login_user(credentials.email, credentials.password)

# 2. OBTENER TODOS: Lista de usuarios sin mostrar contraseñas
@router.get("/", response_model=List[UserResponse])
async def get_users():
    """Lista todos los usuarios registrados en la plataforma"""
    return users_controller.get_users()

# 3. OBTENER UNO: Detalle de un usuario específico
@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int):
    """Busca un usuario por su ID"""
    return users_controller.get_user(id)

# 4. CREAR: Procesa el registro y hashea la clave en el controlador
@router.post("/")
async def create_user(user: UserCreate):
    """Registra un nuevo usuario en la base de datos de la CUL"""
    return users_controller.create_user(user)

# 5. ACTUALIZAR: Modifica datos existentes
@router.put("/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserCreate):
    """Actualiza la información de un usuario (incluyendo password si se envía)"""
    return users_controller.update_user(id, user)

# 6. ELIMINAR: Borra el registro
@router.delete("/{id}", response_model=UserResponse)
async def delete_user(id: int):
    """Elimina definitivamente un usuario del sistema"""
    return users_controller.delete_user(id)