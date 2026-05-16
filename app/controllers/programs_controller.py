# ============================================================
# programs_controller.py — Controlador de Programas Académicos
# ============================================================
# Contiene la lógica de negocio para gestionar los programas
# académicos. Usa LEFT JOIN con la tabla de facultades para
# retornar el nombre de la facultad junto con cada programa,
# evitando consultas adicionales desde el frontend.
#
# Patrón de cada método:
# 1. Abrir conexión a la BD
# 2. Ejecutar consulta SQL
# 3. Retornar resultado
# 4. Manejar errores con HTTPException
# 5. Cerrar conexión en el bloque finally (siempre se ejecuta)
# ============================================================

import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.db_config import get_db_connection
from app.models.programs_model import ProgramCreate

class ProgramsController:

    # ------------------------------------------------------------
    # GET — Obtener todos los programas académicos
    # LEFT JOIN con faculties trae el nombre de la facultad
    # en la misma consulta, sin necesidad de una segunda query.
    # LEFT JOIN (en lugar de INNER JOIN) asegura que se retornen
    # programas aunque no tengan facultad asignada.
    # Ordena alfabéticamente por nombre de programa.
    # ------------------------------------------------------------
    def get_programs(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT p.id, p.name, p.faculty_id, p.is_active, p.created_at, p.updated_at, f.name AS faculty_name
                FROM programs p
                LEFT JOIN faculties f ON p.faculty_id = f.id
                ORDER BY p.name ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()  # Retorna todas las filas como lista de tuplas

            # Construimos una lista de diccionarios a partir de las tuplas
            # accediendo a cada columna por su índice posicional
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'name': data[1],
                    'faculty_id': data[2],
                    'is_active': data[3],
                    'created_at': data[4],
                    'updated_at': data[5],
                    'faculty_name': data[6]     # Obtenido del JOIN con faculties
                })
            return payload
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail="Error al obtener la lista de programas")
        finally:
            if conn: conn.close()           # Cierra la conexión aunque ocurra un error

    # ------------------------------------------------------------
    # GET — Obtener un programa por ID
    # Mismo LEFT JOIN para incluir el nombre de la facultad.
    # Usa %s como placeholder para evitar inyección SQL.
    # jsonable_encoder convierte el dict a formato serializable por FastAPI.
    # Si no encuentra el registro, lanza un error 404.
    # ------------------------------------------------------------
    def get_program(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT p.id, p.name, p.faculty_id, p.is_active, p.created_at, p.updated_at, f.name AS faculty_name
                FROM programs p
                LEFT JOIN faculties f ON p.faculty_id = f.id
                WHERE p.id = %s
            """
            cursor.execute(query, (id,))        # La coma convierte id en tupla, requerido por psycopg2
            result = cursor.fetchone()          # Retorna solo la primera fila o None

            if result:
                content = {
                    'id': result[0],
                    'name': result[1],
                    'faculty_id': result[2],
                    'is_active': result[3],
                    'created_at': result[4],
                    'updated_at': result[5],
                    'faculty_name': result[6]   # Obtenido del JOIN con faculties
                }
                return jsonable_encoder(content)
            raise HTTPException(status_code=404, detail="Programa académico no encontrado")
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error de base de datos al buscar el programa")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # POST — Crear un nuevo programa académico
    # RETURNING id hace que PostgreSQL retorne el ID del registro
    # recién insertado sin necesidad de hacer una segunda consulta.
    # Si faculty_id no existe en la tabla faculties, PostgreSQL
    # lanzará un error de integridad referencial (FK) → error 400.
    # ------------------------------------------------------------
    def create_program(self, program: ProgramCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO programs (name, faculty_id)
                VALUES (%s, %s) RETURNING id;
            """, (program.name, program.faculty_id))

            new_id = cursor.fetchone()[0]   # Captura el ID generado por PostgreSQL
            conn.commit()                   # Confirma la transacción en la BD
            return {"mensaje": "Programa creado con éxito", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()        # Deshace cambios si algo falla
            # Error 400 porque es un problema de datos, no del servidor
            raise HTTPException(status_code=400, detail="Error al crear: verifique que la facultad exista")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT — Actualizar un programa existente
    # updated_at=NOW() registra automáticamente la fecha y hora
    # de la última modificación usando la función de PostgreSQL.
    # Si RETURNING id no retorna nada, el registro no existe → 404.
    # ------------------------------------------------------------
    def update_program(self, id: int, program: ProgramCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE programs
                SET name=%s, faculty_id=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (program.name, program.faculty_id, id))

            if cursor.fetchone():           # Si retorna algo, el UPDATE fue exitoso
                conn.commit()
                return {"mensaje": "Programa actualizado correctamente"}
            raise HTTPException(status_code=404, detail="Programa no encontrado para actualizar")
        except psycopg2.Error:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail="Error al intentar actualizar el programa")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE — Eliminar un programa por ID
    # RETURNING id confirma que el registro existía y fue eliminado.
    # Si el programa tiene materias o docentes asociados, PostgreSQL
    # lanzará un error de integridad referencial (FK) que capturamos
    # con psycopg2.Error y retornamos como error 400.
    # ------------------------------------------------------------
    def delete_program(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM programs WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():           # Si retorna algo, el DELETE fue exitoso
                conn.commit()
                return {"mensaje": "Programa eliminado correctamente"}
            raise HTTPException(status_code=404, detail="El programa no existe")
        except psycopg2.Error:
            if conn: conn.rollback()
            # Error 400 indica que la operación no es posible por restricciones de la BD
            # Un programa con materias o docentes asociados no puede eliminarse
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar: el programa tiene materias o docentes asociados."
            )
        finally:
            if conn: conn.close()