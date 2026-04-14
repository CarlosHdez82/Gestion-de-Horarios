from fastapi import APIRouter
# Importamos los nuevos moldes especializados
from app.models.users_model import UserCreate, UserResponse 
from app.models.login_model import LoginRequest
from app.controllers.users_controller import UsersController

router = APIRouter()

users_controller = UsersController()

# 1. CREAR: Recibe UserCreate (con password plana)
@router.post("/create_user")
async def create_user(user: UserCreate):
    return users_controller.create_user(user)

# 2. OBTENER UNO: Devuelve UserResponse (sin password)
@router.get("/get_user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    return users_controller.get_user(user_id)

# 3. OBTENER TODOS: Devuelve una LISTA de UserResponse
@router.get("/get_users", response_model=list[UserResponse])
async def get_users():
    return users_controller.get_users()

# 4. ACTUALIZAR: Recibe UserCreate y devuelve UserResponse filtrado
@router.put("/update_user/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate):
    return users_controller.update_user(user_id, user)

# 5. ELIMINAR: Devuelve los datos del usuario borrado filtrados
@router.delete("/delete_user/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int):
    return users_controller.delete_user(user_id)

# 6. LOGIN: Se mantiene igual (usa su propio modelo de credenciales)
@router.post("/login")
async def login_user(credentials: LoginRequest):
    return users_controller.login_user(credentials.email, credentials.password)