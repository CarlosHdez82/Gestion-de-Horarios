from fastapi import APIRouter
from app.controllers.stats_controller import StatsController

# Definimos el prefijo y tags para la documentación de FastAPI
router = APIRouter(prefix="/stats", tags=["Dashboard"])

stats_controller = StatsController()

@router.get("/summary")
async def read_stats():
    """
    Retorna el resumen global de la CUL:
    Conteo de usuarios, docentes, materias, programas y facultades.
    """
    return stats_controller.get_stats_summary()