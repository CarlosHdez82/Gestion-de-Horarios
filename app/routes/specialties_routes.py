from fastapi import APIRouter
from app.models.specialties_model import Specialties
from app.controllers.specialties_controller import SpecialtiesController

router = APIRouter()

specialties_controller = SpecialtiesController()

@router.post("/create_specialty")
async def create_specialty(specialty: Specialties):
    return specialties_controller.create_specialty(specialty)

@router.get("/get_specialty/{specialty_id}", response_model=Specialties)
async def get_specialty(specialty_id: int):
    return specialties_controller.get_specialty(specialty_id)

@router.get("/get_specialties/")
async def get_specialties():
    return specialties_controller.get_specialties()

@router.put("/update_specialty/{specialty_id}", response_model=Specialties)
async def update_specialty(specialty_id: int, specialty: Specialties):
    return specialties_controller.update_specialty(specialty_id, specialty)

@router.delete("/delete_specialty/{specialty_id}", response_model=Specialties)
async def delete_specialty(specialty_id: int):
    return specialties_controller.delete_specialty(specialty_id)