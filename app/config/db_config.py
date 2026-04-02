import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="db.irwkwwtrimebxuaqvglf.supabase.co"
        port="5432",
        user="postgres",
        password="chclmdlvg821130",
        dbname="postgres",
        sslmode="require"  # <--- ESTA LÍNEA ES OBLIGATORIA PARA RENDER
    )