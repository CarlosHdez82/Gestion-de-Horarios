from fastapi import APIRouter
# Importamos los nuevos moldes especializados
from app.models.faculties_model import FacultyCreate, FacultyResponse
from app.controllers.faculties_controller import FacultiesController

router = APIRouter()

faculties_controller = FacultiesController()

# 1. CREAR: Recibe el molde de creación
@router.post("/create_faculty")
async def create_faculty(faculty: FacultyCreate):
    return faculties_controller.create_faculty(faculty)

# 2. OBTENER UNA: Devuelve el molde de respuesta
@router.get("/get_faculty/{faculties_id}", response_model=FacultyResponse)
async def get_faculty(faculties_id: int):
    return faculties_controller.get_faculty(faculties_id)

# 3. OBTENER TODAS: Devuelve una lista de moldes de respuesta
@router.get("/get_faculties", response_model=list[FacultyResponse])
async def get_faculties():
    return faculties_controller.get_faculties()

# 4. ACTUALIZAR: Recibe creación y devuelve respuesta filtrada
@router.put("/update_faculty/{faculties_id}", response_model=FacultyResponse)
async def update_faculty(faculties_id: int, faculty: FacultyCreate):
    return faculties_controller.update_faculty(faculties_id, faculty)

# 5. ELIMINAR: Nota: No usamos response_model=FacultyResponse porque 
# el controlador ahora devuelve un mensaje de texto simple.
@router.delete("/delete_faculty/{faculties_id}")
async def delete_faculty(faculties_id: int):
    return faculties_controller.delete_faculty(faculties_id)