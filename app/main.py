# ============================================================
# main.py — Punto de entrada principal de la API
# ============================================================
# Este archivo inicializa la aplicación FastAPI, configura
# los middlewares y registra todas las rutas disponibles.
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ------------------------------------------------------------
# Importación de Routers
# Cada router agrupa las rutas de un módulo específico.
# Se importan con un alias para evitar conflictos de nombres.
# ------------------------------------------------------------
from app.routes.roles_routes import router as roles_router
from app.routes.users_routes import router as users_router
from app.routes.faculties_routes import router as faculties_router
from app.routes.programs_routes import router as programs_router
from app.routes.subjects_routes import router as subjects_router
from app.routes.academicperiods_routes import router as academicperiods_router
from app.routes.teacheravailability_routes import router as teacheravailability_router
from app.routes.schedules_routes import router as schedules_router
from app.routes.stats_routes import router as stats_router

# ------------------------------------------------------------
# Instancia principal de la aplicación FastAPI
# title, description y version aparecen en /docs (Swagger UI)
# ------------------------------------------------------------
app = FastAPI(
    title="API Gestión de Horarios CUL",
    description="Sistema de gestión de disponibilidad docente y horarios académicos",
    version="1.0.0"
)

# ------------------------------------------------------------
# Configuración de CORS (Cross-Origin Resource Sharing)
# CORS controla qué dominios externos pueden hacer peticiones
# a esta API. Sin esto, el navegador bloquea las solicitudes
# del frontend por razones de seguridad.
# ------------------------------------------------------------
origins = [
    "http://localhost:5173",    # SvelteKit / Vite (desarrollo)
    "http://127.0.0.1:5173",
    "http://localhost:3000",    # React / Next.js
    "http://127.0.0.1:5500",    # Live Server (VS Code)
    "https://ghdd.netlify.app",  # Agrega aquí otros orígenes permitidos (producción, staging, etc.)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Permite los orígenes especificados
    allow_credentials=True,     # Permite envío de cookies y credenciales
    allow_methods=["*"],        # Permite todos los métodos HTTP (GET, POST, PUT, DELETE...)
    allow_headers=["*"],        # Permite todos los encabezados HTTP
)

# ------------------------------------------------------------
# Registro de Routers
# Cada router añade a la app las rutas de su módulo.
# FastAPI los unifica bajo una sola aplicación.
# ------------------------------------------------------------
app.include_router(roles_router)
app.include_router(users_router)
app.include_router(faculties_router)
app.include_router(programs_router)
app.include_router(subjects_router)
app.include_router(academicperiods_router)
app.include_router(teacheravailability_router)
app.include_router(schedules_router)
app.include_router(stats_router)

# ------------------------------------------------------------
# Ruta raíz — GET /
# Sirve como endpoint de verificación (health check).
# Retorna un JSON con el estado actual de la API.
# ------------------------------------------------------------
@app.get("/", tags=["Root"])
def root():
    return {
        "status": "online",
        "message": "Bienvenido a la API de Gestión de Horarios de la Universidad CUL",
        "docs": "/docs"         # URL de la documentación interactiva
    }

# ------------------------------------------------------------
# Punto de entrada al ejecutar el archivo directamente
# Se usa cuando corres: python app/main.py
# host="0.0.0.0" expone la API en todas las interfaces de red,
# necesario para despliegues en la nube (Render, Railway, etc.)
# ------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)