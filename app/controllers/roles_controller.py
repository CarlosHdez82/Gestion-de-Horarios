import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.roles_model import Roles
from fastapi.encoders import jsonable_encoder

class RolesController:
        
    def create_role(self, role: Roles):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO roles (name, is_active, created_at, updated_at) 
                VALUES (%s, %s, %s, %s)
            """, (role.name, role.is_active, role.created_at, role.updated_at))
            conn.commit()
            return {"resultado": "Rol creado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_role(self, role_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM roles WHERE role_id = %s", (role_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'role_id': int(result[0]),
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': str(result[3]),
                    'updated_at': str(result[4])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Rol not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
       
    def get_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM roles")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'role_id': data[0],
                    'name': data[1],
                    'is_active': data[2],
                    'created_at': str(data[3]),
                    'updated_at': str(data[4])
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="Rol not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_role(self, role_id: int, role: Roles):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE roles
                SET name = %s, is_active = %s, created_at = %s, updated_at = %s
                WHERE role_id = %s
                RETURNING role_id, name, is_active, created_at, updated_at;
            """, (role.name, role.is_active, role.created_at, role.updated_at, role_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'role_id': int(result[0]),
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': str(result[3]),
                    'updated_at': str(result[4])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Rol not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_role(self, role_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM roles
                WHERE role_id = %s
                RETURNING role_id, name, is_active, created_at, updated_at;
            """, (role_id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'role_id': int(result[0]),
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': str(result[3]),
                    'updated_at': str(result[4])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Rol not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()