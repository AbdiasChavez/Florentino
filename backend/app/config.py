"""Configuración leída de variables de entorno (o de backend/.env)."""
import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _cargar_env() -> None:
    archivo = BASE_DIR / ".env"
    if not archivo.exists():
        return
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#") and "=" in linea:
            clave, valor = linea.split("=", 1)
            os.environ.setdefault(clave.strip(), valor.strip())


_cargar_env()

DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{BASE_DIR / 'taller.db'}"
# Sin SECRET_KEY se genera una al arrancar: las sesiones se invalidan al reiniciar.
SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe(48)
PORTAL_URL = os.getenv("PORTAL_URL", "http://localhost:8000/portal")
MEDIA_DIR = Path(os.getenv("MEDIA_DIR", BASE_DIR / "media"))

# Reglas de negocio parametrizables
BAHIAS = 4                      # RN-05
CAPACIDAD_ESTACIONAMIENTO = 5   # RN-05
VIGENCIA_COTIZACION_DIAS = 5    # RN-11
VIGENCIA_CODIGO_MIN = 5         # RN-02
UMBRAL_REAUTORIZACION = 0.10    # RN-04
GARANTIA_DIAS = 30              # RN-13
SESION_HORAS = 8
FOTO_MAX_BYTES = 5 * 1024 * 1024  # R-06: limitar el tamaño de cada foto
