from fastapi.encoders import jsonable_encoder
import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.academicperiods_model import AcademicPeriodCreate

class PeriodsController:

    def get_periods(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, start_date, end_date, is_active, created_at, updated_at
                FROM academic_periods ORDER BY id DESC
            """)
            result = cursor.fetchall()
            payload = []
            for d in result:
                payload.append({
                    "id": d[0],
                    "name": d[1],
                    "start_date": str(d[2]) if d[2] else None,
                    "end_date": str(d[3]) if d[3] else None,
                    "is_active": d[4],
                    "created_at": d[5],
                    "updated_at": d[6]
                })
            return payload
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener periodos: {str(e)}")
        finally:
            if conn: conn.close()

    def get_period(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, start_date, end_date, is_active, created_at, updated_at
                FROM academic_periods WHERE id = %s
            """, (id,))
            data = cursor.fetchone()
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

    def create_period(self, data: AcademicPeriodCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO academic_periods (name, start_date, end_date, is_active)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (data.name, data.start_date, data.end_date, data.is_active))
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Periodo académico creado", "id": new_id}
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

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
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Periodo actualizado correctamente"}
            raise HTTPException(status_code=404, detail="Periodo no encontrado para actualizar")
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()

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
            raise HTTPException(status_code=400, detail="No se puede eliminar: existen horarios o disponibilidades asociadas a este periodo")
        finally:
            if conn: conn.close()
