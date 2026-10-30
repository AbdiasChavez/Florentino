"""Envío de enlaces y códigos al cliente.

En la Fase 1 el envío real por correo/SMS queda pendiente (riesgo R-05): los
mensajes se registran en la bitácora y se guardan en BANDEJA para que las
pruebas y la demostración puedan leerlos. Para enviar correos de verdad se
reemplaza `enviar` por una implementación con el proveedor elegido.
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime

from app import reloj

log = logging.getLogger("taller.notificaciones")


@dataclass
class Mensaje:
    destino: str
    asunto: str
    cuerpo: str
    fecha: datetime = field(default_factory=reloj.ahora)


BANDEJA: list[Mensaje] = []


def enviar(destino: str, asunto: str, cuerpo: str) -> None:
    BANDEJA.append(Mensaje(destino, asunto, cuerpo))
    log.info("Notificación a %s: %s", destino, asunto)


def ultimo_mensaje(destino: str) -> Mensaje | None:
    return next((m for m in reversed(BANDEJA) if m.destino == destino), None)
