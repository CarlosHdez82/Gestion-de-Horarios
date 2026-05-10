import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection

class StatsController:
    def get_stats_summary(self):
        """
        Obtiene el conteo total de registros en una sola consulta
        optimización para el Dashboard de la CUL.
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Consultamos todo de un solo golpe para mayor velocidad
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
            data = cursor.fetchone()

            # Estructuramos la respuesta para el Frontend
            return {
                "usuarios": data[0],
                "facultades": data[1],
                "programas": data[2],
                "docentes": data[3], # Ahora viene de users con role_id = 3
                "materias": data[4],
                "horarios": data[5],
                "periodo_actual": "2026-1",
                "estado_sistema": "Operacional"
            }

        except psycopg2.Error as e:
            print(f"Error en stats: {e}")
            raise HTTPException(
                status_code=500, 
                detail="Error al sincronizar las métricas del Dashboard"
            )
        
        finally:
            if conn:
                conn.close()

# Instancia lista para los endpoints
stats_controller = StatsController()