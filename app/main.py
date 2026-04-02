from fastapi import FastAPI
from app.routes.roles_routes import router as roles_router
from app.routes.users_routes import router as users_router
from app.routes.faculties_routes import router as faculties_router
from app.routes.programs_routes import router as programs_router
from app.routes.teacherlevels_routes import router as teacherlevels_router
from app.routes.teachers_routes import router as teachers_router
from app.routes.teacherdegrees_routes import router as teacherdegrees_router
from app.routes.specialties_routes import router as specialties_router
from app.routes.teacherspecialties_routes import router as teacherspecialties_router
from app.routes.subjects_routes import router as subjects_router
from app.routes.academicperiods_routes import router as academicperiods_router
from app.routes.teacheravailability_routes import router as teacheravailability_router
from app.routes.schedules_routes import router as schedules_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roles_router)
app.include_router(users_router)
app.include_router(faculties_router)
app.include_router(programs_router)
app.include_router(teacherlevels_router)
app.include_router(teachers_router)
app.include_router(teacherdegrees_router)
app.include_router(specialties_router)
app.include_router(teacherspecialties_router)
app.include_router(subjects_router)
app.include_router(academicperiods_router)
app.include_router(teacheravailability_router)
app.include_router(schedules_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)