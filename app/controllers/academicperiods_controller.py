# ============================================================
# academicperiods_controller.py — Controlador de Periodos Académicos
# ============================================================
# Contiene la lógica de negocio para gestionar los periodos
# académicos. Cada método se conecta a la BD, ejecuta una
# consulta SQL y retorna el resultado o lanza un error HTTP.
#
# Patrón de cada método:
# 1. Abrir conexión a la BD
# 2. Ejecutar consulta SQL
# 3. Retornar resultado
# 4. Manejar errores con HTTPException
# 5. Cerrar conexión en el bloque finally (siempre se ejecuta)
# ============================================================

from fastapi.encoders import jsonable_encoder
import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.academicperiods_model import AcademicPeriodCreate

class PeriodsController:

    # ------------------------------------------------------------
    # GET — Obtener todos los periodos académicos
    # Ejecuta un SELECT ordenado por ID descendente (más reciente primero).
    # Convierte cada fila de la BD en un diccionario para retornarlo como JSON.
    # start_date y end_date se convierten a string porque psycopg2
    # las retorna como objetos date de Python, no como strings.
    # ------------------------------------------------------------
    def get_periods(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, start_date, end_date, is_active, created_at, updated_at
                FROM academic_periods ORDER BY id DESC
            """)
            result = cursor.fetchall()  # Retorna todas las filas como lista de tuplas

            # Construimos una lista de diccionarios a partir de las tuplas
            # accediendo a cada columna por su índice posicional
            payload = []
            for d in result:
                payload.append({
                    "id": d[0],
                    "name": d[1],
                    "start_date": str(d[2]) if d[2] else None,  # Convertir date a string o None
                    "end_date": str(d[3]) if d[3] else None,    # Convertir date a string o None
                    "is_active": d[4],
                    "created_at": d[5],
                    "updated_at": d[6]
                })
            return payload
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener periodos: {str(e)}")
        finally:
            if conn: conn.close()  # Cierra la conexión aunque ocurra un error

    # ------------------------------------------------------------
    # GET — Obtener un periodo académico por ID
    # Usa %s como placeholder para evitar inyección SQL.
    # Si no encuentra el registro, lanza un error 404.
    # jsonable_encoder convierte el dict a un formato serializable por FastAPI.
    # ------------------------------------------------------------
    def get_period(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, start_date, end_date, is_active, created_at, updated_at
                FROM academic_periods WHERE id = %s
            """, (id,))             # La coma convierte id en tupla, requerido por psycopg2
            data = cursor.fetchone()  # Retorna solo la primera fila o None
            if data:
                content = {
                    "id": data[0],
                    "name": data[1],
                    "start_date": str(data[2]) if data[2] else None,
                    "end_date": str(data[3]) if data[3] else None,
                    "is_active": data[4],
                    "created_at": data[5],
                    "updated_at": data[6]
                }
                return jsonable_encoder(content)
            raise HTTPException(status_code=404, detail="Periodo académico no encontrado")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # POST — Crear un nuevo periodo académico
    # RETURNING id hace que PostgreSQL retorne el ID del registro
    # recién insertado sin necesidad de hacer una segunda consulta.
    # conn.commit() confirma la transacción; sin esto los cambios
    # no se guardan permanentemente en la BD.
    # conn.rollback() deshace los cambios si ocurre un error.
    # ------------------------------------------------------------
    def create_period(self, data: AcademicPeriodCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO academic_periods (name, start_date, end_date, is_active)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (data.name, data.start_date, data.end_date, data.is_active))
            new_id = cursor.fetchone()[0]   # Captura el ID generado por PostgreSQL
            conn.commit()                   # Confirma la transacción en la BD
            return {"mensaje": "Periodo académico creado", "id": new_id}
        except Exception as e:
            if conn: conn.rollback()        # Deshace cambios si algo falla
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT — Actualizar un periodo académico existente
    # updated_at=NOW() registra automáticamente la fecha y hora
    # de la última modificación usando la función de PostgreSQL.
    # Si RETURNING id no retorna nada, el registro no existe → 404.
    # ------------------------------------------------------------
    def update_period(self, id: int, data: AcademicPeriodCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE academic_periods
                SET name=%s, start_date=%s, end_date=%s, is_active=%s, updated_at=NOW()
                WHERE id=%s RETURNING id
            """, (data.name, data.start_date, data.end_date, data.is_active, id))
            if cursor.fetchone():           # Si retorna algo, el UPDATE fue exitoso
                conn.commit()
                return {"mensaje": "Periodo actualizado correctamente"}
            raise HTTPException(status_code=404, detail="Periodo no encontrado para actualizar")
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE — Eliminar un periodo académico por ID
    # RETURNING id confirma que el registro existía y fue eliminado.
    # Si hay horarios o disponibilidades asociadas al periodo,
    # PostgreSQL lanzará un error de integridad referencial (FK),
    # que capturamos con psycopg2.Error y retornamos como error 400.
    # ------------------------------------------------------------
    def delete_period(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM academic_periods WHERE id = %s RETURNING id", (id,))
            deleted_id = cursor.fetchone()
            if deleted_id:
                conn.commit()
                return {"mensaje": "Periodo eliminado correctamente", "id": deleted_id[0]}
            raise HTTPException(status_code=404, detail="El periodo no existe")
        except psycopg2.Error:
            if conn: conn.rollback()
            # Error 400 indica que la operación no es posible por restricciones de la BD
            raise HTTPException(status_code=400, detail="No se puede eliminar: existen horarios o disponibilidades asociadas a este periodo")
        finally:
            if conn: conn.close()