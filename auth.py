"""
auth.py

Autenticación mediante Bearer Token.
"""

import secrets

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from models import Login


router = APIRouter(
    tags=["Autenticación"]
)


# ==========================
# Base de usuarios
# ==========================

USUARIOS = {
    "admin": "secreto123"
}


# ==========================
# Tokens activos
# ==========================

TOKENS_ACTIVOS = {}


# ==========================
# Esquema Bearer
# ==========================

security = HTTPBearer()


# ==========================
# Login
# ==========================

@router.post(
    "/login",
    summary="Iniciar sesión",
    description="Genera un Bearer Token válido."
)
def login(datos: Login):

    password = USUARIOS.get(datos.usuario)

    if password != datos.password:

        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos."
        )

    token = secrets.token_hex(32)

    TOKENS_ACTIVOS[token] = datos.usuario

    return {
        "access_token": token,
        "token_type": "Bearer"
    }


# ==========================
# Verificación del token
# ==========================

def verificar_token(
    credenciales: HTTPAuthorizationCredentials = Depends(security)
):

    token = credenciales.credentials

    if token not in TOKENS_ACTIVOS:

        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado."
        )

    return TOKENS_ACTIVOS[token]