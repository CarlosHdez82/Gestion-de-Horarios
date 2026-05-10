import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.programs_model import ProgramCreate
from fastapi.encoders import jsonable_encoder

class ProgramsController:

    def get_programs(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # SQL explícito con JOIN para traer el nombre de la facultad
            query = """
                SELECT p.id, p.name, p.faculty_id, p.is_active, p.created_at, p.updated_at, f.name AS faculty_name 
                FROM programs p
                LEFT JOIN faculties f ON p.faculty_id = f.id
                ORDER BY p.name ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'name': data[1],
                    'faculty_id': data[2],
                    'is_active': data[3],
                    'created_at': data[4],
                    'updated_at': data[5],
                    'faculty_name': data[6]
                })
            return payload
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail="Error al obtener la lista de programas")
        finally:
            if conn: conn.close()

    def get_program(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT p.id, p.name, p.faculty_id, p.is_active, p.created_at, p.updated_at, f.name AS faculty_name 
                FROM programs p
                LEFT JOIN faculties f ON p.faculty_id = f.id
                WHERE p.id = %s
            """
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result:
                content = {
                    'id': result[0],
                    'name': result[1],
                    'faculty_id': result[2],
                    'is_active': result[3],
                    'created_at': result[4],
                    'updated_at': result[5],
                    'faculty_name': result[6]
                }
                return jsonable_encoder(content)
            raise HTTPException(status_code=404, detail="Programa académico no encontrado")
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error de base de datos al buscar el programa")
        finally:
            if conn: conn.close()

    def create_program(self, program: ProgramCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO programs (name, faculty_id)
                VALUES (%s, %s) RETURNING id;
            """, (program.name, program.faculty_id))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Programa creado con éxito", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=400, detail="Error al crear: verifique que la facultad exista")
        finally:
            if conn: conn.close()

    def update_program(self, id: int, program: ProgramCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE programs 
                SET name=%s, faculty_id=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (program.name, program.faculty_id, id))
            
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Programa actualizado correctamente"}
            raise HTTPException(status_code=404, detail="Programa no encontrado para actualizar")
        except psycopg2.Error:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail="Error al intentar actualizar el programa")
        finally:
            if conn: conn.close()

    def delete_program(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM programs WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Programa eliminado correctamente"}
            raise HTTPException(status_code=404, detail="El programa no existe")
        except psycopg2.Error:
            if conn: conn.rollback()
            # Bloqueo por integridad si el programa tiene docentes o materias
            raise HTTPException(
                status_code=400, 
                detail="No se puede eliminar: el programa tiene materias o docentes asociados."
            )
        finally:
            if conn: conn.close()