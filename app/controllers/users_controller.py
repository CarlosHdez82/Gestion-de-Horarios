import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.users_model import UserCreate
from fastapi.encoders import jsonable_encoder
import hashlib
import jwt 
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

class UsersController:

    def create_user(self, user: UserCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Hashing SHA-256
            # Cambiado a user.password_hash para coincidir con tu clase UserCreate
            hashed_password = hashlib.sha256(user.password_hash.strip().encode()).hexdigest()

            # Se agrega 'program_id' al INSERT para que Neon no rechace la fila
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password_hash, role_id, program_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (
                user.first_name, 
                user.last_name, 
                user.email, 
                hashed_password, 
                user.role_id, 
                user.program_id,
                user.is_active
            ))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Usuario creado con éxito", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            # Imprimimos el error técnico en la terminal para que puedas debuguear mejor
            print(f"Error detectado en Neon/Postgres: {err}")
            raise HTTPException(status_code=400, detail="El correo ya está registrado o los datos son inválidos")
        finally:
            if conn: conn.close()

    def get_users(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Traemos el nombre del rol con un JOIN para el frontend de Svelte
            cursor.execute("""
                SELECT u.id, u.first_name, u.last_name, u.email, u.role_id, u.is_active, u.created_at, r.name as role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                ORDER BY u.id ASC
            """)
            result = cursor.fetchall()
            payload = []
            for data in result:
                payload.append({
                    'id': data[0], 'first_name': data[1], 'last_name': data[2],
                    'email': data[3], 'role_id': data[4], 'is_active': data[5],
                    'created_at': data[6], 'role_name': data[7]
                })
            return payload
        finally:
            if conn: conn.close()

    def login_user(self, email: str, password: str):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.first_name, u.last_name, u.email, u.password_hash, u.role_id, u.is_active, r.name as role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.email = %s AND u.is_active = True
            """, (email,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=401, detail="Credenciales incorrectas o usuario inactivo")

            db_id, db_fname, db_lname, db_email, db_hash, db_role_id, db_active, db_role_name = result

            # Verificar Hash (usando SHA-256 según tu configuración)
            input_hash = hashlib.sha256(password.strip().encode()).hexdigest()
            if input_hash != db_hash:
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

            # Generar JWT
            SECRET_KEY = os.getenv("JWT_SECRET", "tu_clave_secreta_por_defecto")
            payload = {
                "sub": str(db_id),
                "email": db_email,
                "role": db_role_name,
                "exp": datetime.now(timezone.utc) + timedelta(hours=8)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return {
                "id": db_id,
                "full_name": f"{db_fname} {db_lname}",
                "email": db_email,
                "role": db_role_name,
                "token": token,
                "message": "Bienvenido al sistema CUL"
            }
        finally:
            if conn: conn.close()

    def delete_user(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Usuario eliminado"}
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        except psycopg2.Error:
            if conn: conn.rollback()
            raise HTTPException(status_code=400, detail="No se puede eliminar: el usuario tiene registros asociados.")
        finally:
            if conn: conn.close()