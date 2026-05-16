# ============================================================
# faculties_model.py — Modelos de Facultades
# ============================================================
# Define la estructura de datos para las facultades
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
from datetime import datetime

# ------------------------------------------------------------
# Modelo Base — campos comunes de la facultad
# Todos los demás modelos heredan de esta clase.
# ------------------------------------------------------------
class FacultyBase(BaseModel):
    name: str               # Nombre de la facultad (ej: "Facultad de Ingeniería")
    is_active: bool = True  # Indica si la facultad está activa en el sistema

# ------------------------------------------------------------
# Modelo de Creación — usado en POST y PUT
# Hereda todos los campos de FacultyBase sin modificaciones.
# El uso de 'pass' indica que no agrega campos adicionales,
# pero mantener la clase separada permite extenderla en el futuro.
# ------------------------------------------------------------
class FacultyCreate(FacultyBase):
    pass

# ------------------------------------------------------------
# Modelo de Respuesta — usado en GET
# Extiende Base con los campos que genera automáticamente
# la base de datos al insertar o actualizar un registro.
# ------------------------------------------------------------
class FacultyResponse(FacultyBase):
    id: int                                 # Identificador único generado por la BD
    created_at: Optional[datetime] = None   # Fecha y hora de creación del registro
    updated_at: Optional[datetime] = None   # Fecha y hora de la última modificación

    class Config:
        # from_attributes = True permite que Pydantic lea los datos
        # directamente desde objetos ORM (filas de la base de datos),
        # en lugar de requerir un diccionario como entrada.
        from_attributes = True