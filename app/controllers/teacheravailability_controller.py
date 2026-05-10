import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
# Ajustamos la importación al nombre real de tu modelo
from app.models.teacheravailability_model import TeacherAvailabilityCreate
from fastapi.encoders import jsonable_encoder

class AvailabilityController:

    def get_availabilities(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Optimizamos el JOIN para traer nombres de docentes y periodos
            query = """
                SELECT a.id, a.teacher_id, a.period_id, a.day_of_week, a.block_label, 
                       a.is_active, a.created_at, a.updated_at,
                       (u.first_name || ' ' || u.last_name) AS teacher_name,
                       p.name AS period_name
                FROM teacher_availability a
                LEFT JOIN users u ON a.teacher_id = u.id
                LEFT JOIN academic_periods p ON a.period_id = p.id
                ORDER BY a.day_of_week, a.block_label ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            payload = []
            for d in result:
                payload.append({
                    "id": d[0], "teacher_id": d[1], "period_id": d[2],
                    "day_of_week": d[3], "block_label": d[4],
                    "is_active": d[5], "created_at": d[6], "updated_at": d[7],
                    "teacher_name": d[8], "period_name": d[9]
                })
            return payload
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener disponibilidades: {str(e)}")
        finally:
            if conn: conn.close()

    def get_availability_by_teacher(self, teacher_id: int, period_id: int):
        """Especial para Svelte: Carga los bloques ocupados para pintar el grid"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, day_of_week, block_label 
                FROM teacher_availability 
                WHERE teacher_id = %s AND period_id = %s AND is_active = True
            """, (teacher_id, period_id))
            result = cursor.fetchall()
            # Devolvemos el ID también por si necesitas eliminar un bloque específico desde el Grid
            return [{"id": d[0], "day": d[1], "block": d[2]} for d in result]
        finally:
            if conn: conn.close()

    def create_availability(self, data: TeacherAvailabilityCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teacher_availability (teacher_id, period_id, day_of_week, block_label)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (data.teacher_id, data.period_id, data.day_of_week, data.block_label))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Bloque de disponibilidad guardado", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            # Error 409 es más preciso para conflictos de duplicados
            raise HTTPException(status_code=409, detail="Este bloque ya está registrado para el docente.")
        finally:
            if conn: conn.close()

    def delete_availability(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM teacher_availability WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Disponibilidad eliminada correctamente"}
            raise HTTPException(status_code=404, detail="No se encontró el registro")
        finally:
            if conn: conn.close()

    def clear_teacher_availability(self, teacher_id: int, period_id: int):
        """Limpia todo el grid del docente para re-programar"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM teacher_availability 
                WHERE teacher_id = %s AND period_id = %s
            """, (teacher_id, period_id))
            conn.commit()
            return {"mensaje": "Grid reiniciado correctamente"}
        finally:
            if conn: conn.close()