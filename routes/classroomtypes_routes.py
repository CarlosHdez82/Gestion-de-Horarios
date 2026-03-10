from fastapi import APIRouter
from models.classroomtypes_model import ClassroomTypes
from controllers.classroomtypes_controller import ClassroomTypesController

router = APIRouter()
controller = ClassroomTypesController()

@router.post("/create_classroomtype")
async def create_type(ctype: ClassroomTypes):
    return controller.create_type(ctype)

@router.get("/get_classroomtype/{id}", response_model=ClassroomTypes)
async def get_type(id: int):
    return controller.get_type(id)

@router.get("/get_classroomtypes/")
async def get_types():
    return controller.get_types()

@router.put("/update_classroomtype/{id}", response_model=ClassroomTypes)
async def update_type(id: int, ctype: ClassroomTypes):
    return controller.update_type(id, ctype)

@router.delete("/delete_classroomtype/{id}", response_model=ClassroomTypes)
async def delete_type(id: int):
    return controller.delete_type(id)