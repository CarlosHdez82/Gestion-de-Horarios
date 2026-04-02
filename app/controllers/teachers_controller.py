import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.teachers_model import Teachers
from fastapi.encoders import jsonable_encoder

class TeachersController:

    def create_teacher(self, teacher: Teachers):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teachers (first_name, last_name, email, phone, hire_date, faculty_id, program_id, level_id, role_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (teacher.first_name, teacher.last_name, teacher.email, teacher.phone, teacher.hire_date,
                  teacher.faculty_id, teacher.program_id, teacher.level_id, teacher.role_id, teacher.is_active))
            conn.commit()
            return {"resultado": "Teacher created"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_teacher(self, teacher_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teachers WHERE teacher_id = %s", (teacher_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'teacher_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'phone': result[4],
                    'hire_date': str(result[5]),
                    'faculty_id': result[6],
                    'program_id': result[7],
                    'level_id': result[8],
                    'role_id': result[9],
                    'is_active': result[10]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_teachers(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teachers")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'teacher_id': data[0],
                    'first_name': data[1],
                    'last_name': data[2],
                    'email': data[3],
                    'phone': data[4],
                    'hire_date': str(data[5]),
                    'faculty_id': data[6],
                    'program_id': data[7],
                    'level_id': data[8],
                    'role_id': data[9],
                    'is_active': data[10]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No teachers found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_teacher(self, teacher_id: int, teacher: Teachers):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teachers
                SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    phone = %s,
                    hire_date = %s,
                    faculty_id = %s,
                    program_id = %s,
                    level_id = %s,
                    role_id = %s,
                    is_active = %s
                WHERE teacher_id = %s
                RETURNING teacher_id, first_name, last_name, email, phone, hire_date, faculty_id, program_id, level_id, role_id, is_active;
            """, (teacher.first_name, teacher.last_name, teacher.email, teacher.phone, teacher.hire_date,
                  teacher.faculty_id, teacher.program_id, teacher.level_id, teacher.role_id, teacher.is_active, teacher_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'teacher_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'phone': result[4],
                    'hire_date': str(result[5]),
                    'faculty_id': result[6],
                    'program_id': result[7],
                    'level_id': result[8],
                    'role_id': result[9],
                    'is_active': result[10]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_teacher(self, teacher_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM teachers
                WHERE teacher_id = %s
                RETURNING teacher_id, first_name, last_name, email, phone, hire_date, faculty_id, program_id, level_id, role_id, is_active;
            """, (teacher_id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'teacher_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'phone': result[4],
                    'hire_date': str(result[5]),
                    'faculty_id': result[6],
                    'program_id': result[7],
                    'level_id': result[8],
                    'role_id': result[9],
                    'is_active': result[10]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Teacher not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()