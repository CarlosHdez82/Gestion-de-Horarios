import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection

class StatsController:
    def get_stats_summary(self):
        """
        Obtiene el conteo total de registros de las tablas principales
        para mostrar en las tarjetas del Dashboard.
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 1. Conteo de Usuarios
            cursor.execute("SELECT COUNT(*) FROM users;")
            usuarios = cursor.fetchone()[0]

            # 2. Conteo de Facultades
            cursor.execute("SELECT COUNT(*) FROM faculties;")
            facultades = cursor.fetchone()[0]

            # 3. Conteo de Programas
            cursor.execute("SELECT COUNT(*) FROM programs;")
            programas = cursor.fetchone()[0]

            # 4. Conteo de Docentes (Filtrando por el rol 3 si es necesario)
            cursor.execute("SELECT COUNT(*) FROM teachers;")
            docentes = cursor.fetchone()[0]

            # 5. Conteo de Materias
            cursor.execute("SELECT COUNT(*) FROM subjects;")
            materias = cursor.fetchone()[0]

            # 6. Conteo de Horarios Generados
            # Ajusta el nombre de la tabla 'schedules' según tu DB
            cursor.execute("SELECT COUNT(*) FROM schedules;")
            horarios = cursor.fetchone()[0]

            return {
                "usuarios": usuarios,
                "facultades": facultades,
                "programas": programas,
                "docentes": docentes,
                "materias": materias,
                "horarios": horarios,
                "periodo_actual": "2026-1"
            }

        except psycopg2.Error as e:
            print(f"Error en base de datos: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener estadísticas de la CUL")
        
        finally:
            if conn:
                conn.close()

# Instanciamos el controlador para usarlo en las rutas
stats_controller = StatsController()