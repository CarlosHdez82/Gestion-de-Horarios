import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.teacheravailability_model import TeacherAvailability
from fastapi.encoders import jsonable_encoder

class TeacherAvailabilityController:

    def create_availability(self, availability: TeacherAvailability):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teacher_availability (teacher_id, period_id, day_of_week, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s)
            """, (availability.teacher_id, availability.period_id, availability.day_of_week,
                  availability.start_time, availability.end_time))
            conn.commit()
            return {"resultado": "Availability created"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_availability(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teacher_availability WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'id': int(result[0]),
                    'teacher_id': result[1],
                    'period_id': result[2],
                    'day_of_week': result[3],
                    'start_time': str(result[4]),
                    'end_time': str(result[5])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Availability not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_availabilities(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teacher_availability")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'teacher_id': data[1],
                    'period_id': data[2],
                    'day_of_week': data[3],
                    'start_time': str(data[4]),
                    'end_time': str(data[5])
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No availabilities found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_availability(self, id: int, availability: TeacherAvailability):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teacher_availability
                SET teacher_id = %s,
                    period_id = %s,
                    day_of_week = %s,
                    start_time = %s,
                    end_time = %s
                WHERE id = %s
                RETURNING id, teacher_id, period_id, day_of_week, start_time, end_time;
            """, (availability.teacher_id, availability.period_id, availability.day_of_week,
                  availability.start_time, availability.end_time, id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'teacher_id': result[1],
                    'period_id': result[2],
                    'day_of_week': result[3],
                    'start_time': str(result[4]),
                    'end_time': str(result[5])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Availability not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_availability(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM teacher_availability
                WHERE id = %s
                RETURNING id, teacher_id, period_id, day_of_week, start_time, end_time;
            """, (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'teacher_id': result[1],
                    'period_id': result[2],
                    'day_of_week': result[3],
                    'start_time': str(result[4]),
                    'end_time': str(result[5])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Availability not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()