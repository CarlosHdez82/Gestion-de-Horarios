import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection

class SubjectsController:
    def get_subjects(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # CORRECCIÓN EN EL JOIN: s.program_id se une con p.id
            query = """
                SELECT 
                    s.id, 
                    s.name, 
                    s.code, 
                    s.credits, 
                    s.program_id, 
                    s.is_active, 
                    s.created_at, 
                    s.updated_at, 
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
                    "created_at": str(data[6]) if data[6] else None,
                    "updated_at": str(data[7]) if data[7] else None,
                    "program_name": data[8]
                })
            return payload
        except Exception as e:
            print(f"Error detallado en get_subjects: {e}")
            raise HTTPException(status_code=500, detail=f"Error en la consulta: {str(e)}")
        finally:
            if conn: conn.close()

    # Asegúrate de aplicar el mismo cambio en get_subject (singular)
    def get_subject(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT s.*, p.name AS program_name 
                FROM subjects s 
                LEFT JOIN programs p ON s.program_id = p.id 
                WHERE s.id = %s
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return {
                    "id": data[0], "name": data[1], "code": data[2],
                    "credits": data[3], "program_id": data[4],
                    "is_active": data[5], "program_name": data[8]
                }
            raise HTTPException(status_code=404, detail="Materia no encontrada")
        finally:
            if conn: conn.close()

    def create_subject(self, subject):
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
            return {"mensaje": "Materia registrada", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def update_subject(self, id: int, subject):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE subjects SET name=%s, code=%s, credits=%s, program_id=%s, is_active=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (subject.name, subject.code, subject.credits, subject.program_id, subject.is_active, id))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Materia actualizada"}
            raise HTTPException(status_code=404, detail="No encontrada")
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
                return {"mensaje": "Materia eliminada"}
            raise HTTPException(status_code=404, detail="No encontrada")
        finally:
            if conn: conn.close()