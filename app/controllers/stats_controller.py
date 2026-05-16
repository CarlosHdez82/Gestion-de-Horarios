# ============================================================
# stats_controller.py — Controlador de Estadísticas / Dashboard
# ============================================================
# Obtiene las métricas globales del sistema en una sola consulta
# optimizada para alimentar el dashboard principal de la CUL.
# En lugar de hacer múltiples consultas separadas, usa subconsultas
# SELECT COUNT(*) dentro de un solo SELECT para mayor eficiencia.
# ============================================================

import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection

class StatsController:

    # ------------------------------------------------------------
    # GET — Obtener resumen de métricas del sistema
    # Usa subconsultas COUNT(*) en un solo SELECT para obtener
    # todos los conteos en una única ida a la BD, lo que es
    # significativamente más rápido que ejecutar 6 queries separadas.
    #
    # role_id = 3 filtra únicamente los usuarios con rol docente.
    # Si el ID del rol docente cambia en la BD, este valor
    # debe actualizarse para mantener el conteo correcto.
    # ------------------------------------------------------------
    def get_stats_summary(self):
        """
        Obtiene el conteo total de registros en una sola consulta.
        Optimización para el Dashboard de la CUL.
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Una sola consulta con subconsultas COUNT(*) por tabla
            # es más eficiente que 6 queries individuales separadas
            query = """
                SELECT
                    (SELECT COUNT(*) FROM users) as total_users,
                    (SELECT COUNT(*) FROM faculties) as total_faculties,
                    (SELECT COUNT(*) FROM programs) as total_programs,
                    (SELECT COUNT(*) FROM users WHERE role_id = 3) as total_teachers,
                    (SELECT COUNT(*) FROM subjects) as total_subjects,
                    (SELECT COUNT(*) FROM schedules) as total_schedules;
            """

            cursor.execute(query)
            data = cursor.fetchone()    # Retorna una sola fila con todos los conteos

            # Estructuramos el resultado como diccionario JSON para el frontend
            # Accedemos a cada conteo por su índice posicional en la tupla
            return {
                "usuarios": data[0],            # Total de usuarios registrados
                "facultades": data[1],          # Total de facultades activas
                "programas": data[2],           # Total de programas académicos
                "docentes": data[3],            # Usuarios con role_id = 3 (rol Docente)
                "materias": data[4],            # Total de materias registradas
                "horarios": data[5],            # Total de bloques de horario asignados
                "periodo_actual": "2026-1",     # Periodo vigente (actualizar cada semestre)
                "estado_sistema": "Operacional" # Estado general de la plataforma
            }

        except psycopg2.Error as e:
            print(f"Error en stats: {e}")       # Log en consola para diagnóstico
            raise HTTPException(
                status_code=500,
                detail="Error al sincronizar las métricas del Dashboard"
            )

        finally:
            if conn: conn.close()               # Cierra la conexión aunque ocurra un error

# ------------------------------------------------------------
# Instancia global del controlador
# Se crea una sola vez al importar el módulo, evitando
# instanciar el objeto en cada petición al endpoint.
# ------------------------------------------------------------
stats_controller = StatsController()