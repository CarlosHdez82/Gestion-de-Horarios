import psycopg2
import os
from dotenv import load_dotenv

# 1. Cargamos las variables de entorno del archivo .env
load_dotenv()

def get_db_connection():
    """
    Establece una conexión con la base de datos de Supabase 
    utilizando las credenciales del archivo .env.
    """
    try:
        # 2. Intentamos conectar usando os.getenv para cada parámetro
        conn = psycopg2.connect(
            host=os.getenv("SUPABASE_HOST"),
            port=os.getenv("SUPABASE_PORT"),
            database=os.getenv("SUPABASE_DB"),
            user=os.getenv("SUPABASE_USER"),
            password=os.getenv("SUPABASE_PASSWORD"),
            sslmode="require"  # Supabase requiere SSL por seguridad
        )
        print("✅ Conexión exitosa a la base de datos en Supabase")
        return conn
        
    except Exception as e:
        # 3. Si algo falla (contraseña errónea, sin internet, etc.), atrapamos el error
        print(f"❌ Error al intentar conectar: {e}")
        return None