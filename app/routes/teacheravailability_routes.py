from fastapi import APIRouter
from models.teacheravailability_model import TeacherAvailability
from controllers.teacheravailability_controller import TeacherAvailabilityController

router = APIRouter()
controller = TeacherAvailabilityController()

@router.post("/create_availability")
async def create_availability(availability: TeacherAvailability):
    return controller.create_availability(availability)

@router.get("/get_availability/{id}", response_model=TeacherAvailability)
async def get_availability(id: int):
    return controller.get_availability(id)

@router.get("/get_availabilities/")
async def get_availabilities():
    return controller.get_availabilities()

@router.put("/update_availability/{id}", response_model=TeacherAvailability)
async def update_availability(id: int, availability: TeacherAvailability):
    return controller.update_availability(id, availability)

@router.delete("/delete_availability/{id}", response_model=TeacherAvailability)
async def delete_availability(id: int):
    return controller.delete_availability(id)