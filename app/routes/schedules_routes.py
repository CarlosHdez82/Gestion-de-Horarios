from fastapi import APIRouter
from app.models.schedules_model import Schedules
from app.controllers.schedules_controller import SchedulesController

router = APIRouter()
controller = SchedulesController()

@router.post("/create_schedule")
async def create_schedule(schedule: Schedules):
    return controller.create_schedule(schedule)

@router.get("/get_schedule/{id}", response_model=Schedules)
async def get_schedule(id: int):
    return controller.get_schedule(id)

@router.get("/get_schedules/")
async def get_schedules():
    return controller.get_schedules()

@router.put("/update_schedule/{id}", response_model=Schedules)
async def update_schedule(id: int, schedule: Schedules):
    return controller.update_schedule(id, schedule)

@router.delete("/delete_schedule/{id}", response_model=Schedules)
async def delete_schedule(id: int):
    return controller.delete_schedule(id)