# ============================================================
# subjects_controller.py — Controlador de Materias
# ============================================================
# Contiene la lógica de negocio para gestionar las materias
# académicas. Usa LEFT JOIN con la tabla de programas para
# retornar el nombre del programa junto con cada materia,
# evitando consultas adicionales desde el frontend.
#
# Patrón de cada método:
# 1. Abrir conexión a la BD
# 2. Ejecutar consulta SQL
# 3. Retornar resultado
# 4. Manejar errores con HTTPException
# 5. Cerrar conexión en el bloque finally (siempre se ejecuta)
# ============================================================

import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.db_config import get_db_connection
from app.models.subjects_model import SubjectCreate

class SubjectsController:

    # ------------------------------------------------------------
    # GET — Obtener todas las materias
    # LEFT JOIN con programs trae el nombre del programa en la
    # misma consulta, sin necesidad de una segunda query.
    # LEFT JOIN (en lugar de INNER JOIN) asegura que se retornen
    # materias aunque no tengan programa asignado.
    # Ordena alfabéticamente por nombre de materia.
    # ------------------------------------------------------------
    def get_subjects(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT
                    s.id, s.name, s.code, s.credits, s.program_id,
                    s.is_active, s.created_at, s.updated_at,
                    p.name AS program_name
                FROM subjects s
                LEFT JOIN programs p ON s.program_id = p.id
                ORDER BY s.name ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()  # Retorna todas las filas como lista de tuplas

            # Construimos una lista de diccionarios a partir de las tuplas
            # accediendo a cada columna por su índice posicional
            payload = []
            for data in result:
                payload.append({
                    "id": data[0],
                    "name": data[1],
                    "code": data[2],
                    "credits": data[3],
                    "program_id": data[4],
                    "is_active": data[5],
                    "created_at": data[6],
                    "updated_at": data[7],
                    "program_name": data[8]     # Obtenido del JOIN con programs
                })
            return payload
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener materias: {str(e)}")
        finally:
            if conn: conn.close()           # Cierra la conexión aunque ocurra un error

    # ------------------------------------------------------------
    # GET — Obtener una materia por ID
    # Mismo LEFT JOIN para incluir el nombre del programa.
    # Usa %s como placeholder para evitar inyección SQL.
    # La coma en (id,) convierte el valor en tupla, requerido por psycopg2.
    # jsonable_encoder convierte el dict a formato serializable por FastAPI.
    # Si no encuentra el registro, lanza un error 404.
    # ------------------------------------------------------------
    def get_subject(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT
                    s.id, s.name, s.code, s.credits, s.program_id,
                    s.is_active, s.created_at, s.updated_at,
                    p.name AS program_name
                FROM subjects s
                LEFT JOIN programs p ON s.program_id = p.id
                WHERE s.id = %s
            """
            cursor.execute(query, (id,))        # La coma convierte id en tupla, requerido por psycopg2
            data = cursor.fetchone()            # Retorna solo la primera fila o None
            if data:
                content = {
                    "id": data[0],
                    "name": data[1],
                    "code": data[2],
                    "credits": data[3],
                    "program_id": data[4],
                    "is_active": data[5],
                    "created_at": data[6],
                    "updated_at": data[7],
                    "program_name": data[8]     # Obtenido del JOIN con programs
                }
                return jsonable_encoder(content)
            raise HTTPException(status_code=404, detail="Materia no encontrada")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # POST — Crear una nueva materia
    # RETURNING id retorna el ID generado sin segunda consulta.
    # Si el código de materia ya existe o el program_id no es válido,
    # PostgreSQL lanzará un error de restricción (UNIQUE o FK)
    # que capturamos y retornamos como error 400.
    # ------------------------------------------------------------
    def create_subject(self, subject: SubjectCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO subjects (name, code, credits, program_id, is_active)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """, (subject.name, subject.code, subject.credits, subject.program_id, subject.is_active))

            new_id = cursor.fetchone()[0]   # Captura el ID generado por PostgreSQL
            conn.commit()                   # Confirma la transacción en la BD
            return {"mensaje": "Materia registrada exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()        # Deshace cambios si algo falla
            # Error 400 porque es un problema de datos, no del servidor
            # Puede ocurrir si el código ya existe (UNIQUE) o el programa no existe (FK)
            raise HTTPException(status_code=400, detail=f"Error: Verifique si el código ya existe o el programa es válido. {err}")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT — Actualizar una materia existente
    # Permite modificar nombre, código, créditos, programa y estado.
    # updated_at=NOW() registra la fecha de modificación en la BD.
    # Si RETURNING id no retorna nada, el registro no existe → 404.
    # ------------------------------------------------------------
    def update_subject(self, id: int, subject: SubjectCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE subjects
                SET name=%s, code=%s, credits=%s, program_id=%s, is_active=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (subject.name, subject.code, subject.credits, subject.program_id, subject.is_active, id))

            if cursor.fetchone():           # Si retorna algo, el UPDATE fue exitoso
                conn.commit()
                return {"mensaje": "Materia actualizada correctamente"}
            raise HTTPException(status_code=404, detail="Materia no encontrada para actualizar")
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE — Eliminar una materia por ID
    # RETURNING id confirma que el registro existía y fue eliminado.
    # Si la materia tiene horarios asignados en la tabla schedules,
    # PostgreSQL lanzará un error de integridad referencial (FK)
    # que capturamos con psycopg2.Error y retornamos como error 400.
    # Esto protege la integridad de los horarios ya generados.
    # ------------------------------------------------------------
    def delete_subject(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():           # Si retorna algo, el DELETE fue exitoso
                conn.commit()
                return {"mensaje": "Materia eliminada correctamente"}
            raise HTTPException(status_code=404, detail="La materia no existe")
        except psycopg2.Error:
            if conn: conn.rollback()
            # Error 400 indica que la operación no es posible por restricciones de la BD
            # Una materia con horarios asignados no puede eliminarse (integridad referencial)
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar: la materia ya tiene horarios asignados."
            )
        finally:
            if conn: conn.close()