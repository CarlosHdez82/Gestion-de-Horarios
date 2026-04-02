import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.faculties_model import Faculties
from fastapi.encoders import jsonable_encoder

class FacultiesController:

    def create_faculty(self, faculty: Faculties):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO faculties (name, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
            """, (faculty.name, faculty.is_active, faculty.created_at, faculty.updated_at))
            conn.commit()
            return {"resultado": "Faculty created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_faculty(self, faculties_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM faculties WHERE faculties_id = %s", (faculties_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'faculties_id': int(result[0]),
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': str(result[3]),
                    'updated_at': str(result[4])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Faculty not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_faculties(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM faculties")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'faculties_id': data[0],
                    'name': data[1],
                    'is_active': data[2],
                    'created_at': str(data[3]),
                    'updated_at': str(data[4])
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No faculties found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_faculty(self, faculties_id: int, faculty: Faculties):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE faculties
                SET name = %s, is_active = %s, created_at = %s, updated_at = %s
                WHERE faculties_id = %s
                RETURNING faculties_id, name, is_active, created_at, updated_at;
            """, (faculty.name, faculty.is_active, faculty.created_at, faculty.updated_at, faculties_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'faculties_id': int(result[0]),
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': str(result[3]),
                    'updated_at': str(result[4])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Faculty not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_faculty(self, faculties_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM faculties
                WHERE faculties_id = %s
                RETURNING faculties_id, name, is_active, created_at, updated_at;
            """, (faculties_id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'faculties_id': int(result[0]),
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': str(result[3]),
                    'updated_at': str(result[4])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Faculty not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()