import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.teacherspecialties_model import TeacherSpecialties
from fastapi.encoders import jsonable_encoder

class TeacherSpecialtiesController:

    def create_relation(self, relation: TeacherSpecialties):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teacher_specialties (teacher_id, specialty_id)
                VALUES (%s, %s)
            """, (relation.teacher_id, relation.specialty_id))
            conn.commit()
            return {"resultado": "Relation created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_relation(self, teacher_id: int, specialty_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM teacher_specialties
                WHERE teacher_id = %s AND specialty_id = %s
            """, (teacher_id, specialty_id))
            result = cursor.fetchone()
            if result:
                content = {
                    'teacher_id': result[0],
                    'specialty_id': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Relation not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_relations(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teacher_specialties")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'teacher_id': data[0],
                    'specialty_id': data[1]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No relations found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_relation(self, teacher_id: int, specialty_id: int, relation: TeacherSpecialties):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teacher_specialties
                SET teacher_id = %s,
                    specialty_id = %s
                WHERE teacher_id = %s AND specialty_id = %s
                RETURNING teacher_id, specialty_id;
            """, (relation.teacher_id, relation.specialty_id, teacher_id, specialty_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'teacher_id': result[0],
                    'specialty_id': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Relation not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_relation(self, teacher_id: int, specialty_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM teacher_specialties
                WHERE teacher_id = %s AND specialty_id = %s
                RETURNING teacher_id, specialty_id;
            """, (teacher_id, specialty_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'teacher_id': result[0],
                    'specialty_id': result[1]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Relation not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()