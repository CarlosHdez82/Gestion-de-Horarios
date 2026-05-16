# ============================================================
# stats_routes.py — Rutas de Estadísticas / Dashboard
# ============================================================
# Define los endpoints para consultar métricas y resúmenes
# generales del sistema. Estos datos alimentan el dashboard
# principal de la aplicación con conteos globales de la CUL.
# ============================================================

from fastapi import APIRouter
from app.controllers.stats_controller import StatsController

# ------------------------------------------------------------
# Configuración del Router
# prefix="/stats"      → todas las rutas inician con /stats
# tags=["Dashboard"]   → agrupa los endpoints en /docs (Swagger UI)
#                        bajo la sección "Dashboard"
# ------------------------------------------------------------
router = APIRouter(prefix="/stats", tags=["Dashboard"])

# Instancia del controlador que contiene la lógica de negocio
stats_controller = StatsController()

# ------------------------------------------------------------
# GET /stats/summary
# Retorna un resumen con los conteos globales del sistema:
# total de usuarios, docentes, materias, programas y facultades.
# Es el endpoint principal que alimenta las tarjetas del dashboard.
# ------------------------------------------------------------
@router.get("/summary")
async def read_stats():
    """
    Retorna el resumen global de la CUL:
    Conteo de usuarios, docentes, materias, programas y facultades.
    """
    return stats_controller.get_stats_summary()