# ============================================================
# schedules_controller.py — Controlador de Horarios
# ============================================================
# Contiene la lógica de negocio para gestionar los horarios
# académicos. El método get_schedules usa múltiples LEFT JOINs
# para retornar nombres legibles de docente, materia y periodo
# en una sola consulta, evitando llamadas adicionales desde
# el frontend.
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
from app.models.schedules_model import ScheduleCreate

class SchedulesController:

    # ------------------------------------------------------------
    # POST — Crear un nuevo bloque de horario
    # Registra la asignación de una materia a un docente en un
    # día, franja horaria y grupo específicos dentro de un periodo.
    # RETURNING id retorna el ID generado sin segunda consulta.
    # ------------------------------------------------------------
    def create_schedule(self, schedule: ScheduleCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO schedules (teacher_id, subject_id, period_id, day_of_week, block_label, group_code)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """, (schedule.teacher_id, schedule.subject_id, schedule.period_id,
                  schedule.day_of_week, schedule.block_label, schedule.group_code))

            new_id = cursor.fetchone()[0]   # Captura el ID generado por PostgreSQL
            conn.commit()                   # Confirma la transacción en la BD
            return {"mensaje": "Carga académica asignada exitosamente", "id": new_id}
        except psycopg2.Error as err:
            if conn: conn.rollback()        # Deshace cambios si algo falla
            raise HTTPException(status_code=500, detail=f"Error al asignar horario: {err}")
        finally:
            if conn: conn.close()           # Cierra la conexión aunque ocurra un error

    # ------------------------------------------------------------
    # GET — Obtener todos los horarios
    # Usa múltiples LEFT JOINs para enriquecer cada registro con
    # nombres legibles en lugar de solo IDs numéricos:
    #   - users       → nombre completo del docente
    #   - subjects    → nombre y código de la materia
    #   - academic_periods → nombre del periodo académico
    #
    # COALESCE retorna el primer valor no nulo de la lista,
    # evitando que aparezcan campos NULL en la respuesta cuando
    # alguna relación no existe (ej: docente eliminado).
    #
    # Concatenación: first_name || ' ' || last_name une nombre
    # y apellido del docente en un solo string.
    #
    # Orden: periodo descendente (más reciente primero),
    # luego día y franja horaria ascendente.
    # ------------------------------------------------------------
    def get_schedules(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT
                    s.id, s.teacher_id, s.subject_id, s.period_id, s.day_of_week,
                    s.block_label, COALESCE(s.group_code, 'A') as group_code, s.created_at,
                    COALESCE(u.first_name || ' ' || u.last_name, 'Sin asignar') AS teacher_name,
                    COALESCE(sub.name, 'Sin materia') AS subject_name,
                    COALESCE(sub.code, '') AS subject_code,
                    COALESCE(ap.name, 'Sin periodo') AS period_name
                FROM schedules s
                LEFT JOIN users u ON s.teacher_id = u.id
                LEFT JOIN subjects sub ON s.subject_id = sub.id
                LEFT JOIN academic_periods ap ON s.period_id = ap.id
                ORDER BY ap.name DESC, s.day_of_week, s.block_label ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()  # Retorna todas las filas como lista de tuplas

            # Construimos una lista de diccionarios a partir de las tuplas
            # accediendo a cada columna por su índice posicional
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'teacher_id': data[1],
                    'subject_id': data[2],
                    'period_id': data[3],
                    'day_of_week': data[4],
                    'block_label': data[5],
                    'group_code': data[6],
                    'created_at': data[7],
                    'teacher_name': data[8],    # Obtenido del JOIN con users
                    'subject_name': data[9],    # Obtenido del JOIN con subjects
                    'subject_code': data[10],   # Obtenido del JOIN con subjects
                    'period_name': data[11]     # Obtenido del JOIN con academic_periods
                })
            return payload
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener horarios: {str(err)}")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # PUT — Actualizar un bloque de horario existente
    # Permite modificar cualquier campo del horario: docente,
    # materia, periodo, día, franja horaria o grupo.
    # updated_at=NOW() registra la fecha de modificación en la BD.
    # Si RETURNING id no retorna nada, el registro no existe → 404.
    # ------------------------------------------------------------
    def update_schedule(self, id: int, schedule: ScheduleCreate):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE schedules SET
                    teacher_id=%s, subject_id=%s, period_id=%s,
                    day_of_week=%s, block_label=%s, group_code=%s, updated_at=NOW()
                WHERE id=%s RETURNING id;
            """, (schedule.teacher_id, schedule.subject_id, schedule.period_id,
                  schedule.day_of_week, schedule.block_label, schedule.group_code, id))

            if cursor.fetchone():           # Si retorna algo, el UPDATE fue exitoso
                conn.commit()
                return {"mensaje": "Horario actualizado correctamente"}
            raise HTTPException(status_code=404, detail="Registro de horario no encontrado")
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar el horario")
        finally:
            if conn: conn.close()

    # ------------------------------------------------------------
    # DELETE — Eliminar un bloque de horario por ID
    # RETURNING id confirma que el registro existía y fue eliminado.
    # Si no retorna nada, el registro no existe → 404.
    # Los horarios pueden eliminarse libremente ya que no tienen
    # tablas dependientes con restricciones de integridad (FK).
    # ------------------------------------------------------------
    def delete_schedule(self, id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM schedules WHERE id = %s RETURNING id", (id,))
            if cursor.fetchone():           # Si retorna algo, el DELETE fue exitoso
                conn.commit()
                return {"mensaje": "Carga académica eliminada"}
            raise HTTPException(status_code=404, detail="El registro no existe")
        finally:
            if conn: conn.close()