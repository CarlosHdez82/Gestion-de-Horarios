from fastapi import APIRouter
from app.models.academicperiods_model import AcademicPeriods
from app.controllers.academicperiods_controller import PeriodsController

router = APIRouter()

academicperiods_controller = PeriodsController()

@router.post("/create_period")
async def create_period(period: AcademicPeriods):
    return academicperiods_controller.create_period(period)

@router.get("/get_period/{id}", response_model=AcademicPeriods)
async def get_period(id: int):
    return academicperiods_controller.get_period(id)

@router.get("/get_periods")
async def get_periods():
    return academicperiods_controller.get_periods()

@router.put("/update_period/{id}", response_model=AcademicPeriods)
async def update_period(id: int, period: AcademicPeriods):
    return academicperiods_controller.update_period(id, period)

@router.delete("/delete_period/{id}", response_model=AcademicPeriods)
async def delete_period(id: int):
    return academicperiods_controller.delete_period(id)