from fastapi import APIRouter
from app.models.users_model import UserCreate, UserResponse
from app.models.login_model import LoginRequest
from app.controllers.users_controller import UsersController
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/users", tags=["Users & Authentication"])
users_controller = UsersController()

class ChangePasswordRequest(BaseModel):
    user_id: int
    current_password: str
    new_password: str

# 1. LOGIN
@router.post("/login")
async def login_user(credentials: LoginRequest):
    """Autenticación para obtener acceso al sistema de horarios"""
    return users_controller.login_user(credentials.email, credentials.password)

# 2. CAMBIAR CONTRASEÑA — debe ir ANTES de /{id} para que FastAPI no lo confunda
@router.put("/change-password")
async def change_password(data: ChangePasswordRequest):
    """Permite al usuario cambiar su propia contraseña"""
    return users_controller.change_password(data.user_id, data.current_password, data.new_password)

# 3. OBTENER DOCENTES
@router.get("/teachers")
async def get_teachers():
    """Lista solo los usuarios con rol docente"""
    return users_controller.get_teachers()

# 4. OBTENER TODOS
@router.get("/", response_model=List[UserResponse])
async def get_users():
    """Lista todos los usuarios registrados en la plataforma"""
    return users_controller.get_users()

# 5. OBTENER UNO
@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int):
    """Busca un usuario por su ID"""
    return users_controller.get_user(id)

# 6. CREAR
@router.post("/")
async def create_user(user: UserCreate):
    """Registra un nuevo usuario en la base de datos de la CUL"""
    return users_controller.create_user(user)

# 7. ACTUALIZAR
@router.put("/{id}")
async def update_user(id: int, user: UserCreate):
    """Actualiza la información de un usuario"""
    return users_controller.update_user(id, user)

# 8. ELIMINAR
@router.delete("/{id}", response_model=UserResponse)
async def delete_user(id: int):
    """Elimina definitivamente un usuario del sistema"""
    return users_controller.delete_user(id)