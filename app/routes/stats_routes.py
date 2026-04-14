from fastapi import APIRouter
from app.controllers.stats_controller import StatsController

router = APIRouter()

stats_controller = StatsController()

@router.get("/stats/summary")
def read_stats():
    return stats_controller.get_stats_summary()