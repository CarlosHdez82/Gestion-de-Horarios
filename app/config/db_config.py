import psycopg2
import socket

def get_db_connection():
    host = "db.irwkwwtrimebxuaqvglf.supabase.co"
    addr = socket.gethostbyname(host)  # fuerza IPv4
    return psycopg2.connect(
        host=addr,
        port="5432",
        user="postgres",
        password="chclmdlvg821130",
        dbname="postgres",
        sslmode="require"
    )