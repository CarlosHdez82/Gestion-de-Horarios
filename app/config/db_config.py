# ============================================================
# db_config.py — Configuración de Conexión a la Base de Datos
# ============================================================
# Gestiona la conexión a la base de datos PostgreSQL alojada
# en Neon (neon.tech), un servicio de PostgreSQL serverless
# en la nube que requiere SSL en todas sus conexiones.
#
# Las credenciales NUNCA se escriben directamente en el código.
# Se leen desde el archivo .env para mantenerlas seguras y
# facilitar el cambio entre entornos (desarrollo, producción).
# ============================================================

import psycopg2
import os
from dotenv import load_dotenv

# ------------------------------------------------------------
# Carga las variables de entorno definidas en el archivo .env
# Debe llamarse antes de cualquier os.getenv() para que las
# variables estén disponibles en el entorno de Python.
# En producción (Render, Railway, etc.) las variables se
# configuran directamente en el panel del servidor, no en .env
# ------------------------------------------------------------
load_dotenv()

def get_db_connection():
    """
    Establece y retorna una conexión con la base de datos de Neon.
    Neon utiliza PostgreSQL estándar pero requiere SSL en todas las conexiones.
    Retorna el objeto de conexión o None si falla.
    """
    try:
        # ------------------------------------------------------------
        # Parámetros de conexión leídos desde el archivo .env
        # Estructura del .env requerida:
        #   NEON_HOST     = ep-xxx.us-east-2.aws.neon.tech
        #   NEON_PORT     = 5432
        #   NEON_DB       = nombre_base_de_datos
        #   NEON_USER     = nombre_usuario
        #   NEON_PASSWORD = contraseña_segura
        #
        # Separar los parámetros individualmente es más organizado
        # que usar el connection string completo de Neon, y permite
        # cambiar cada valor de forma independiente.
        # ------------------------------------------------------------
        conn = psycopg2.connect(
            host=os.getenv("NEON_HOST"),
            port=os.getenv("NEON_PORT", 5432),  # Puerto estándar de PostgreSQL
            database=os.getenv("NEON_DB"),
            user=os.getenv("NEON_USER"),
            password=os.getenv("NEON_PASSWORD"),
            sslmode="require"   # CRÍTICO: Neon rechaza conexiones sin SSL
                                # Omitir esto causará un error de conexión
        )

        # Línea de diagnóstico para confirmar que el endpoint de Neon
        # está activo y accesible
        print("Conectado exitosamente al endpoint de NEON")

        return conn     # Retorna el objeto de conexión activo

    except Exception as e:
        # Registra el error en consola para diagnóstico
        # En producción considera usar logging en lugar de print
        print(f"Error al conectar con NEON: {e}")
        return None     # Retorna None para que el controlador maneje el fallo