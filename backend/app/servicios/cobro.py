"""Fin del trabajo, pagos, entrega a crédito y entrega del vehículo."""
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config, notificaciones, reloj
from app.errores import ReglaNegocioError
from app.models import EstadoOrden, Garantia, OrdenServicio, Pago, RolUsuario, TokenAcceso, Usuario
from app.servicios import cotizaciones, ordenes


def total_autorizado(orden: OrdenServicio) -> Decimal:
    cot = cotizaciones.autorizada_vigente(orden)
    return cot.total if cot else Decimal("0.00")


def total_pagado(orden: OrdenServicio) -> Decimal:
    return sum((Decimal(p.monto) for c in orden.cotizaciones for p in c.pagos), Decimal("0.00"))


def saldo_pendiente(orden: OrdenServicio) -> Decimal:
    return total_autorizado(orden) - total_pagado(orden)


def terminar_trabajo(db: Session, orden: OrdenServicio, jefe: Usuario) -> None:
    """CU-07 / HU-20. RN-04: no se termina si hay una re-cotización sin autorizar."""
    if cotizaciones.pendiente(orden):
        raise ReglaNegocioError("Hay trabajos adicionales que superan el 10 % sin autorización del cliente", "RN-04")
    ordenes.cambiar_estado(db, orden, EstadoOrden.ListaParaEntrega, jefe)
    notificaciones.enviar("recepcion", f"Orden {orden.folio} lista para entrega",
                          f"El vehículo {orden.vehiculo.placas} está listo. Avise al cliente.")


def registrar_pago(db: Session, orden: OrdenServicio, monto: Decimal, metodo: str) -> Pago:
    """HU-23: el pago se liga a la cotización autorizada vigente."""
    cot = cotizaciones.autorizada_vigente(orden)
    if not cot:
        raise ReglaNegocioError("La orden no tiene una cotización autorizada")
    if monto <= 0:
        raise ReglaNegocioError("El monto debe ser mayor que cero")
    if monto > saldo_pendiente(orden):
        raise ReglaNegocioError(f"El monto excede el saldo pendiente (${saldo_pendiente(orden):,.2f})")
    pago = Pago(monto=monto, metodo=metodo, fecha_hora=reloj.ahora())
    cot.pagos.append(pago)
    return pago


def autorizar_credito(db: Session, orden: OrdenServicio, gerente: Usuario) -> None:
    """HU-22 / RN-10: solo el Gerente y solo para flotillas con crédito habilitado."""
    if gerente.rol != RolUsuario.Gerente:
        raise ReglaNegocioError("Solo el Gerente autoriza entregas a crédito", "RN-10")
    flotilla = orden.vehiculo.cliente.flotilla
    if not flotilla or not flotilla.credito_habilitado:
        raise ReglaNegocioError("Solo las flotillas con crédito habilitado pueden recibir el vehículo a crédito", "RN-10")
    orden.entrega_a_credito = True
    orden.id_usuario_autoriza_credito = gerente.id_usuario


def entregar(db: Session, orden: OrdenServicio, recepcionista: Usuario) -> Garantia:
    """HU-21 / HU-23 / CU-04: entrega, cierre, garantía de 30 días y expiración del enlace."""
    if orden.estado != EstadoOrden.ListaParaEntrega:
        raise ReglaNegocioError("Solo se entrega un vehículo cuya orden está lista para entrega")
    if saldo_pendiente(orden) > 0 and not orden.entrega_a_credito:
        raise ReglaNegocioError(f"La orden tiene saldo pendiente (${saldo_pendiente(orden):,.2f})", "RN-10")
    orden.fecha_entrega = reloj.ahora()
    ordenes.cambiar_estado(db, orden, EstadoOrden.Cerrada, recepcionista)
    garantia = Garantia(folio=orden.folio, fecha_inicio=reloj.hoy(), duracion_dias=config.GARANTIA_DIAS)
    db.add(garantia)
    # RN-01: el enlace del cliente expira al entregar y saldar.
    if saldo_pendiente(orden) <= 0:
        for t in db.scalars(select(TokenAcceso).where(TokenAcceso.folio == orden.folio, TokenAcceso.activo)):
            t.activo = False
            t.fecha_expiracion = orden.fecha_entrega
    return garantia
