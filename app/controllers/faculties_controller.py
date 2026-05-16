# ============================================================
# faculties_controller.py — Controlador de Facultades
# ============================================================
# Contiene la lógica de negocio para gestionar las facultades.
# Cada método se conecta a la BD, ejecuta una consulta SQL
# y retorna el resultado o lanza un error HTTP.
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
from app.models.faculties_model import FacultyCreate

class FacultiesController:

    # ------------------------------------------------------------
    # POST — Crear una nueva facultad
    # RETURNING id hace que PostgreSQL retorne el ID del registro
    # recién insertado sin necesidad de hacer una segunda consulta.
    # conn.commit() confirma la transacción; sin esto los cambios
    # no se guardan permanentemente en la BD.
    # ------------------------------------------------------------
    def create_faculty(self, faculty: FacultyCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO faculties (name, is_active)
                VALUES (%s, %s)
                RETURNING id;
            """, (faculty.name, faculty.is_active))

            new_id = cursor.fetchone()[0]   # Captura el ID generado por PostgreSQL
            conn.commit()                   # Confirma la transacción en la BD
            return {"mensaje": "Facultad creada exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()        # Deshace cambios si algo falla
            raise HTTPException(status_code=500, detail=f"Error al crear la facultad: {str(err)}")
        finally:
            if conn: conn.close()           # Cierra la conexión aunque ocurra un error

    # ------------------------------------------------------------
    # GET — Obtener una facultad por ID
    # Usa %s como placeholder para evitar inyección SQL.
    # La coma en (id,) convierte el valor en tupla, requerido por psycopg2.
    # jsonable_encoder convierte el dict a un formato serializable por FastAPI.
    # Si no encuentra el registro, lanza un error 404.
    # ------------------------------------------------------------
    def get_faculty(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, is_active, created_at, updated_at
                FROM faculties
                WHERE id = %s
            """, (id,))             # La coma convierte id en tupla, requerido por psycopg2
            result = cursor.fetchone()  # Retorna solo la primera fila o None

            if result:
                content = {
                    'id': result[0],
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': result[3],
                    'updated_at': result[4]
                }
                return jsonable_encoder(content)
            raise HTTPException(status_code=404, detail="Facultad no encontrada")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # GET — Obtener todas las facultades
    # Ordena alfabéticamente por nombre (ORDER BY name ASC)
    # para facilitar la visualización en el frontend.
    # Convierte cada fila de la BD en un diccionario JSON.
    # ------------------------------------------------------------
    def get_faculties(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, is_active, created_at, updated_at FROM faculties ORDER BY name ASC")
            result = cursor.fetchall()  # Retorna todas las filas como lista de tuplas

            # Construimos una lista de diccionarios a partir de las tuplas
            # accediendo a cada columna por su índice posicional
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'name': data[1],
                    'is_active': data[2],
                    'created_at': data[3],
                    'updated_at': data[4]
                })
            return payload
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT — Actualizar una facultad existente
    # updated_at=NOW() registra automáticamente la fecha y hora
    # de la última modificación usando la función de PostgreSQL.
    # RETURNING retorna los datos actualizados directamente,
    # evitando una segunda consulta para obtener el registro.
    # Si no retorna nada, el registro no existe → 404.
    # ------------------------------------------------------------
    def update_faculty(self, id: int, faculty: FacultyCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE faculties
                SET name = %s, is_active = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING id, name, is_active, created_at, updated_at;
            """, (faculty.name, faculty.is_active, id))

            result = cursor.fetchone()
            conn.commit()

            if result:
                # Retorna directamente los datos actualizados sin consulta adicional
                return jsonable_encoder({
                    'id': result[0],
                    'name': result[1],
                    'is_active': result[2],
                    'created_at': result[3],
                    'updated_at': result[4]
                })
            raise HTTPException(status_code=404, detail="Facultad no encontrada")
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar facultad")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE — Eliminar una facultad por ID
    # RETURNING id, name confirma que el registro existía y fue
    # eliminado, además permite incluir el nombre en el mensaje
    # de confirmación para mayor claridad.
    # Si la facultad tiene programas asociados, PostgreSQL lanzará
    # un error de integridad referencial (FK) que capturamos con
    # psycopg2.Error y retornamos como error 400.
    # ------------------------------------------------------------
    def delete_faculty(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM faculties
                WHERE id = %s
                RETURNING id, name;
            """, (id,))
            result = cursor.fetchone()
            conn.commit()

            if result:
                return {"mensaje": f"Facultad '{result[1]}' eliminada correctamente"}
            raise HTTPException(status_code=404, detail="Facultad no encontrada")
        except psycopg2.Error as err:
            if conn: conn.rollback()
            # Error 400 indica que la operación no es posible por restricciones de la BD
            # Una facultad con programas asociados no puede eliminarse (integridad referencial)
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar la facultad porque tiene programas académicos asociados."
            )
        finally:
            if conn: conn.close()