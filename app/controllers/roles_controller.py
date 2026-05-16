# ============================================================
# roles_controller.py — Controlador de Roles de Usuario
# ============================================================
# Contiene la lógica de negocio para gestionar los roles del
# sistema. Los roles determinan el nivel de acceso y permisos
# de cada usuario (ej: Administrador, Docente, Coordinador).
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
from app.models.roles_model import RoleCreate

class RolesController:

    # ------------------------------------------------------------
    # POST — Crear un nuevo rol
    # Las fechas created_at y updated_at las maneja automáticamente
    # la BD mediante valores DEFAULT definidos en la tabla.
    # RETURNING id retorna el ID generado sin segunda consulta.
    # ------------------------------------------------------------
    def create_role(self, role: RoleCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # La BD asigna created_at y updated_at automáticamente
            cursor.execute("""
                INSERT INTO roles (name)
                VALUES (%s) RETURNING id
            """, (role.name,))
            new_id = cursor.fetchone()[0]   # Captura el ID generado por PostgreSQL
            conn.commit()                   # Confirma la transacción en la BD
            return {"mensaje": "Rol creado exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()        # Deshace cambios si algo falla
            raise HTTPException(status_code=500, detail=f"Error al crear rol: {str(err)}")
        finally:
            if conn: conn.close()           # Cierra la conexión aunque ocurra un error

    # ------------------------------------------------------------
    # GET — Obtener un rol por ID
    # Usa %s como placeholder para evitar inyección SQL.
    # La coma en (id,) convierte el valor en tupla, requerido por psycopg2.
    # jsonable_encoder convierte el dict a formato serializable por FastAPI.
    # Si no encuentra el registro, lanza un error 404.
    # ------------------------------------------------------------
    def get_role(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, created_at, updated_at FROM roles WHERE id = %s", (id,))
            result = cursor.fetchone()      # Retorna solo la primera fila o None
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

    # ------------------------------------------------------------
    # GET — Obtener todos los roles
    # Ordena por ID ascendente para mostrar los roles en el orden
    # en que fueron creados (del más antiguo al más reciente).
    # FastAPI serializa automáticamente la lista de diccionarios a JSON.
    # ------------------------------------------------------------
    def get_roles(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, created_at, updated_at FROM roles ORDER BY id ASC")
            result = cursor.fetchall()      # Retorna todas las filas como lista de tuplas

            # Construimos una lista de diccionarios a partir de las tuplas
            # accediendo a cada columna por su índice posicional
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'name': data[1],
                    'created_at': data[2],
                    'updated_at': data[3]
                })
            return payload  # FastAPI serializa la lista automáticamente a JSON
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT — Actualizar un rol existente
    # updated_at=NOW() registra automáticamente la fecha y hora
    # de la última modificación usando la función de PostgreSQL.
    # RETURNING id, name confirma que el UPDATE fue exitoso y
    # retorna los datos del registro actualizado.
    # Si no retorna nada, el registro no existe → 404.
    # ------------------------------------------------------------
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
            if result:                      # Si retorna algo, el UPDATE fue exitoso
                return {"mensaje": "Rol actualizado", "id": result[0]}
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        except psycopg2.Error:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar el rol")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE — Eliminar un rol por ID
    # RETURNING id confirma que el registro existía y fue eliminado.
    # Si hay usuarios con este rol asignado, PostgreSQL lanzará un
    # error de integridad referencial (FK) que capturamos con
    # psycopg2.Error y retornamos como error 400.
    # Importante: eliminar un rol con usuarios activos rompería
    # el sistema de permisos, por eso se bloquea a nivel de BD.
    # ------------------------------------------------------------
    def delete_role(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM roles WHERE id = %s RETURNING id", (id,))
            result = cursor.fetchone()
            conn.commit()
            if result:                      # Si retorna algo, el DELETE fue exitoso
                return {"mensaje": "Rol eliminado correctamente"}
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        except psycopg2.Error:
            if conn: conn.rollback()
            # Error 400 indica que la operación no es posible por restricciones de la BD
            # Un rol asignado a usuarios activos no puede eliminarse
            raise HTTPException(status_code=400, detail="No se puede eliminar: existen usuarios asociados a este rol")
        finally:
            if conn: conn.close()