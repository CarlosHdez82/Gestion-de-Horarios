import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.users_model import UserCreate, UserResponse
from fastapi.encoders import jsonable_encoder
import hashlib
import jwt  # La versión de Python
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env

class UsersController:

    def create_user(self, user: UserCreate): # <-- Cambiado a UserCreate
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # PASO CLAVE: Convertimos la password plana a hash SHA-256
            # Esto mantiene la consistencia con tu función de login
            hashed_password = hashlib.sha256(user.password.strip().encode()).hexdigest()

            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password_hash, role_id, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (
                user.first_name, 
                user.last_name, 
                user.email, 
                hashed_password, # <-- Guardamos el hash generado, no la clave plana
                user.role_id, 
                user.is_active
            ))
            conn.commit()
            return {"resultado": "Usuario creado con éxito"}
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
            # 1. Traemos solo las columnas que el modelo UserResponse necesita
            # IMPORTANTE: No traemos 'password_hash'
            cursor.execute("""
                SELECT id, first_name, last_name, email, role_id, is_active, created_at 
                FROM users 
                WHERE id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            
            if result:
                # 2. Mapeamos el resultado a un diccionario
                content = {
                    'user_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'role_id': result[4],
                    'is_active': result[5],
                    'created_at': result[6] # Pydantic lo validará como datetime
                }
                # 3. Lo pasamos por jsonable_encoder para que FastAPI lo envíe como JSON
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Usuario de la CUL no encontrado")
                
        except psycopg2.Error as err:
            print(f"Error en get_user: {err}")
            raise HTTPException(status_code=500, detail="Error interno de la base de datos")
        finally:
            if conn:
                conn.close()

    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 1. Traemos columnas específicas (SIN password_hash)
            # Esto asegura que el orden en data[0], data[1], etc. siempre sea el mismo
            cursor.execute("""
                SELECT id, first_name, last_name, email, role_id, is_active, created_at 
                FROM users 
                ORDER BY created_at DESC
            """)
            
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                # 2. Construimos el diccionario que coincide con UserResponse
                content = {
                    'user_id': data[0],
                    'first_name': data[1],
                    'last_name': data[2],
                    'email': data[3],
                    'role_id': data[4],
                    'is_active': data[5],
                    'created_at': data[6] # Pydantic lo procesará como datetime
                }
                payload.append(content)
            
            # 3. Devolvemos la lista directamente (sin el wrapper "resultado" si prefieres 
            # que FastAPI la valide con el response_model de la ruta)
            return payload

        except psycopg2.Error as err:
            print(f"Error en base de datos: {err}")
            raise HTTPException(status_code=500, detail="No se pudo obtener la lista de usuarios")
        finally:
            if conn:
                conn.close()

    def update_user(self, user_id: int, user: UserCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 1. Procesamos la contraseña (Hash SHA-256)
            # Esto asegura que si el admin cambia la clave, el usuario pueda loguearse
            hashed_password = hashlib.sha256(user.password.strip().encode()).hexdigest()

            # 2. Ejecutamos el UPDATE con columnas específicas
            # Usamos 'id' en el WHERE porque así suele llamarse la PK en Postgres/Supabase
            query = """
                UPDATE users
                SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    password_hash = %s,
                    role_id = %s,
                    is_active = %s,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING id, first_name, last_name, email, role_id, is_active, created_at;
            """
            
            cursor.execute(query, (
                user.first_name, 
                user.last_name, 
                user.email, 
                hashed_password, 
                user.role_id, 
                user.is_active, 
                user_id
            ))
            
            result = cursor.fetchone()
            conn.commit()

            if result:
                # 3. Construimos la respuesta basada en el molde UserResponse
                content = {
                    'user_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'role_id': result[4],
                    'is_active': result[5],
                    'created_at': result[6] 
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Usuario no encontrado en la CUL")

        except psycopg2.Error as err:
            if conn: conn.rollback()
            print(f"Error en update_user: {err}")
            raise HTTPException(status_code=500, detail="Error al actualizar en la base de datos")
        finally:
            if conn: conn.close()

    def delete_user(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 1. Ejecutamos el DELETE y retornamos los datos (MENOS la contraseña)
            # Usamos RETURNING para confirmar qué se borró exactamente
            query = """
                DELETE FROM users 
                WHERE id = %s 
                RETURNING id, first_name, last_name, email, role_id, is_active, created_at;
            """
            
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            conn.commit()

            if result:
                # 2. Mapeamos al formato de UserResponse para que Svelte reciba 
                # la confirmación del usuario eliminado.
                content = {
                    'user_id': int(result[0]),
                    'first_name': result[1],
                    'last_name': result[2],
                    'email': result[3],
                    'role_id': result[4],
                    'is_active': result[5],
                    'created_at': result[6]
                }
                return jsonable_encoder(content)
            else:
                # Si el ID no existe en la base de datos de la CUL
                raise HTTPException(status_code=404, detail="El usuario no existe o ya fue eliminado")

        except psycopg2.Error as err:
            if conn: conn.rollback()
            print(f"Error en delete_user: {err}")
            raise HTTPException(status_code=500, detail="No se pudo eliminar el registro")
        finally:
            if conn:
                conn.close()
    
    
    def login_user(self, email: str, password: str):
        conn = None # Inicializamos conn para evitar errores en el finally
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, first_name, last_name, email, password_hash, role_id, is_active, created_at, updated_at
                FROM users
                WHERE email = %s
            """, (email,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=401, detail="Usuario no encontrado")

            # Extraemos los datos de la DB
            db_id, db_first_name, db_last_name, db_email, db_password_hash, db_role_id, db_is_active, db_created_at, db_updated_at = result

            # PASO 2: Convertir la password que ingresa el usuario a SHA-256
            input_password_hashed = hashlib.sha256(password.strip().encode()).hexdigest()

            # --- AGREGA ESTAS LÍNEAS PARA DEPURAR ---
            print(f"DEBUG -> Email ingresado: {email}")
            print(f"DEBUG -> Password ingresado (sin hash): {password}")
            print(f"DEBUG -> Input Hash: {input_password_hashed}")
            print(f"DEBUG -> DB Hash:    {db_password_hash}")
            
            # PASO 3: Comparar el hash generado con el hash de la base de datos
            if input_password_hashed.strip() != db_password_hash.strip():
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            # Mapeo de roles ajustado para tu SvelteKit
            roles_map = {
                1: "admi",
                2: "faculty",
                3: "teacher",
                4: "student"
            }
            role_name = roles_map.get(db_role_id, "Desconocido")
            
            # --- INICIO IMPLEMENTACIÓN JWT ---
            
            # 1. Traemos la clave secreta desde tu archivo .env
            SECRET_KEY = os.getenv("JWT_SECRET")
            ALGORITHM = "HS256"

            # 2. Creamos el Payload (la información que va dentro del token)
            # 'exp' es la fecha de expiración (8 horas desde ahora)
            # 'sub' es el estándar para el ID del usuario
            payload = {
                "sub": str(db_id),
                "email": db_email,
                "role": role_name,
                "exp": datetime.now(timezone.utc) + timedelta(hours=8)
            }

            # 3. Generamos el token codificado
            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            # --- FIN IMPLEMENTACIÓN JWT ---

            # Respuesta exitosa enviando el TOKEN al Frontend
            content = {
                "user_id": db_id,
                "first_name": db_first_name,
                "last_name": db_last_name,
                "email": db_email,
                "role_id": db_role_id,
                "role_name": role_name,
                "token": token,  # <-- El frontend de la CUL guardará esto
                "is_active": db_is_active,
                "message": "Login exitoso"
            }
            return jsonable_encoder(content)

        except psycopg2.Error as err:
            print(f"ERROR REAL DE DB: {err.pgerror}") # Esto te dirá si falta una columna o si la tabla no existe
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()