# ============================================================
# teacheravailability_controller.py — Controlador de Disponibilidad Docente
# ============================================================
# Contiene la lógica de negocio para gestionar la disponibilidad
# horaria de los docentes. Incluye métodos estándar CRUD y dos
# métodos especiales diseñados para el grid visual de Svelte:
# - get_availability_by_teacher: carga los bloques de un docente
# - clear_teacher_availability: reinicia todo el grid de un docente
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
from app.models.teacheravailability_model import TeacherAvailabilityCreate

class AvailabilityController:

    # ------------------------------------------------------------
    # GET — Obtener todos los bloques de disponibilidad
    # LEFT JOIN con users trae el nombre completo del docente.
    # LEFT JOIN con academic_periods trae el nombre del periodo.
    # La concatenación first_name || ' ' || last_name une nombre
    # y apellido en un solo string legible para el frontend.
    # Ordena por día y franja horaria ascendente.
    # ------------------------------------------------------------
    def get_availabilities(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT a.id, a.teacher_id, a.period_id, a.day_of_week, a.block_label,
                       a.is_active, a.created_at, a.updated_at,
                       (u.first_name || ' ' || u.last_name) AS teacher_name,
                       p.name AS period_name
                FROM teacher_availability a
                LEFT JOIN users u ON a.teacher_id = u.id
                LEFT JOIN academic_periods p ON a.period_id = p.id
                ORDER BY a.day_of_week, a.block_label ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()  # Retorna todas las filas como lista de tuplas

            # Construimos una lista de diccionarios a partir de las tuplas
            # accediendo a cada columna por su índice posicional
            payload = []
            for d in result:
                payload.append({
                    "id": d[0],
                    "teacher_id": d[1],
                    "period_id": d[2],
                    "day_of_week": d[3],
                    "block_label": d[4],
                    "is_active": d[5],
                    "created_at": d[6],
                    "updated_at": d[7],
                    "teacher_name": d[8],   # Obtenido del JOIN con users
                    "period_name": d[9]     # Obtenido del JOIN con academic_periods
                })
            return payload
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener disponibilidades: {str(e)}")
        finally:
            if conn: conn.close()           # Cierra la conexión aunque ocurra un error

    # ------------------------------------------------------------
    # GET especial — Obtener bloques de un docente en un periodo
    # Diseñado exclusivamente para el grid visual de Svelte.
    # Filtra por teacher_id, period_id y is_active=True para
    # retornar solo los bloques marcados como disponibles.
    # Retorna id, day y block — el formato mínimo que necesita
    # el componente grid para pintar las celdas seleccionadas.
    # El id se incluye para poder eliminar bloques desde el grid.
    # ------------------------------------------------------------
    def get_availability_by_teacher(self, teacher_id: int, period_id: int):
        """Especial para Svelte: Carga los bloques ocupados para pintar el grid"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, day_of_week, block_label
                FROM teacher_availability
                WHERE teacher_id = %s AND period_id = %s AND is_active = True
            """, (teacher_id, period_id))
            result = cursor.fetchall()

            # List comprehension para convertir las tuplas al formato
            # simplificado que necesita el grid de Svelte
            return [{"id": d[0], "day": d[1], "block": d[2]} for d in result]
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # POST — Registrar un nuevo bloque de disponibilidad
    # Cada bloque representa un día y franja horaria en que el
    # docente está disponible dentro del periodo académico.
    # Si el bloque ya existe (restricción UNIQUE en la BD),
    # PostgreSQL lanza un error que retornamos como 409 Conflict,
    # que es más preciso que 400 para indicar duplicados.
    # ------------------------------------------------------------
    def create_availability(self, data: TeacherAvailabilityCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teacher_availability (teacher_id, period_id, day_of_week, block_label)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (data.teacher_id, data.period_id, data.day_of_week, data.block_label))

            new_id = cursor.fetchone()[0]   # Captura el ID generado por PostgreSQL
            conn.commit()                   # Confirma la transacción en la BD
            return {"mensaje": "Bloque de disponibilidad guardado", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()        # Deshace cambios si algo falla
            # 409 Conflict es más semánticamente correcto que 400
            # para indicar que el recurso ya existe en la BD
            raise HTTPException(status_code=409, detail="Este bloque ya está registrado para el docente.")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT — Actualizar un bloque de disponibilidad existente
    # Permite modificar docente, periodo, día o franja horaria.
    # updated_at=NOW() registra la fecha de modificación en la BD.
    # Si hay conflicto con un bloque duplicado → 409 Conflict.
    # Si el registro no existe → 404 Not Found.
    # ------------------------------------------------------------
    def update_availability(self, id: int, data: TeacherAvailabilityCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE teacher_availability
                SET teacher_id=%s, period_id=%s, day_of_week=%s, block_label=%s, updated_at=NOW()
                WHERE id=%s RETURNING id
            """, (data.teacher_id, data.period_id, data.day_of_week, data.block_label, id))
            if cursor.fetchone():           # Si retorna algo, el UPDATE fue exitoso
                conn.commit()
                return {"mensaje": "Disponibilidad actualizada correctamente"}
            raise HTTPException(status_code=404, detail="No se encontró el registro")
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=409, detail="Conflicto al actualizar el bloque.")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE — Eliminar un bloque de disponibilidad por ID
    # RETURNING id confirma que el registro existía y fue eliminado.
    # Se usa para eliminar bloques individuales desde el grid de Svelte
    # cuando el docente desmarca una celda específica.
    # ------------------------------------------------------------
    def delete_availability(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM teacher_availability WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():           # Si retorna algo, el DELETE fue exitoso
                conn.commit()
                return {"mensaje": "Disponibilidad eliminada correctamente"}
            raise HTTPException(status_code=404, detail="No se encontró el registro")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE especial — Limpiar todo el grid de un docente
    # Elimina TODOS los bloques de disponibilidad de un docente
    # en un periodo específico de una sola vez.
    # Se usa cuando el docente necesita redefinir su disponibilidad
    # desde cero sin tener que eliminar bloque por bloque.
    # No lanza 404 si no hay registros, ya que un grid vacío
    # es un estado válido (el docente aún no ha marcado nada).
    # ------------------------------------------------------------
    def clear_teacher_availability(self, teacher_id: int, period_id: int):
        """Limpia todo el grid del docente para re-programar"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM teacher_availability
                WHERE teacher_id = %s AND period_id = %s
            """, (teacher_id, period_id))
            conn.commit()
            return {"mensaje": "Grid reiniciado correctamente"}
        finally:
            if conn: conn.close()