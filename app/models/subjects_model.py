# ============================================================
# subjects_model.py — Modelos de Materias
# ============================================================
# Define la estructura de datos para las materias académicas
# usando Pydantic. Una materia pertenece a un programa y tiene
# atributos como nombre, código y cantidad de créditos.
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
# Modelo Base — campos comunes de la materia
# Todos los demás modelos heredan de esta clase.
# ------------------------------------------------------------
class SubjectBase(BaseModel):
    name: str                       # Nombre de la materia (ej: "Cálculo Diferencial")
    credits: int                    # Número de créditos académicos de la materia
    program_id: int                 # ID del programa al que pertenece la materia
                                    # Representa la relación entre materia y programa en la BD
    code: Optional[str] = None      # Código interno de la materia (ej: "MAT101")
                                    # Opcional porque puede asignarse después de la creación

# ------------------------------------------------------------
# Modelo de Creación — usado en POST y PUT
# Hereda todos los campos de SubjectBase sin modificaciones.
# El uso de 'pass' indica que no agrega campos adicionales,
# pero mantener la clase separada permite extenderla en el futuro.
# ------------------------------------------------------------
class SubjectCreate(SubjectBase):
    pass

# ------------------------------------------------------------
# Modelo de Respuesta — usado en GET
# Extiende Base con campos generados por la BD y datos adicionales
# obtenidos mediante JOIN con la tabla de programas.
# ------------------------------------------------------------
class SubjectResponse(SubjectBase):
    id: int                                 # Identificador único generado por la BD
    program_name: Optional[str] = None      # Nombre del programa obtenido por JOIN,
                                            # evita que el frontend haga una segunda consulta
    created_at: Optional[datetime] = None   # Fecha y hora de creación del registro
    updated_at: Optional[datetime] = None   # Fecha y hora de la última modificación

    class Config:
        # from_attributes = True permite que Pydantic lea los datos
        # directamente desde objetos ORM (filas de la base de datos),
        # en lugar de requerir un diccionario como entrada.
        from_attributes = True