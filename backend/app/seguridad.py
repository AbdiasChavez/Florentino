"""Contraseñas, sesiones del personal, tokens del cliente y códigos 2FA.

Solo usa la biblioteca estándar: PBKDF2-SHA256 para contraseñas y códigos,
HMAC-SHA256 para firmar sesiones y SHA-256 para guardar los tokens del cliente
(nunca se guardan en claro: RNF-05).
"""
import base64
import hashlib
import hmac
import json
import secrets
from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import config, reloj
from app.db import get_db
from app.models import RolUsuario, Usuario

_ITERACIONES = 260_000


def hash_secreto(secreto: str) -> str:
    sal = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", secreto.encode(), sal.encode(), _ITERACIONES)
    return f"pbkdf2_sha256${_ITERACIONES}${sal}${dk.hex()}"


def verificar_secreto(secreto: str, guardado: str | None) -> bool:
    if not guardado:
        return False
    try:
        _, iteraciones, sal, esperado = guardado.split("$")
    except ValueError:
        return False
    dk = hashlib.pbkdf2_hmac("sha256", secreto.encode(), sal.encode(), int(iteraciones))
    return hmac.compare_digest(dk.hex(), esperado)


def sha256(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()


def nuevo_token_cliente() -> tuple[str, str]:
    """Devuelve (token en claro para el enlace, hash que se guarda)."""
    token = secrets.token_urlsafe(32)
    return token, sha256(token)


def nuevo_codigo_2fa() -> str:
    """RN-02: código numérico de 6 dígitos."""
    return f"{secrets.randbelow(10**6):06d}"


# --- Sesiones del personal --------------------------------------------------
def _b64(datos: bytes) -> str:
    return base64.urlsafe_b64encode(datos).rstrip(b"=").decode()


def _firma(carga: str) -> str:
    return _b64(hmac.new(config.SECRET_KEY.encode(), carga.encode(), hashlib.sha256).digest())


def crear_sesion(usuario: Usuario) -> str:
    expira = reloj.ahora() + timedelta(hours=config.SESION_HORAS)
    carga = _b64(json.dumps({"sub": usuario.id_usuario, "rol": usuario.rol.value,
                             "exp": int(expira.timestamp())}).encode())
    return f"{carga}.{_firma(carga)}"


def leer_sesion(token: str) -> dict | None:
    try:
        carga, firma = token.split(".")
    except ValueError:
        return None
    if not hmac.compare_digest(firma, _firma(carga)):
        return None
    datos = json.loads(base64.urlsafe_b64decode(carga + "=" * (-len(carga) % 4)))
    if datos["exp"] < reloj.ahora().timestamp():
        return None
    return datos


_bearer = HTTPBearer(auto_error=False)


def usuario_actual(cred: HTTPAuthorizationCredentials | None = Depends(_bearer),
                   db: Session = Depends(get_db)) -> Usuario:
    datos = leer_sesion(cred.credentials) if cred else None
    usuario = db.get(Usuario, datos["sub"]) if datos else None
    if not usuario or not usuario.activo:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sesión inválida o vencida",
                            headers={"WWW-Authenticate": "Bearer"})
    return usuario


def requiere_rol(*roles: RolUsuario):
    """Control de acceso por rol (OWASP A01). El Gerente no hereda permisos
    operativos: cada endpoint declara explícitamente qué roles lo usan."""
    def dependencia(usuario: Usuario = Depends(usuario_actual)) -> Usuario:
        if usuario.rol not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Tu rol no tiene permiso para esta operación")
        return usuario
    return dependencia
