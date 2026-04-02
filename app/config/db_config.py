import os
import psycopg2
import socket

def get_db_connection():
    host = os.getenv("DB_HOST", "db.irwkwwtrimebxuaqvglf.supabase.co")
    addr = socket.gethostbyname(host)  # fuerza IPv4
    return psycopg2.connect(
        host=addr,
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "TU_PASSWORD"),
        dbname=os.getenv("DB_NAME", "postgres"),
        sslmode=os.getenv("DB_SSLMODE", "require")
    )