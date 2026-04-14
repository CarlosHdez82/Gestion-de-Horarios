from fastapi import APIRouter
from app.models.schedules_model import Schedules
from app.controllers.schedules_controller import SchedulesController

router = APIRouter()
controller = SchedulesController()

@router.post("/create_schedule")
async def create_schedule(schedule: Schedules):
    return controller.create_schedule(schedule)

@router.get("/get_schedules", response_model=list[Schedules])
async def get_schedules():
    return controller.get_schedules()

@router.put("/update_schedule/{id}")
async def update_schedule(id: int, schedule: Schedules):
    return controller.update_schedule(id, schedule)

@router.delete("/delete_schedule/{id}")
async def delete_schedule(id: int):
    return controller.delete_schedule(id)