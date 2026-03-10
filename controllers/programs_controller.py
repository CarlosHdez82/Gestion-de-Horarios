import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.programs_model import Programs
from fastapi.encoders import jsonable_encoder

class ProgramsController:

    def create_program(self, program: Programs):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO programs (name, faculty_id)
                VALUES (%s, %s)
            """, (program.name, program.faculty_id))
            conn.commit()
            return {"resultado": "Program created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_program(self, program_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programs WHERE program_id = %s", (program_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'program_id': int(result[0]),
                    'name': result[1],
                    'faculty_id': int(result[2])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Program not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_programs(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programs")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'program_id': data[0],
                    'name': data[1],
                    'faculty_id': data[2]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No programs found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_program(self, program_id: int, program: Programs):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE programs
                SET name = %s,
                    faculty_id = %s
                WHERE program_id = %s
                RETURNING program_id, name, faculty_id;
            """, (program.name, program.faculty_id, program_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'program_id': int(result[0]),
                    'name': result[1],
                    'faculty_id': int(result[2])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Program not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_program(self, program_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM programs
                WHERE program_id = %s
                RETURNING program_id, name, faculty_id;
            """, (program_id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'program_id': int(result[0]),
                    'name': result[1],
                    'faculty_id': int(result[2])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Program not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()