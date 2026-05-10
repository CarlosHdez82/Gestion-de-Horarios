from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importación de Routers
from app.routes.roles_routes import router as roles_router
from app.routes.users_routes import router as users_router
from app.routes.faculties_routes import router as faculties_router
from app.routes.programs_routes import router as programs_router
from app.routes.subjects_routes import router as subjects_router
from app.routes.academicperiods_routes import router as academicperiods_router
from app.routes.teacheravailability_routes import router as teacheravailability_router
from app.routes.schedules_routes import router as schedules_router
from app.routes.stats_routes import router as stats_router

app = FastAPI(
    title="API Gestión de Horarios CUL",
    description="Sistema de gestión de disponibilidad docente y horarios académicos",
    version="1.0.0"
)

# Configuración de CORS
# Esto permite que Svelte (5173) y otros entornos se comuniquen con FastAPI
origins = [
    "http://localhost:5173",    # SvelteKit / Vite
    "http://127.0.0.1:5173",
    "http://localhost:3000",    # Otros entornos de React/Next
    "http://127.0.0.1:5500",    # Live Server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En desarrollo puedes dejar "*", en producción usa 'origins'
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Rutas
app.include_router(roles_router)
app.include_router(users_router)
app.include_router(faculties_router)
app.include_router(programs_router)
app.include_router(subjects_router)
app.include_router(academicperiods_router)
app.include_router(teacheravailability_router)
app.include_router(schedules_router)
app.include_router(stats_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "status": "online",
        "message": "Bienvenido a la API de Gestión de Horarios de la Universidad CUL",
        "docs": "/docs"
    }

if __name__ == "__main__":
    # Host 0.0.0.0 es necesario para despliegues en la nube como Render
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)