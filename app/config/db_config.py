import psycopg2
import os
from dotenv import load_dotenv

# 1. Cargamos las variables de entorno
load_dotenv()

def get_db_connection():
    """
    Establece una conexión con la base de datos de NEON.
    Neon utiliza PostgreSQL estándar pero requiere SSL para todas las conexiones.
    """
    try:
        # 2. Usamos las variables de NEON
        # Es común que Neon te dé un "Connection String" completo, 
        # pero separarlo así es más organizado para tu código.
        conn = psycopg2.connect(
            host=os.getenv("NEON_HOST"),
            port=os.getenv("NEON_PORT", 5432), # Por defecto es 5432
            database=os.getenv("NEON_DB"),
            user=os.getenv("NEON_USER"),
            password=os.getenv("NEON_PASSWORD"),
            sslmode="require"  # CRÍTICO: Neon no acepta conexiones sin SSL
        )
        
        # Opcional: Esto confirma que el endpoint de Neon está activo
        # print("✅ Conectado exitosamente al endpoint de NEON")
        return conn
        
    except Exception as e:
        print(f"❌ Error al conectar con NEON: {e}")
        return None