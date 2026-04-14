import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection

class ProgramsController:

    def get_program(self, program_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT p.*, f.name AS faculty_name 
                FROM programs p
                LEFT JOIN faculties f ON p.faculty_id = f.id
                WHERE p.program_id = %s
            """
            cursor.execute(query, (program_id,))
            result = cursor.fetchone()
            
            if result:
                content = {
                    'program_id': result[0],
                    'name': result[1],
                    'faculty_id': result[2],
                    'is_active': result[3],
                    'created_at': str(result[4]),
                    'updated_at': str(result[5]),
                    'faculty_name': result[6]
                }
                return content
            else:
                raise HTTPException(status_code=404, detail="Programa no encontrado")
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error de base de datos")
        finally:
            if conn: conn.close()
    
    def get_programs(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # SQL con JOIN para no mostrar solo IDs numéricos
            query = """
                SELECT p.*, f.name AS faculty_name 
                FROM programs p
                LEFT JOIN faculties f ON p.faculty_id = f.id
                ORDER BY p.name ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                payload.append({
                    'program_id': data[0],
                    'name': data[1],
                    'faculty_id': data[2],
                    'is_active': data[3],
                    'created_at': str(data[4]),
                    'updated_at': str(data[5]),
                    'faculty_name': data[6] # El nombre de la facultad del JOIN
                })
            return payload
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail="Error al obtener programas")
        finally:
            if conn: conn.close()

    def create_program(self, program):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO programs (name, faculty_id, is_active)
                VALUES (%s, %s, %s) RETURNING id;
            """, (program.name, program.faculty_id, program.is_active))
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Programa creado con éxito", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def update_program(self, program_id: int, program):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE programs SET name=%s, faculty_id=%s, is_active=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (program.name, program.faculty_id, program.is_active, program_id))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Programa actualizado"}
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        finally:
            if conn: conn.close()

    def delete_program(self, program_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM programs WHERE id = %s RETURNING id", (program_id,))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Programa eliminado"}
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        finally:
            if conn: conn.close()