import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.subjects_model import SubjectCreate
from fastapi.encoders import jsonable_encoder

class SubjectsController:

    def get_subjects(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT 
                    s.id, s.name, s.code, s.credits, s.program_id, 
                    s.is_active, s.created_at, s.updated_at, 
                    p.name AS program_name 
                FROM subjects s
                LEFT JOIN programs p ON s.program_id = p.id
                ORDER BY s.name ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                payload.append({
                    "id": data[0],
                    "name": data[1],
                    "code": data[2],
                    "credits": data[3],
                    "program_id": data[4],
                    "is_active": data[5],
                    "created_at": data[6],
                    "updated_at": data[7],
                    "program_name": data[8]
                })
            return payload
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener materias: {str(e)}")
        finally:
            if conn: conn.close()

    def get_subject(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT 
                    s.id, s.name, s.code, s.credits, s.program_id, 
                    s.is_active, s.created_at, s.updated_at,
                    p.name AS program_name 
                FROM subjects s 
                LEFT JOIN programs p ON s.program_id = p.id 
                WHERE s.id = %s
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                content = {
                    "id": data[0], "name": data[1], "code": data[2],
                    "credits": data[3], "program_id": data[4],
                    "is_active": data[5], "created_at": data[6], 
                    "updated_at": data[7], "program_name": data[8]
                }
                return jsonable_encoder(content)
            raise HTTPException(status_code=404, detail="Materia no encontrada")
        finally:
            if conn: conn.close()

    def create_subject(self, subject: SubjectCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO subjects (name, code, credits, program_id, is_active)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """, (subject.name, subject.code, subject.credits, subject.program_id, subject.is_active))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Materia registrada exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error: Verifique si el código ya existe o el programa es válido. {err}")
        finally:
            if conn: conn.close()

    def update_subject(self, id: int, subject: SubjectCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE subjects 
                SET name=%s, code=%s, credits=%s, program_id=%s, is_active=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (subject.name, subject.code, subject.credits, subject.program_id, subject.is_active, id))
            
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Materia actualizada correctamente"}
            raise HTTPException(status_code=404, detail="Materia no encontrada para actualizar")
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")
        finally:
            if conn: conn.close()

    def delete_subject(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Materia eliminada correctamente"}
            raise HTTPException(status_code=404, detail="La materia no existe")
        except psycopg2.Error:
            if conn: conn.rollback()
            # Seguridad: No borrar si ya está en algún horario (schedules)
            raise HTTPException(
                status_code=400, 
                detail="No se puede eliminar: la materia ya tiene horarios asignados."
            )
        finally:
            if conn: conn.close()