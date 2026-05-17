# ============================================================
# users_controller.py — Controlador de Usuarios y Autenticación
# ============================================================
# El controlador más completo del sistema. Gestiona el CRUD de
# usuarios y maneja la autenticación mediante JWT (JSON Web Tokens).
#
# Tecnologías usadas:
# - hashlib   → hashing SHA-256 para almacenar contraseñas de forma segura
# - jwt       → generación y firma de tokens de acceso
# - dotenv    → carga de variables de entorno (JWT_SECRET)
#
# Patrón de cada método:
# 1. Abrir conexión a la BD
# 2. Ejecutar consulta SQL
# 3. Retornar resultado
# 4. Manejar errores con HTTPException
# 5. Cerrar conexión en el bloque finally (siempre se ejecuta)
# ============================================================

import psycopg2
import hashlib
import jwt
import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from dotenv import load_dotenv
from app.config.db_config import get_db_connection
from app.models.users_model import UserCreate

# Carga las variables de entorno definidas en el archivo .env
# Debe llamarse antes de usar os.getenv() para que estén disponibles
load_dotenv()

class UsersController:

    # ------------------------------------------------------------
    # POST — Crear un nuevo usuario
    # La contraseña nunca se guarda en texto plano.
    # Se aplica SHA-256 antes de insertar en la BD:
    #   .strip()   → elimina espacios accidentales al inicio/fin
    #   .encode()  → convierte el string a bytes (requerido por hashlib)
    #   .hexdigest() → retorna el hash como string hexadecimal
    # Si el email ya existe (restricción UNIQUE), PostgreSQL lanza
    # un error que capturamos y retornamos como error 400.
    # ------------------------------------------------------------
    def create_user(self, user: UserCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Aplicamos SHA-256 a la contraseña antes de guardarla en la BD
            hashed_password = hashlib.sha256(user.password_hash.strip().encode()).hexdigest()

            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password_hash, role_id, program_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (
                user.first_name,
                user.last_name,
                user.email,
                hashed_password,    # Guardamos el hash, nunca la contraseña original
                user.role_id,
                user.program_id,
                user.is_active
            ))

            new_id = cursor.fetchone()[0]   # Captura el ID generado por PostgreSQL
            conn.commit()                   # Confirma la transacción en la BD
            return {"mensaje": "Usuario creado con éxito", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()        # Deshace cambios si algo falla
            print(f"Error detectado en Neon/Postgres: {err}")
            # Error 400 porque es un problema de datos (email duplicado o datos inválidos)
            raise HTTPException(status_code=400, detail="El correo ya está registrado o los datos son inválidos")
        finally:
            if conn: conn.close()           # Cierra la conexión aunque ocurra un error

    # ------------------------------------------------------------
    # GET — Obtener todos los usuarios
    # JOIN con roles para incluir el nombre del rol en la respuesta,
    # evitando que el frontend tenga que hacer una consulta adicional.
    # INNER JOIN (no LEFT JOIN) porque todo usuario debe tener un rol.
    # Ordena alfabéticamente por apellido.
    # ------------------------------------------------------------
    def get_users(self):
        """Lista todos los usuarios registrados"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.first_name, u.last_name, u.email,
                       u.role_id, u.program_id, u.is_active,
                       r.name as role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                ORDER BY u.last_name ASC
            """)
            result = cursor.fetchall()

            # Construimos una lista de diccionarios a partir de las tuplas
            payload = []
            for row in result:
                payload.append({
                    'id': row[0], 'first_name': row[1], 'last_name': row[2],
                    'email': row[3], 'role_id': row[4], 'program_id': row[5],
                    'is_active': row[6], 'role_name': row[7]  # Obtenido del JOIN con roles
                })
            return payload
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # GET — Obtener un usuario por ID
    # Consulta simple sin JOIN ya que solo se necesitan los datos
    # básicos del usuario, no el nombre de su rol.
    # Si no encuentra el registro, lanza un error 404.
    # ------------------------------------------------------------
    def get_user(self, id: int):
        """Obtiene un usuario por ID"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.first_name, u.last_name, u.email,
                       u.role_id, u.program_id, u.is_active
                FROM users u WHERE u.id = %s
            """, (id,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {
                'id': row[0], 'first_name': row[1], 'last_name': row[2],
                'email': row[3], 'role_id': row[4], 'program_id': row[5],
                'is_active': row[6]
            }
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # GET especial — Obtener solo los docentes
    # Diseñado para la vista de administración de docentes.
    # Usa un JOIN triple para retornar información completa:
    #   - roles     → nombre del rol para verificar que es docente
    #   - programs  → nombre del programa al que pertenece
    #   - faculties → nombre y ID de la facultad del programa
    # ILIKE hace la búsqueda insensible a mayúsculas/minúsculas,
    # funcionando tanto con 'teacher' como con 'Docente'.
    # LEFT JOIN en programs y faculties porque un docente podría
    # no tener programa asignado aún.
    # ------------------------------------------------------------
    def get_teachers(self):
        """Especial para la vista de administración de docente"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
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
                    'is_active': d[6],
                    'role_name': d[7],      # Obtenido del JOIN con roles
                    'program_name': d[8],   # Obtenido del JOIN con programs
                    'faculty_name': d[9],   # Obtenido del JOIN con faculties
                    'faculty_id': d[10]     # Obtenido del JOIN con faculties
                })
            return payload
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT — Actualizar información de un usuario
    # IMPORTANTE: Este método NO actualiza la contraseña por seguridad.
    # El cambio de contraseña se maneja en el método change_password,
    # que requiere verificación de la contraseña actual.
    # updated_at=NOW() registra la fecha de modificación en la BD.
    # ------------------------------------------------------------
    def update_user(self, id: int, user: UserCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # password_hash se excluye intencionalmente de este UPDATE
            # para evitar que se sobreescriba accidentalmente
            cursor.execute("""
                UPDATE users
                SET first_name = %s, last_name = %s, email = %s,
                    role_id = %s, program_id = %s, is_active = %s, updated_at = NOW()
                WHERE id = %s RETURNING id;
            """, (user.first_name, user.last_name, user.email,
                  user.role_id, user.program_id, user.is_active, id))

            if cursor.fetchone():           # Si retorna algo, el UPDATE fue exitoso
                conn.commit()
                return {"mensaje": "Usuario actualizado"}
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # POST — Autenticar usuario y generar token JWT
    # Proceso de autenticación en 3 pasos:
    # 1. Buscar usuario por email verificando que esté activo
    # 2. Comparar el hash SHA-256 de la contraseña ingresada
    #    con el hash almacenado en la BD
    # 3. Si coinciden, generar un token JWT firmado que expira
    #    en 8 horas y retornarlo junto con los datos del usuario
    #
    # JWT_SECRET se lee del .env para mayor seguridad.
    # El payload del token incluye id, email, rol y expiración.
    # timezone.utc garantiza que la expiración use UTC consistentemente.
    # ------------------------------------------------------------
    def login_user(self, email: str, password: str):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Paso 1: Buscar usuario activo por email con su rol
            cursor.execute("""
                SELECT u.id, u.first_name, u.last_name, u.email, u.password_hash, r.name as role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.email = %s AND u.is_active = True
            """, (email,))
            result = cursor.fetchone()

            # Si no existe o está inactivo, rechazamos sin revelar cuál falló
            if not result:
                raise HTTPException(status_code=401, detail="Credenciales incorrectas o usuario inactivo")

            db_id, db_fname, db_lname, db_email, db_hash, db_role_name = result

            # Paso 2: Hashear la contraseña ingresada y comparar con la BD
            input_hash = hashlib.sha256(password.strip().encode()).hexdigest()
            if input_hash != db_hash:
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

            # Paso 3: Generar token JWT firmado con la clave secreta del .env
            SECRET_KEY = os.getenv("JWT_SECRET", "cul_secret_key_2024")
            payload = {
                "sub": str(db_id),          # Subject: ID del usuario como string
                "email": db_email,          # Email incluido en el token para referencia
                "role": db_role_name,       # Rol para control de acceso en el frontend
                "exp": datetime.now(timezone.utc) + timedelta(hours=8)  # Expira en 8 horas
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            # Retornamos el token y datos básicos del usuario para el frontend
            return {
                "id": db_id,
                "full_name": f"{db_fname} {db_lname}",
                "email": db_email,
                "role": db_role_name,
                "token": token              # El frontend debe guardar este token y
                                            # enviarlo en cada petición como: Bearer {token}
            }
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE — Eliminar un usuario por ID
    # RETURNING id confirma que el registro existía y fue eliminado.
    # Si el usuario tiene registros asociados (disponibilidad,
    # horarios, etc.), PostgreSQL lanzará un error de integridad
    # referencial (FK) que capturamos como error 400.
    # ------------------------------------------------------------
    def delete_user(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():           # Si retorna algo, el DELETE fue exitoso
                conn.commit()
                return {"mensaje": "Usuario eliminado"}
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        except psycopg2.Error:
            if conn: conn.rollback()
            raise HTTPException(status_code=400, detail="Error: El usuario tiene registros asociados (ej: disponibilidad o materias).")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT especial — Cambiar contraseña del usuario
    # Proceso en 2 pasos para mayor seguridad:
    # 1. Verificar que la contraseña actual sea correcta comparando
    #    su hash con el almacenado en la BD
    # 2. Solo si coincide, hashear y guardar la nueva contraseña
    #
    # El bloque 'except HTTPException: raise' reenvía los errores
    # 400 del paso 1 sin que sean capturados por el except general,
    # evitando que se conviertan en errores 500 incorrectamente.
    # ------------------------------------------------------------
    def change_password(self, id: int, current_password: str, new_password: str):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Paso 1: Verificar que la contraseña actual sea correcta
            current_hash = hashlib.sha256(current_password.strip().encode()).hexdigest()
            cursor.execute("SELECT id FROM users WHERE id = %s AND password_hash = %s", (id, current_hash))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")

            # Paso 2: Hashear y guardar la nueva contraseña
            new_hash = hashlib.sha256(new_password.strip().encode()).hexdigest()
            cursor.execute(
                "UPDATE users SET password_hash = %s, updated_at = NOW() WHERE id = %s",
                (new_hash, id)
            )
            conn.commit()
            return {"mensaje": "Contraseña actualizada correctamente"}
        except HTTPException:
            raise     # Reenvía el error 400 del paso 1 sin transformarlo en error 500
        except Exception as e:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn: conn.close()