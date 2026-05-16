# ============================================================
# login_model.py — Modelos de Autenticación
# ============================================================
# Define la estructura de datos para el proceso de login.
# Contiene el modelo de entrada (credenciales) y el modelo
# de respuesta (token JWT + datos del usuario autenticado).
# ============================================================

from pydantic import BaseModel, EmailStr, Field

# ------------------------------------------------------------
# Modelo de Solicitud de Login — usado en POST /users/login
# Recibe las credenciales del usuario desde el frontend.
# Pydantic valida automáticamente el formato y las restricciones
# antes de que el dato llegue al controlador.
# ------------------------------------------------------------
class LoginRequest(BaseModel):
    # EmailStr valida que el valor tenga formato de correo real
    # Field(...) indica que el campo es obligatorio
    # example aparece en /docs (Swagger UI) como valor de ejemplo
    email: EmailStr = Field(..., example="docente@cul.edu.co")

    # min_length=6 rechaza contraseñas muy cortas como medida
    # básica contra ataques de fuerza bruta
    password: str = Field(..., min_length=6, example="contraseña123")

# ------------------------------------------------------------
# Modelo de Respuesta de Login — retornado tras autenticación exitosa
# Contiene el token JWT que el frontend (Svelte) debe almacenar
# y enviar en cada petición protegida como cabecera Authorization.
# ------------------------------------------------------------
class LoginResponse(BaseModel):
    access_token: str       # Token JWT firmado que expira según configuración
    token_type: str = "bearer"  # Tipo estándar de token para APIs REST
    user: dict              # Datos básicos del usuario: nombre, rol y programa
                            # Se usa dict para flexibilidad, ya que el contenido
                            # puede variar según el rol del usuario autenticado