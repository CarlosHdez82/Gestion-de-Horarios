# ============================================================
# teacheravailability_model.py — Modelos de Disponibilidad Docente
# ============================================================
# Define la estructura de datos para la disponibilidad horaria
# de los docentes usando Pydantic. Cada registro representa un
# bloque de tiempo en que un docente está disponible para dictar
# clases dentro de un periodo académico específico.
#
# Patrón Base → Create → Response + modelo especial para el grid:
# - Base:             campos comunes compartidos por todos los modelos
# - Create:           hereda de Base, se usa para crear/actualizar (POST/PUT)
# - Response:         hereda de Base, agrega campos que genera la BD (GET)
# - AvailabilityGridItem: modelo simplificado para el grid visual de Svelte
# ============================================================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ------------------------------------------------------------
# 1. Modelo Base — campos comunes de disponibilidad
# Todos los demás modelos heredan de esta clase.
# ------------------------------------------------------------
class TeacherAvailabilityBase(BaseModel):
    teacher_id: int     # ID del docente al que pertenece el bloque de disponibilidad
    period_id: int      # ID del periodo académico al que aplica la disponibilidad
    day_of_week: str    # Día de la semana (ej: "Lunes", "Martes", "Miércoles")
    block_label: str    # Franja horaria del bloque (ej: "06:00 - 08:00")

# ------------------------------------------------------------
# 2. Modelo de Creación — usado en POST y PUT
# Hereda todos los campos de TeacherAvailabilityBase sin modificaciones.
# El uso de 'pass' indica que no agrega campos adicionales,
# pero mantener la clase separada permite extenderla en el futuro.
# ------------------------------------------------------------
class TeacherAvailabilityCreate(TeacherAvailabilityBase):
    pass

# ------------------------------------------------------------
# 3. Modelo de Respuesta — usado en GET
# Extiende Base con campos generados por la BD y datos adicionales
# obtenidos mediante JOINs con las tablas de docentes y periodos.
# Incluye nombres legibles para evitar consultas adicionales
# desde el frontend.
# ------------------------------------------------------------
class TeacherAvailabilityResponse(TeacherAvailabilityBase):
    id: int                                 # Identificador único generado por la BD
    teacher_name: Optional[str] = None      # Nombre del docente obtenido por JOIN
    period_name: Optional[str] = None       # Nombre del periodo obtenido por JOIN
    created_at: Optional[datetime] = None   # Fecha y hora de creación del registro
    updated_at: Optional[datetime] = None   # Fecha y hora de la última modificación

# ------------------------------------------------------------
# 4. Modelo especial para el Grid de Disponibilidad (Svelte)
# Versión simplificada usada por el endpoint:
# GET /availability/teacher/{teacher_id}/{period_id}
# Retorna solo los campos que necesita el componente visual
# del grid para marcar las celdas ya seleccionadas por el docente.
# ------------------------------------------------------------
class AvailabilityGridItem(BaseModel):
    id: int     # ID del bloque, necesario para poder eliminarlo desde el grid
    day: str    # Día de la semana del bloque marcado
    block: str  # Franja horaria del bloque marcado

    class Config:
        # from_attributes = True permite que Pydantic lea los datos
        # directamente desde objetos ORM (filas de la base de datos),
        # en lugar de requerir un diccionario como entrada.
        from_attributes = True