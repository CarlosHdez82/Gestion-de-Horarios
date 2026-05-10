import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.schedules_model import ScheduleCreate
from fastapi.encoders import jsonable_encoder

class SchedulesController:

    def create_schedule(self, schedule: ScheduleCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Usamos block_label y group_code según el nuevo esquema
            cursor.execute("""
                INSERT INTO schedules (teacher_id, subject_id, period_id, day_of_week, block_label, group_code)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """, (schedule.teacher_id, schedule.subject_id, schedule.period_id, 
                  schedule.day_of_week, schedule.block_label, schedule.group_code))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Carga académica asignada exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al asignar horario: {err}")
        finally:
            if conn: conn.close()

    def get_schedules(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # JOIN actualizado: t ahora es la tabla 'users'
            query = """
                SELECT 
                    s.id, s.teacher_id, s.subject_id, s.period_id, s.day_of_week, 
                    s.block_label, s.group_code, s.created_at,
                    (u.first_name || ' ' || u.last_name) AS teacher_name,
                    sub.name AS subject_name,
                    sub.code AS subject_code,
                    ap.name AS period_name
                FROM schedules s
                LEFT JOIN users u ON s.teacher_id = u.id
                LEFT JOIN subjects sub ON s.subject_id = sub.id
                LEFT JOIN academic_periods ap ON s.period_id = ap.id
                ORDER BY ap.name DESC, s.day_of_week, s.block_label ASC
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
                    'block_label': data[5],
                    'group_code': data[6],
                    'created_at': data[7],
                    'teacher_name': data[8],
                    'subject_name': data[9],
                    'subject_code': data[10],
                    'period_name': data[11]
                })
            return payload
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail="Error al obtener la carga académica")
        finally:
            if conn: conn.close()

    def update_schedule(self, id: int, schedule: ScheduleCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE schedules SET 
                    teacher_id=%s, subject_id=%s, period_id=%s, 
                    day_of_week=%s, block_label=%s, group_code=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (schedule.teacher_id, schedule.subject_id, schedule.period_id, 
                  schedule.day_of_week, schedule.block_label, schedule.group_code, id))
            
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Horario actualizado correctamente"}
            raise HTTPException(status_code=404, detail="Registro de horario no encontrado")
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar el horario")
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
                return {"mensaje": "Carga académica eliminada"}
            raise HTTPException(status_code=404, detail="El registro no existe")
        finally:
            if conn: conn.close()