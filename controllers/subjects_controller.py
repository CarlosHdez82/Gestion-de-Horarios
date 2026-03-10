import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.subjects_model import Subjects
from fastapi.encoders import jsonable_encoder

class SubjectsController:

    def create_subject(self, subject: Subjects):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO subjects (name, code, credits, program_id, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """, (subject.name, subject.code, subject.credits, subject.program_id, subject.is_active))
            conn.commit()
            return {"resultado": "Subject created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_subject(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'code': result[2],
                    'credits': int(result[3]),
                    'program_id': int(result[4]),
                    'is_active': result[5]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Subject not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_subjects(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'name': data[1],
                    'code': data[2],
                    'credits': data[3],
                    'program_id': data[4],
                    'is_active': data[5]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No subjects found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_subject(self, id: int, subject: Subjects):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE subjects
                SET name = %s,
                    code = %s,
                    credits = %s,
                    program_id = %s,
                    is_active = %s
                WHERE id = %s
                RETURNING id, name, code, credits, program_id, is_active;
            """, (subject.name, subject.code, subject.credits, subject.program_id, subject.is_active, id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'code': result[2],
                    'credits': int(result[3]),
                    'program_id': int(result[4]),
                    'is_active': result[5]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Subject not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_subject(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM subjects
                WHERE id = %s
                RETURNING id, name, code, credits, program_id, is_active;
            """, (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'id': int(result[0]),
                    'name': result[1],
                    'code': result[2],
                    'credits': int(result[3]),
                    'program_id': int(result[4]),
                    'is_active': result[5]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Subject not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()