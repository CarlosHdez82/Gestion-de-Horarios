import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.teacherlevels_model import TeacherLevels
from fastapi.encoders import jsonable_encoder

class TeacherLevelsController:

    def create_teacherlevel(self, teacherlevel: TeacherLevels):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teacher_levels (name)
                VALUES (%s)
            """, (teacherlevel.name,))
            conn.commit()
            return {"resultado": "Teacher level created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_teacherlevel(self, teacherlevel_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teacher_levels WHERE teacherlevel_id = %s", (teacherlevel_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'teacherlevel_id': int(result[0]),
                    'name': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher level not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_teacherlevels(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teacher_levels")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'teacherlevel_id': data[0],
                    'name': data[1]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No teacher levels found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_teacherlevel(self, teacherlevel_id: int, teacherlevel: TeacherLevels):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teacher_levels
                SET name = %s
                WHERE teacherlevel_id = %s
                RETURNING teacherlevel_id, name;
            """, (teacherlevel.name, teacherlevel_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'teacherlevel_id': int(result[0]),
                    'name': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher level not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_teacherlevel(self, teacherlevel_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM teacher_levels
                WHERE teacherlevel_id = %s
                RETURNING teacherlevel_id, name;
            """, (teacherlevel_id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'teacherlevel_id': int(result[0]),
                    'name': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher level not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()