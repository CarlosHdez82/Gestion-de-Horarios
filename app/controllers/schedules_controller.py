import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder

class SchedulesController:

    def create_schedule(self, schedule):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO schedules (teacher_id, subject_id, period_id, day_of_week, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """, (schedule.teacher_id, schedule.subject_id, schedule.period_id, 
                  schedule.day_of_week, schedule.start_time, schedule.end_time))
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Horario creado exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            if conn: conn.close()

    def get_schedules(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Consulta con JOINs para traer nombres reales en lugar de solo IDs
            query = """
                SELECT 
                    s.id, s.teacher_id, s.subject_id, s.period_id, s.day_of_week, 
                    s.start_time, s.end_time, s.created_at, s.is_active, s.updated_at,
                    (t.first_name || ' ' || t.last_name) AS teacher_name,
                    sub.name AS subject_name,
                    ap.name AS period_name
                FROM schedules s
                LEFT JOIN teachers t ON s.teacher_id = t.id
                LEFT JOIN subjects sub ON s.subject_id = sub.id
                LEFT JOIN academic_periods ap ON s.period_id = ap.id
                ORDER BY s.day_of_week, s.start_time ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'teacher_id': data[1],
                    'subject_id': data[2],
                    'period_id': data[3],
                    'day_of_week': data[4],
                    'start_time': str(data[5]),
                    'end_time': str(data[6]),
                    'created_at': str(data[7]),
                    'is_active': data[8],
                    'teacher_name': data[10],
                    'subject_name': data[11],
                    'period_name': data[12]
                })
            return payload
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail="Error al obtener horarios")
        finally:
            if conn: conn.close()

    def update_schedule(self, id: int, schedule):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE schedules SET 
                    teacher_id=%s, subject_id=%s, period_id=%s, 
                    day_of_week=%s, start_time=%s, end_time=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (schedule.teacher_id, schedule.subject_id, schedule.period_id, 
                  schedule.day_of_week, schedule.start_time, schedule.end_time, id))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Horario actualizado"}
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        finally:
            if conn: conn.close()

    def delete_schedule(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM schedules WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Horario eliminado"}
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        finally:
            if conn: conn.close()