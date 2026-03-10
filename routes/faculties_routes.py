from fastapi import APIRouter
from models.faculties_model import Faculties
from controllers.faculties_controller import FacultiesController

router = APIRouter()

faculties_controller = FacultiesController()

@router.post("/create_faculty")
async def create_faculty(faculty: Faculties):
    return faculties_controller.create_faculty(faculty)

@router.get("/get_faculty/{faculties_id}", response_model=Faculties)
async def get_faculty(faculties_id: int):
    return faculties_controller.get_faculty(faculties_id)

@router.get("/get_faculties/")
async def get_faculties():
    return faculties_controller.get_faculties()

@router.put("/update_faculty/{faculties_id}", response_model=Faculties)
async def update_faculty(faculties_id: int, faculty: Faculties):
    return faculties_controller.update_faculty(faculties_id, faculty)

@router.delete("/delete_faculty/{faculties_id}", response_model=Faculties)
async def delete_faculty(faculties_id: int):
    return faculties_controller.delete_faculty(faculties_id)