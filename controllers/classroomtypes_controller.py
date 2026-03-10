import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.classroomtypes_model import ClassroomTypes
from fastapi.encoders import jsonable_encoder

class ClassroomTypesController:

    def create_type(self, ctype: ClassroomTypes):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO classroom_types (name) VALUES (%s)", (ctype.name,))
            conn.commit()
            return {"resultado": "Classroom type created"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_type(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classroom_types WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                return jsonable_encoder({"id": result[0], "name": result[1]})
            else:
                raise HTTPException(status_code=404, detail="Type not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_types(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classroom_types")
            result = cursor.fetchall()
            payload = [{"id": r[0], "name": r[1]} for r in result]
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No types found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_type(self, id: int, ctype: ClassroomTypes):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE classroom_types SET name = %s WHERE id = %s RETURNING id, name
            """, (ctype.name, id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                return jsonable_encoder({"id": result[0], "name": result[1]})
            else:
                raise HTTPException(status_code=404, detail="Type not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_type(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM classroom_types WHERE id = %s RETURNING id, name", (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                return jsonable_encoder({"id": result[0], "name": result[1]})
            else:
                raise HTTPException(status_code=404, detail="Type not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()