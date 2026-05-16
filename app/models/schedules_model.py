# ============================================================
# schedules_model.py — Modelos de Horarios
# ============================================================
# Define la estructura de datos para los horarios académicos
# usando Pydantic. Un horario representa la asignación de una
# materia a un docente en un día, franja horaria y grupo
# específicos dentro de un periodo académico.
#
# Patrón Base → Create → Response:
# - Base:     campos comunes compartidos por todos los modelos
# - Create:   hereda de Base, se usa para crear/actualizar (POST/PUT)
# - Response: hereda de Base, agrega campos que genera la BD (GET)
# ============================================================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ------------------------------------------------------------
# Modelo Base — campos comunes del horario
# Todos los demás modelos heredan de esta clase.
# Los campos de tipo _id representan claves foráneas que
# relacionan el horario con otras tablas de la BD.
# ------------------------------------------------------------
class ScheduleBase(BaseModel):
    teacher_id: int         # ID del docente asignado a la clase
    subject_id: int         # ID de la materia que se dictará
    period_id: int          # ID del periodo académico (ej: 2026-1)
    day_of_week: str        # Día de la semana (ej: "Lunes", "Martes")
    block_label: str        # Franja horaria (ej: "7:00 - 9:00", "Bloque 1")
    group_code: str = "A"   # Código del grupo, por defecto "A"

# ------------------------------------------------------------
# Modelo de Creación — usado en POST y PUT
# Hereda todos los campos de ScheduleBase sin modificaciones.
# El uso de 'pass' indica que no agrega campos adicionales,
# pero mantener la clase separada permite extenderla en el futuro.
# ------------------------------------------------------------
class ScheduleCreate(ScheduleBase):
    pass

# ------------------------------------------------------------
# Modelo de Respuesta — usado en GET
# Extiende Base con campos generados por la BD y datos adicionales
# obtenidos mediante JOINs con las tablas relacionadas.
# Incluye los nombres legibles de docente, materia y periodo
# para evitar que el frontend tenga que hacer consultas adicionales.
# ------------------------------------------------------------
class ScheduleResponse(ScheduleBase):
    id: int                                 # Identificador único generado por la BD
    teacher_name: Optional[str] = None      # Nombre del docente obtenido por JOIN
    subject_name: Optional[str] = None      # Nombre de la materia obtenido por JOIN
    subject_code: Optional[str] = None      # Código de la materia obtenido por JOIN
    period_name: Optional[str] = None       # Nombre del periodo obtenido por JOIN
    created_at: Optional[datetime] = None   # Fecha y hora de creación del registro
    updated_at: Optional[datetime] = None   # Fecha y hora de la última modificación

    class Config:
        # from_attributes = True permite que Pydantic lea los datos
        # directamente desde objetos ORM (filas de la base de datos),
        # en lugar de requerir un diccionario como entrada.
        from_attributes = True