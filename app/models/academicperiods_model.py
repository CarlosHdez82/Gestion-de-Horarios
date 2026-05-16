# ============================================================
# academicperiods_model.py — Modelos de Periodos Académicos
# ============================================================
# Define la estructura de datos para los periodos académicos
# usando Pydantic. Estos modelos validan automáticamente los
# datos de entrada y salida de la API.
#
# Patrón Base → Create → Response:
# - Base:     campos comunes compartidos por todos los modelos
# - Create:   hereda de Base, se usa para crear/actualizar (POST/PUT)
# - Response: hereda de Base, agrega campos que genera la BD (GET)
# ============================================================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# ------------------------------------------------------------
# Modelo Base — campos comunes del periodo académico
# Todos los demás modelos heredan de esta clase.
# ------------------------------------------------------------
class AcademicPeriodBase(BaseModel):
    name: str                           # Nombre del periodo (ej: "2026-1", "2026-2")
    start_date: Optional[date] = None   # Fecha de inicio (puede omitirse al crear)
    end_date: Optional[date] = None     # Fecha de fin (puede omitirse al crear)
    is_active: bool = True              # Indica si el periodo está vigente actualmente

# ------------------------------------------------------------
# Modelo de Creación — usado en POST y PUT
# Hereda todos los campos de AcademicPeriodBase sin modificaciones.
# El uso de 'pass' indica que no agrega campos adicionales,
# pero mantener la clase separada permite extenderla en el futuro.
# ------------------------------------------------------------
class AcademicPeriodCreate(AcademicPeriodBase):
    pass

# ------------------------------------------------------------
# Modelo de Respuesta — usado en GET
# Extiende Base con los campos que genera automáticamente
# la base de datos al insertar o actualizar un registro.
# ------------------------------------------------------------
class AcademicPeriodResponse(AcademicPeriodBase):
    id: int                                 # Identificador único generado por la BD
    created_at: Optional[datetime] = None   # Fecha y hora de creación del registro
    updated_at: Optional[datetime] = None   # Fecha y hora de la última modificación

    class Config:
        # from_attributes = True permite que Pydantic lea los datos
        # directamente desde objetos ORM (filas de la base de datos),
        # en lugar de requerir un diccionario como entrada.
        from_attributes = True