"""Cotización, enlace seguro del cliente y autorización con código 2FA."""
import json
from datetime import timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config, notificaciones, reloj, seguridad
from app.errores import NoEncontradoError, ReglaNegocioError
from app.models import (Autorizacion, Cotizacion, DetalleCotizacion, EstadoAutorizacion,
                        EstadoCotizacion, EstadoOrden, MedioAutorizacion, OrdenServicio,
                        TipoAutorizacion, TipoConcepto, TokenAcceso, Usuario)
from app.servicios import ordenes

EC = EstadoCotizacion


def obtener_cotizacion(db: Session, id_cotizacion: int) -> Cotizacion:
    cot = db.get(Cotizacion, id_cotizacion)
    if not cot:
        raise NoEncontradoError(f"No existe la cotización {id_cotizacion}")
    return actualizar_vencimiento(cot)


def actualizar_vencimiento(cot: Cotizacion) -> Cotizacion:
    """RN-11: una cotización pendiente cuyo plazo pasó queda Vencida."""
    if cot.estado == EC.Pendiente and not cot.esta_vigente():
        cot.estado = EC.Vencida
    return cot


def autorizada_inicial(orden: OrdenServicio) -> Cotizacion | None:
    return next((c for c in orden.cotizaciones if c.estado == EC.Autorizada), None)


def autorizada_vigente(orden: OrdenServicio) -> Cotizacion | None:
    """La versión autorizada más reciente: es la que se cobra."""
    return next((c for c in reversed(orden.cotizaciones) if c.estado == EC.Autorizada), None)


def pendiente(orden: OrdenServicio) -> Cotizacion | None:
    for c in orden.cotizaciones:
        actualizar_vencimiento(c)
    return next((c for c in orden.cotizaciones if c.estado == EC.Pendiente), None)


def crear_cotizacion(db: Session, orden: OrdenServicio, autor: Usuario, detalles: list[dict]) -> Cotizacion:
    """HU-12 (cotización inicial) y HU-16 / RN-04 (re-cotización por trabajos adicionales)."""
    if not detalles:
        raise ReglaNegocioError("La cotización necesita al menos un concepto")
    if orden.estado not in (EstadoOrden.Diagnosticada, EstadoOrden.Autorizada):
        raise ReglaNegocioError("Solo se cotiza una orden diagnosticada o autorizada (re-cotización)")
    if pendiente(orden):
        raise ReglaNegocioError("Ya hay una cotización pendiente y vigente para esta orden")

    anterior = autorizada_vigente(orden) or (orden.cotizaciones[-1] if orden.cotizaciones else None)
    cot = Cotizacion(folio=orden.folio, version=len(orden.cotizaciones) + 1, fecha_emision=reloj.hoy(),
                     vigencia_dias=config.VIGENCIA_COTIZACION_DIAS, estado=EC.Pendiente,
                     id_cotizacion_reemplazada=anterior.id_cotizacion if anterior else None)
    for d in detalles:
        opcional = d.get("opcional", False)
        cot.detalles.append(DetalleCotizacion(concepto=d["concepto"], tipo=TipoConcepto(d["tipo"]),
                                              cantidad=d["cantidad"], precio_unitario=Decimal(str(d["precio_unitario"])),
                                              opcional=opcional, seleccionado=True))
    orden.cotizaciones.append(cot)
    db.flush()

    if orden.estado == EstadoOrden.Autorizada:
        base = autorizada_inicial(orden).total
        if cot.total <= base * (1 + Decimal(str(config.UMBRAL_REAUTORIZACION))):
            # RN-04: un incremento de hasta 10 % no detiene el trabajo.
            cot.estado = EC.Autorizada
            return cot
    enviar_enlace(db, orden)
    return cot


def enviar_enlace(db: Session, orden: OrdenServicio) -> None:
    """HU-02 / RN-01: envía al cliente el enlace seguro. Solo un enlace activo por orden."""
    for t in db.scalars(select(TokenAcceso).where(TokenAcceso.folio == orden.folio, TokenAcceso.activo)):
        t.activo = False
    token, token_hash = seguridad.nuevo_token_cliente()
    cliente = orden.vehiculo.cliente
    db.add(TokenAcceso(token_hash=token_hash, folio=orden.folio, id_cliente=cliente.id_cliente,
                       fecha_emision=reloj.ahora()))
    notificaciones.enviar(cliente.correo, f"Cotización de su vehículo {orden.vehiculo.placas}",
                          f"Revise y autorice su cotización en: {config.PORTAL_URL}/{token}")


def token_valido(db: Session, token: str) -> TokenAcceso:
    acceso = db.get(TokenAcceso, seguridad.sha256(token))
    if not acceso or not acceso.es_valido():
        raise NoEncontradoError("El enlace no es válido o ya expiró")
    return acceso


def seleccionar_opcionales(cot: Cotizacion, seleccion: dict[int, bool]) -> Cotizacion:
    """HU-13 / RN-03: el cliente elige los conceptos opcionales antes de autorizar."""
    _exigir_autorizable(cot)
    por_id = {d.id_detalle: d for d in cot.detalles}
    for id_detalle, elegido in seleccion.items():
        detalle = por_id.get(id_detalle)
        if not detalle:
            raise NoEncontradoError(f"El concepto {id_detalle} no pertenece a la cotización")
        if not detalle.opcional and not elegido:
            raise ReglaNegocioError(f"«{detalle.concepto}» no es opcional", "RN-03")
        detalle.seleccionado = elegido
    _expirar_codigos(cot)  # el monto cambió: un código emitido antes ya no aplica
    return cot


def _exigir_autorizable(cot: Cotizacion) -> None:
    actualizar_vencimiento(cot)
    if cot.estado == EC.Vencida:
        raise ReglaNegocioError("La cotización venció (5 días naturales); el taller debe emitir una nueva", "RN-11")
    if cot.estado != EC.Pendiente:
        raise ReglaNegocioError(f"La cotización ya está {cot.estado.value}")


def _expirar_codigos(cot: Cotizacion) -> None:
    for a in cot.autorizaciones:
        if a.estado == EstadoAutorizacion.Pendiente:
            a.estado = EstadoAutorizacion.Expirada


def solicitar_codigo(db: Session, cot: Cotizacion, medio: MedioAutorizacion, *,
                     token_hash: str | None = None, ip: str | None = None) -> Autorizacion:
    """RN-02: envía al correo del cliente un código de 6 dígitos, de un solo uso, vigente 5 minutos."""
    _exigir_autorizable(cot)
    _expirar_codigos(cot)
    tipo = TipoAutorizacion.Inicial if cot.orden.estado == EstadoOrden.Diagnosticada else TipoAutorizacion.IncrementoMayor10
    codigo = seguridad.nuevo_codigo_2fa()
    aut = Autorizacion(medio=medio, tipo=tipo, monto_aceptado=cot.total, ip=ip, token_hash=token_hash,
                       codigo_verificacion_hash=seguridad.hash_secreto(codigo),
                       estado=EstadoAutorizacion.Pendiente, fecha_hora=reloj.ahora())
    cot.autorizaciones.append(aut)
    cliente = cot.orden.vehiculo.cliente
    notificaciones.enviar(cliente.correo, "Código para autorizar su cotización",
                          f"Su código es {codigo}. Vence en {config.VIGENCIA_CODIGO_MIN} minutos. "
                          f"Monto a autorizar: ${cot.total:,.2f}")
    return aut


def huella(aut: Autorizacion) -> str:
    """RNF-04: huella SHA-256 de lo que el cliente aceptó, para detectar alteraciones."""
    cot = aut.cotizacion
    contenido = {
        "folio": cot.folio, "cotizacion": cot.id_cotizacion, "version": cot.version,
        "conceptos": [[d.concepto, d.cantidad, f"{Decimal(d.precio_unitario):.2f}", d.seleccionado] for d in cot.detalles],
        "monto": f"{Decimal(aut.monto_aceptado):.2f}", "fecha_hora": reloj.utc(aut.fecha_hora).isoformat(),
        "ip": str(aut.ip) if aut.ip else None, "medio": aut.medio.value, "tipo": aut.tipo.value,
    }
    return seguridad.sha256(json.dumps(contenido, sort_keys=True, ensure_ascii=False))


def verificar_huella(aut: Autorizacion) -> bool:
    return aut.huella_sha256 is not None and aut.huella_sha256 == huella(aut)


def confirmar_codigo(db: Session, cot: Cotizacion, codigo: str, *, usuario: Usuario | None = None,
                     ip: str | None = None, token_hash: str | None = None) -> Autorizacion:
    """HU-14 / CU-03 / CU-11: confirma la autorización y la orden pasa a Autorizada."""
    _exigir_autorizable(cot)
    aut = next((a for a in reversed(cot.autorizaciones) if a.estado == EstadoAutorizacion.Pendiente), None)
    if not aut:
        raise ReglaNegocioError("No hay un código vigente; solicita uno nuevo", "RN-02")
    if (token_hash is None) != (aut.medio == MedioAutorizacion.Presencial):
        raise ReglaNegocioError("El código se pidió por otro medio; solicita uno nuevo", "RN-02")
    if reloj.ahora() > reloj.utc(aut.fecha_hora) + timedelta(minutes=config.VIGENCIA_CODIGO_MIN):
        aut.estado = EstadoAutorizacion.Expirada
        raise ReglaNegocioError("El código expiró (5 minutos); solicita uno nuevo", "RN-02")
    if not seguridad.verificar_secreto(codigo, aut.codigo_verificacion_hash):
        raise ReglaNegocioError("Código incorrecto", "RN-02")

    aut.estado = EstadoAutorizacion.Confirmada
    aut.fecha_hora = reloj.ahora()
    if ip:
        aut.ip = ip
    aut.huella_sha256 = huella(aut)
    cot.estado = EC.Autorizada
    if cot.orden.estado == EstadoOrden.Diagnosticada:
        # Si autoriza el cliente desde su enlace, el cambio no tiene usuario interno.
        ordenes.cambiar_estado(db, cot.orden, EstadoOrden.Autorizada, usuario)
    return aut


def rechazar(db: Session, cot: Cotizacion, usuario: Usuario | None = None) -> None:
    """HU-15: el cliente rechaza; una cotización inicial rechazada cancela la orden."""
    _exigir_autorizable(cot)
    _expirar_codigos(cot)
    cot.estado = EC.Rechazada
    if cot.orden.estado == EstadoOrden.Diagnosticada:
        ordenes.cambiar_estado(db, cot.orden, EstadoOrden.Cancelada, usuario)
