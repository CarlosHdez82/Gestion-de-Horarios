import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.classrooms_model import Classrooms
from fastapi.encoders import jsonable_encoder

class ClassroomsController:

    def create_classroom(self, classroom: Classrooms):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO classrooms (name, capacity, location, type_id, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """, (classroom.name, classroom.capacity, classroom.location, classroom.type_id, classroom.is_active))
            conn.commit()
            return {"resultado": "Classroom created"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_classroom(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classrooms WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'capacity': int(result[2]),
                    'location': result[3],
                    'type_id': result[4],
                    'is_active': result[5]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Classroom not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_classrooms(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classrooms")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'name': data[1],
                    'capacity': data[2],
                    'location': data[3],
                    'type_id': data[4],
                    'is_active': data[5]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No classrooms found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_classroom(self, id: int, classroom: Classrooms):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE classrooms
                SET name = %s,
                    capacity = %s,
                    location = %s,
                    type_id = %s,
                    is_active = %s
                WHERE id = %s
                RETURNING id, name, capacity, location, type_id, is_active;
            """, (classroom.name, classroom.capacity, classroom.location, classroom.type_id, classroom.is_active, id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'capacity': int(result[2]),
                    'location': result[3],
                    'type_id': result[4],
                    'is_active': result[5]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Classroom not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_classroom(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM classrooms
                WHERE id = %s
                RETURNING id, name, capacity, location, type_id, is_active;
            """, (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'capacity': int(result[2]),
                    'location': result[3],
                    'type_id': result[4],
                    'is_active': result[5]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Classroom not found")
        except psycopg2.Error:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()