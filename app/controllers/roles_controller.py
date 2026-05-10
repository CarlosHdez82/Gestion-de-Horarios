import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.roles_model import RoleCreate # Usamos el modelo estandarizado
from fastapi.encoders import jsonable_encoder

class RolesController:
        
    def create_role(self, role: RoleCreate):   
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Dejamos que la DB maneje las fechas
            cursor.execute("""
                INSERT INTO roles (name) 
                VALUES (%s) RETURNING id
            """, (role.name,))
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Rol creado exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear rol: {str(err)}")
        finally:
            if conn: conn.close()

    def get_role(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, created_at, updated_at FROM roles WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'id': result[0],
                    'name': result[1],
                    'created_at': result[2],
                    'updated_at': result[3]
                }
                return jsonable_encoder(content)
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        finally:
            if conn: conn.close()
       
    def get_roles(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, created_at, updated_at FROM roles ORDER BY id ASC")
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'name': data[1],
                    'created_at': data[2],
                    'updated_at': data[3]
                })
            return payload # FastAPI se encarga de serializar la lista
        finally:
            if conn: conn.close()

    def update_role(self, id: int, role: RoleCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE roles
                SET name = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING id, name;
            """, (role.name, id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                return {"mensaje": "Rol actualizado", "id": result[0]}
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        except psycopg2.Error:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar el rol")
        finally:
            if conn: conn.close()

    def delete_role(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM roles WHERE id = %s RETURNING id", (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                return {"mensaje": "Rol eliminado correctamente"}
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        except psycopg2.Error:
            if conn: conn.rollback()
            # Importante: No se puede borrar si hay usuarios con este rol
            raise HTTPException(status_code=400, detail="No se puede eliminar: existen usuarios asociados a este rol")
        finally:
            if conn: conn.close()