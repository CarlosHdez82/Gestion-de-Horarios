import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.faculties_model import FacultyCreate # Usamos los nuevos modelos
from fastapi.encoders import jsonable_encoder

class FacultiesController:

    def create_faculty(self, faculty: FacultyCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Dejamos que la DB maneje las fechas automáticamente
            cursor.execute("""
                INSERT INTO faculties (name, is_active)
                VALUES (%s, %s)
                RETURNING id;
            """, (faculty.name, faculty.is_active))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Facultad creada exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            print(f"Error en create_faculty: {err}")
            raise HTTPException(status_code=500, detail="Error al crear la facultad")
        finally:
            if conn: conn.close()

    def get_faculty(self, faculties_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, is_active, created_at, updated_at 
                FROM faculties 
                WHERE id = %s
            """, (faculties_id,))
            result = cursor.fetchone()
            
            if result:
                content = {
                    'faculties_id': result[0],
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': result[3],
                    'updated_at': result[4]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Facultad no encontrada")
        finally:
            if conn: conn.close()

    def get_faculties(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Ordenamos por nombre para que se vea bien en la tabla de la CUL
            cursor.execute("SELECT id, name, is_active, created_at, updated_at FROM faculties ORDER BY name ASC")
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                payload.append({
                    'faculties_id': data[0],
                    'name': data[1],
                    'is_active': data[2],
                    'created_at': data[3],
                    'updated_at': data[4]
                })
            
            # Devolvemos la lista limpia directamente
            return payload
        finally:
            if conn: conn.close()

    def update_faculty(self, faculties_id: int, faculty: FacultyCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Solo actualizamos name e is_active. updated_at lo maneja la DB
            cursor.execute("""
                UPDATE faculties
                SET name = %s, is_active = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING id, name, is_active, created_at, updated_at;
            """, (faculty.name, faculty.is_active, faculties_id))
            
            result = cursor.fetchone()
            conn.commit()
            
            if result:
                return jsonable_encoder({
                    'faculties_id': result[0],
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': result[3],
                    'updated_at': result[4]
                })
            else:
                raise HTTPException(status_code=404, detail="Facultad no encontrada")
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar facultad")
        finally:
            if conn: conn.close()

    def delete_faculty(self, faculties_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM faculties
                WHERE id = %s
                RETURNING id, name;
            """, (faculties_id,))
            result = cursor.fetchone()
            conn.commit()
            
            if result:
                return {"mensaje": f"Facultad '{result[1]}' eliminada"}
            else:
                raise HTTPException(status_code=404, detail="Facultad no encontrada")
        finally:
            if conn: conn.close()