from fastapi import APIRouter
from typing import List
from app.models.teacheravailability_model import TeacherAvailability
from app.controllers.teacheravailability_controller import AvailabilityController

router = APIRouter()
controller = AvailabilityController()

@router.get("/get_availabilities", response_model=List[TeacherAvailability])
async def get_availabilities():
    return controller.get_availabilities()

@router.get("/get_availability/{id}", response_model=TeacherAvailability)
async def get_availability(id: int):
    return controller.get_availability(id)

@router.post("/create_availability")
async def create_availability(data: TeacherAvailability):
    return controller.create_availability(data)

@router.put("/update_availability/{id}")
async def update_availability(id: int, data: TeacherAvailability):
    return controller.update_availability(id, data)

@router.delete("/delete_availability/{id}")
async def delete_availability(id: int):
    return controller.delete_availability(id)