import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.teacherdegrees_model import TeacherDegrees
from fastapi.encoders import jsonable_encoder

class TeacherDegreesController:

    def create_teacherdegree(self, teacherdegree: TeacherDegrees):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teacher_degrees (teacher_id, degree_type, title, institution)
                VALUES (%s, %s, %s, %s)
            """, (teacherdegree.teacher_id, teacherdegree.degree_type, teacherdegree.title, teacherdegree.institution))
            conn.commit()
            return {"resultado": "Teacher degree created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_teacherdegree(self, teacherdegree_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teacher_degrees WHERE id = %s", (teacherdegree_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'teacherdegree_id': int(result[0]),
                    'teacher_id': result[1],
                    'degree_type': result[2],
                    'title': result[3],
                    'institution': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher degree not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_teacherdegrees(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teacher_degrees")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'teacherdegree_id': data[0],
                    'teacher_id': data[1],
                    'degree_type': data[2],
                    'title': data[3],
                    'institution': data[4]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No teacher degrees found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_teacherdegree(self, teacherdegree_id: int, teacherdegree: TeacherDegrees):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teacher_degrees
                SET teacher_id = %s,
                    degree_type = %s,
                    title = %s,
                    institution = %s
                WHERE id = %s
                RETURNING id, teacher_id, degree_type, title, institution;
            """, (teacherdegree.teacher_id, teacherdegree.degree_type, teacherdegree.title, teacherdegree.institution, teacherdegree_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'teacherdegree_id': int(result[0]),
                    'teacher_id': result[1],
                    'degree_type': result[2],
                    'title': result[3],
                    'institution': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher degree not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_teacherdegree(self, teacherdegree_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM teacher_degrees
                WHERE id = %s
                RETURNING id, teacher_id, degree_type, title, institution;
            """, (teacherdegree_id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'teacherdegree_id': int(result[0]),
                    'teacher_id': result[1],
                    'degree_type': result[2],
                    'title': result[3],
                    'institution': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher degree not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()