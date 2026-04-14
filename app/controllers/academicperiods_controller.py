from fastapi.encoders import jsonable_encoder
import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection

class PeriodsController:
    # ... (get_periods, create y update ya los tienes)

    def get_period(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Seleccionamos por ID
            cursor.execute("SELECT * FROM academic_periods WHERE id = %s", (id,))
            data = cursor.fetchone()
            if data:
                content = {
                    "id": data[0], 
                    "name": data[1], 
                    "start_date": str(data[2]), 
                    "end_date": str(data[3]),
                    "is_active": data[4],
                    "created_at": str(data[5]),
                    "updated_at": str(data[6])
                }
                return jsonable_encoder(content)
            raise HTTPException(status_code=404, detail="Periodo académico no encontrado")
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
        finally:
            if conn: conn.close()

    def delete_period(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Verificamos si existe antes de borrar
            cursor.execute("DELETE FROM academic_periods WHERE id = %s RETURNING id", (id,))
            deleted_id = cursor.fetchone()
            if deleted_id:
                conn.commit()
                return {"mensaje": "Periodo eliminado correctamente", "id": deleted_id[0]}
            raise HTTPException(status_code=404, detail="El periodo no existe")
        except psycopg2.Error as e:
            if conn: conn.rollback()
            # Si hay llaves foráneas (ej: clases asignadas a este periodo), fallará aquí
            raise HTTPException(status_code=400, detail="No se puede eliminar: el periodo tiene registros asociados")
        finally:
            if conn: conn.close()
            
    def get_periods(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM academic_periods ORDER BY start_date DESC")
            result = cursor.fetchall()
            payload = []
            for d in result:
                payload.append({
                    "id": d[0], "name": d[1], 
                    "start_date": str(d[2]), "end_date": str(d[3]),
                    "is_active": d[4], "created_at": str(d[5]), "updated_at": str(d[6])
                })
            return payload
        finally:
            if conn: conn.close()

    def create_period(self, data: AcademicPeriods):
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

    def update_period(self, id: int, data: AcademicPeriods):
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
                return {"mensaje": "Periodo actualizado"}
            raise HTTPException(status_code=404, detail="No encontrado")
        finally:
            if conn: conn.close()