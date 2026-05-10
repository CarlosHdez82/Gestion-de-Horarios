import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.users_model import UserCreate
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
            hashed_password = hashlib.sha256(user.password_hash.strip().encode()).hexdigest()

            # Insertamos en la tabla users de Neon
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
            print(f"Error detectado en Neon/Postgres: {err}")
            raise HTTPException(status_code=400, detail="El correo ya está registrado o los datos son inválidos")
        finally:
            if conn: conn.close()

    def get_teachers(self):
        """Especial para la vista de administración de docentes"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # JOIN triple para traer info completa de ubicación
            cursor.execute("""
                SELECT u.id, u.first_name, u.last_name, u.email, u.role_id, u.program_id, u.is_active,
                       r.name as role_name, p.name as program_name, f.name as faculty_name, f.id as faculty_id
                FROM users u
                JOIN roles r ON u.role_id = r.id
                LEFT JOIN programs p ON u.program_id = p.id
                LEFT JOIN faculties f ON p.faculty_id = f.id
                WHERE r.name ILIKE 'teacher' OR r.name ILIKE 'Docente'
                ORDER BY u.last_name ASC
            """)
            result = cursor.fetchall()
            payload = []
            for d in result:
                payload.append({
                    'id': d[0], 'first_name': d[1], 'last_name': d[2],
                    'email': d[3], 'role_id': d[4], 'program_id': d[5],
                    'is_active': d[6], 'role_name': d[7], 'program_name': d[8],
                    'faculty_name': d[9], 'faculty_id': d[10]
                })
            return payload
        finally:
            if conn: conn.close()

    def update_user(self, id: int, user: UserCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # No actualizamos el password_hash aquí por seguridad (usar otra ruta para eso)
            cursor.execute("""
                UPDATE users 
                SET first_name = %s, last_name = %s, email = %s, 
                    role_id = %s, program_id = %s, is_active = %s, updated_at = NOW()
                WHERE id = %s RETURNING id;
            """, (user.first_name, user.last_name, user.email, 
                  user.role_id, user.program_id, user.is_active, id))
            
            if cursor.fetchone():
                conn.commit()
                return {"mensaje": "Usuario actualizado"}
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            if conn: conn.close()

    def login_user(self, email: str, password: str):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.first_name, u.last_name, u.email, u.password_hash, r.name as role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.email = %s AND u.is_active = True
            """, (email,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=401, detail="Credenciales incorrectas o usuario inactivo")

            db_id, db_fname, db_lname, db_email, db_hash, db_role_name = result

            input_hash = hashlib.sha256(password.strip().encode()).hexdigest()
            if input_hash != db_hash:
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

            SECRET_KEY = os.getenv("JWT_SECRET", "cul_secret_key_2024")
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
                "token": token
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
            raise HTTPException(status_code=400, detail="Error: El usuario tiene registros asociados (ej: disponibilidad o materias).")
        finally:
            if conn: conn.close()