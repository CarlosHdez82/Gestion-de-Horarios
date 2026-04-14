import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.teachers_model import TeacherCreate

class TeachersController:

    def get_teachers(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Consulta con JOINs para traer los nombres de las tablas relacionadas
            query = """
                SELECT 
                    t.*, 
                    f.name AS faculty_name, 
                    p.name AS program_name, 
                    tl.name AS level_name
                FROM teachers t
                LEFT JOIN faculties f ON t.faculty_id = f.id
                LEFT JOIN programs p ON t.program_id = p.id
                LEFT JOIN teacher_levels tl ON t.level_id = tl.id
                ORDER BY t.last_name ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                payload.append({
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
                    'is_active': data[10],
                    'created_at': str(data[11]),
                    'updated_at': str(data[12]),
                    'faculty_name': data[13], 
                    'program_name': data[14],
                    'level_name': data[15]   
                })
            
            return payload
        except psycopg2.Error as err:
            # Mantenemos solo el print de error para diagnóstico en caso de fallo
            print(f"❌ ERROR CRÍTICO EN BD: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener la lista de docentes")
        finally:
            if conn: conn.close()

    def create_teacher(self, teacher: TeacherCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teachers (first_name, last_name, email, phone, hire_date, faculty_id, program_id, level_id, role_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (teacher.first_name, teacher.last_name, teacher.email, teacher.phone, teacher.hire_date,
                  teacher.faculty_id, teacher.program_id, teacher.level_id, teacher.role_id, teacher.is_active))
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Docente registrado exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear: {err}")
        finally:
            if conn: conn.close()

    def update_teacher(self, teacher_id: int, teacher: TeacherCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teachers SET 
                    first_name=%s, last_name=%s, email=%s, phone=%s, 
                    hire_date=%s, faculty_id=%s, program_id=%s, 
                    level_id=%s, role_id=%s, is_active=%s, updated_at=NOW() 
                WHERE id=%s RETURNING id;
            """, (teacher.first_name, teacher.last_name, teacher.email, teacher.phone, teacher.hire_date,
                  teacher.faculty_id, teacher.program_id, teacher.level_id, teacher.role_id, teacher.is_active, teacher_id))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Docente actualizado correctamente"}
            raise HTTPException(status_code=404, detail="Docente no encontrado")
        finally:
            if conn: conn.close()

    def delete_teacher(self, teacher_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Retornamos ID para confirmar que existía
            cursor.execute("DELETE FROM teachers WHERE id = %s RETURNING id", (teacher_id,))
            result = cursor.fetchone()
            if result:
                conn.commit()
                return {"mensaje": "Docente eliminado físicamente"}
            raise HTTPException(status_code=404, detail="El docente no existe")
        except psycopg2.Error as err:
            if conn: conn.rollback()
            # Error común: Integridad referencial (FK)
            raise HTTPException(status_code=400, detail="No se puede eliminar porque el docente tiene registros asociados")
        finally:
            if conn: conn.close()