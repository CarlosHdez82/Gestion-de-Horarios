import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.users_model import Users
from fastapi.encoders import jsonable_encoder

class UsersController:

    def create_user(self, user: Users):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password_hash, role_id, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (user.first_name, user.last_name, user.email, user.password_hash, user.role_id, user.is_active))
            conn.commit()
            return {"resultado": "Usuario creado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'user_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'password_hash': result[4],
                    'role_id': result[5],
                    'is_active': result[6],
                    'created_at': str(result[7])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'user_id': data[0],
                    'first_name': data[1],
                    'last_name': data[2],
                    'email': data[3],
                    'password_hash': data[4],
                    'role_id': data[5],
                    'is_active': data[6],
                    'created_at': str(data[7])
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No users found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def update_user(self, user_id: int, user: Users):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    password_hash = %s,
                    role_id = %s,
                    is_active = %s
                WHERE user_id = %s
                RETURNING user_id, first_name, last_name, email, password_hash, role_id, is_active, created_at;
            """, (user.first_name, user.last_name, user.email, user.password_hash, user.role_id, user.is_active, user_id))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'user_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'password_hash': result[4],
                    'role_id': result[5],
                    'is_active': result[6],
                    'created_at': str(result[7])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()

    def delete_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM users
                WHERE user_id = %s
                RETURNING user_id, first_name, last_name, email, password_hash, role_id, is_active, created_at;
            """, (user_id,))
            result = cursor.fetchone()
            conn.commit()
            if result:
                content = {
                    'user_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'password_hash': result[4],
                    'role_id': result[5],
                    'is_active': result[6],
                    'created_at': str(result[7])
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()