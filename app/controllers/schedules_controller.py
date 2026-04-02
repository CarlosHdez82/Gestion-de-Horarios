import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.schedules_model import Schedules
from fastapi.encoders import jsonable_encoder

class SchedulesController:

    def create_schedule(self, schedule: Schedules):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO schedules (teacher_id, subject_id, period_id, day_of_week, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (schedule.teacher_id, schedule.subject_id, schedule.period_id, schedule.day_of_week, schedule.start_time, schedule.end_time))
            conn.commit()
            return {"resultado": "Schedule created"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_schedule(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM schedules WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'id': int(result[0]),
                    'teacher_id': result[1],
                    'subject_id': result[2],
                    'period_id': result[3],
                    'day_of_week': result[4],
                    'start_time': str(result[5]),
                    'end_time': str(result[6]),
                    'created_at': str(result[7])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Schedule not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_schedules(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM schedules")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'teacher_id': data[1],
                    'subject_id': data[2],
                    'period_id': data[3],
                    'day_of_week': data[4],
                    'start_time': str(data[5]),
                    'end_time': str(data[6]),
                    'created_at': str(data[7])
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No schedules found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_schedule(self, id: int, schedule: Schedules):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE schedules
                SET teacher_id = %s,
                    subject_id = %s,
                    period_id = %s,
                    day_of_week = %s,
                    start_time = %s,
                    end_time = %s
                WHERE id = %s
                RETURNING id, teacher_id, subject_id, period_id, day_of_week, start_time, end_time, created_at;
            """, (schedule.teacher_id, schedule.subject_id, schedule.period_id, schedule.day_of_week, schedule.start_time, schedule.end_time, id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'teacher_id': result[1],
                    'subject_id': result[2],
                    'period_id': result[3],
                    'day_of_week': result[4],
                    'start_time': str(result[5]),
                    'end_time': str(result[6]),
                    'created_at': str(result[7])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Schedule not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_schedule(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM schedules
                WHERE id = %s
                RETURNING id, teacher_id, subject_id, period_id, day_of_week, start_time, end_time, created_at;
            """, (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'teacher_id': result[1],
                    'subject_id': result[2],
                    'period_id': result[3],
                    'day_of_week': result[4],
                    'start_time': str(result[5]),
                    'end_time': str(result[6]),
                    'created_at': str(result[7])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Schedule not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()