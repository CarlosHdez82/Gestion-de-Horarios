import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection

class AvailabilityController:
    def get_availabilities(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT a.*, 
                       CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
                       p.name AS period_name
                FROM teacher_availability a
                LEFT JOIN teachers t ON a.teacher_id = t.id
                LEFT JOIN academic_periods p ON a.period_id = p.id
                ORDER BY a.day_of_week, a.start_time ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            payload = []
            for d in result:
                payload.append({
                    "id": d[0], "teacher_id": d[1], "period_id": d[2],
                    "day_of_week": d[3], "start_time": str(d[4]), "end_time": str(d[5]),
                    "is_active": d[6], "created_at": str(d[7]), "updated_at": str(d[8]),
                    "teacher_name": d[9], "period_name": d[10]
                })
            return payload
        finally:
            if conn: conn.close()

    def get_availability(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM teacher_availability WHERE id = %s"
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return {
                    "id": data[0], "teacher_id": data[1], "period_id": data[2],
                    "day_of_week": data[3], "start_time": str(data[4]), "end_time": str(data[5]),
                    "is_active": data[6]
                }
            raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
        finally:
            if conn: conn.close()

    def create_availability(self, data):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teacher_availability (teacher_id, period_id, day_of_week, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (data.teacher_id, data.period_id, data.day_of_week, data.start_time, data.end_time))
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Registrado con éxito", "id": new_id}
        finally:
            if conn: conn.close()

    def update_availability(self, id: int, data):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teacher_availability 
                SET teacher_id=%s, period_id=%s, day_of_week=%s, start_time=%s, end_time=%s, updated_at=NOW()
                WHERE id=%s RETURNING id
            """, (data.teacher_id, data.period_id, data.day_of_week, data.start_time, data.end_time, id))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Disponibilidad actualizada"}
            raise HTTPException(status_code=404, detail="No encontrado")
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
                return {"mensaje": "Eliminado"}
            raise HTTPException(status_code=404, detail="No encontrado")
        finally:
            if conn: conn.close()