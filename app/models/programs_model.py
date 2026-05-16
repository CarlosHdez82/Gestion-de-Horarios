# ============================================================
# programs_model.py — Modelos de Programas Académicos
# ============================================================
# Define la estructura de datos para los programas académicos
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
# Modelo Base — campos comunes del programa académico
# Todos los demás modelos heredan de esta clase.
# ------------------------------------------------------------
class ProgramBase(BaseModel):
    name: str           # Nombre del programa (ej: "Ingeniería de Sistemas")
    faculty_id: int     # ID de la facultad a la que pertenece el programa
                        # Representa la relación entre programa y facultad en la BD

# ------------------------------------------------------------
# Modelo de Creación — usado en POST y PUT
# Hereda todos los campos de ProgramBase sin modificaciones.
# El uso de 'pass' indica que no agrega campos adicionales,
# pero mantener la clase separada permite extenderla en el futuro.
# ------------------------------------------------------------
class ProgramCreate(ProgramBase):
    pass

# ------------------------------------------------------------
# Modelo de Respuesta — usado en GET
# Extiende Base con campos generados por la BD y datos adicionales
# obtenidos mediante JOIN con la tabla de facultades.
# ------------------------------------------------------------
class ProgramResponse(ProgramBase):
    id: int                                 # Identificador único generado por la BD
    is_active: bool = True                  # Indica si el programa está activo
    faculty_name: Optional[str] = None      # Nombre de la facultad obtenido por JOIN,
                                            # evita que el frontend haga una segunda consulta
    created_at: Optional[datetime] = None   # Fecha y hora de creación del registro
    updated_at: Optional[datetime] = None   # Fecha y hora de la última modificación

    class Config:
        # from_attributes = True permite que Pydantic lea los datos
        # directamente desde objetos ORM (filas de la base de datos),
        # en lugar de requerir un diccionario como entrada.
        from_attributes = True