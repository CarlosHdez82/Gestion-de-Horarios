import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.academicperiods_model import AcademicPeriods
from fastapi.encoders import jsonable_encoder

class AcademicPeriodsController:

    def create_period(self, period: AcademicPeriods):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO academic_periods (name, start_date, end_date, is_active)
                VALUES (%s, %s, %s, %s)
            """, (period.name, period.start_date, period.end_date, period.is_active))
            conn.commit()
            return {"resultado": "Academic period created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_period(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM academic_periods WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'start_date': str(result[2]),
                    'end_date': str(result[3]),
                    'is_active': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Academic period not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_periods(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM academic_periods")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'name': data[1],
                    'start_date': str(data[2]),
                    'end_date': str(data[3]),
                    'is_active': data[4]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No academic periods found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_period(self, id: int, period: AcademicPeriods):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE academic_periods
                SET name = %s,
                    start_date = %s,
                    end_date = %s,
                    is_active = %s
                WHERE id = %s
                RETURNING id, name, start_date, end_date, is_active;
            """, (period.name, period.start_date, period.end_date, period.is_active, id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'start_date': str(result[2]),
                    'end_date': str(result[3]),
                    'is_active': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Academic period not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_period(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM academic_periods
                WHERE id = %s
                RETURNING id, name, start_date, end_date, is_active;
            """, (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'start_date': str(result[2]),
                    'end_date': str(result[3]),
                    'is_active': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Academic period not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()