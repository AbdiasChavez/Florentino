"""Órdenes de servicio, cotizaciones, cobro, bahías y panel del gerente."""
import uuid
from collections import Counter
from decimal import Decimal

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config, schemas
from app.db import get_db
from app.models import (ESTADOS_ABIERTOS, Bahia, MedioAutorizacion, OrdenServicio, Pago, PosicionFoto,
                        RolUsuario, Usuario)
from app.rutas.serializar import cotizacion, detalle_orden, resumen_orden
from app.seguridad import requiere_rol
from app.servicios import cobro, cotizaciones, ordenes

R = RolUsuario
router = APIRouter()
OPERACION = (R.Recepcionista, R.JefeMecanicos, R.Gerente)
TIPOS_IMAGEN = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}


# --- Recepción y orden (CU-02, HU-01, HU-07) ---------------------------------
@router.post("/ordenes", response_model=schemas.OrdenAbierta, status_code=201, tags=["Órdenes"])
def abrir_orden(datos: schemas.Recepcion, db: Session = Depends(get_db),
                usuario: Usuario = Depends(requiere_rol(R.Recepcionista))):
    orden, sin_bahias = ordenes.abrir_orden(
        db, usuario, kilometraje=datos.kilometraje, nivel_combustible=datos.nivel_combustible,
        id_vehiculo=datos.id_vehiculo, id_cita=datos.id_cita, checklist=datos.checklist.model_dump())
    db.commit()
    return schemas.OrdenAbierta(orden=detalle_orden(orden), alerta_sin_bahias=sin_bahias)


@router.get("/ordenes", response_model=list[schemas.OrdenResumen], tags=["Órdenes"])
def listar_ordenes(abiertas: bool = True, db: Session = Depends(get_db),
                   _: Usuario = Depends(requiere_rol(*OPERACION))):
    """Lista de órdenes abiertas del flujo núcleo (las más antiguas primero)."""
    consulta = select(OrdenServicio).order_by(OrdenServicio.fecha_apertura)
    if abiertas:
        consulta = consulta.where(OrdenServicio.estado.in_(ESTADOS_ABIERTOS))
    return [resumen_orden(o) for o in db.scalars(consulta)]


@router.get("/ordenes/{folio}", response_model=schemas.OrdenDetalle, tags=["Órdenes"])
def ver_orden(folio: str, db: Session = Depends(get_db), _: Usuario = Depends(requiere_rol(*OPERACION))):
    return detalle_orden(ordenes.obtener_orden(db, folio))


@router.put("/ordenes/{folio}/checklist", response_model=schemas.Checklist, tags=["Órdenes"])
def actualizar_checklist(folio: str, datos: schemas.Checklist, db: Session = Depends(get_db),
                         _: Usuario = Depends(requiere_rol(R.Recepcionista))):
    checklist = ordenes.actualizar_checklist(db, ordenes.obtener_orden(db, folio), datos.model_dump())
    db.commit()
    return schemas.Checklist.model_validate(checklist, from_attributes=True)


@router.post("/ordenes/{folio}/fotografias", response_model=schemas.FotoSalida, status_code=201, tags=["Órdenes"])
async def subir_fotografia(folio: str, posicion: PosicionFoto = Form(...), archivo: UploadFile = File(...),
                           db: Session = Depends(get_db),
                           _: Usuario = Depends(requiere_rol(R.Recepcionista, R.JefeMecanicos))):
    extension = TIPOS_IMAGEN.get(archivo.content_type or "")
    if not extension:
        raise HTTPException(415, "Solo se aceptan imágenes JPEG, PNG o WebP")
    contenido = await archivo.read(config.FOTO_MAX_BYTES + 1)
    if len(contenido) > config.FOTO_MAX_BYTES:
        raise HTTPException(413, "La fotografía excede 5 MB")
    orden = ordenes.obtener_orden(db, folio)
    ruta = f"{orden.folio}/{uuid.uuid4().hex}{extension}"
    foto = ordenes.agregar_fotografia(db, orden, posicion, ruta)
    destino = config.MEDIA_DIR / ruta
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(contenido)
    db.commit()
    return foto


@router.post("/ordenes/{folio}/asignacion", response_model=schemas.OrdenDetalle, tags=["Órdenes"])
def asignar(folio: str, datos: schemas.Asignacion, db: Session = Depends(get_db),
            usuario: Usuario = Depends(requiere_rol(R.JefeMecanicos))):
    orden = ordenes.obtener_orden(db, folio)
    ordenes.asignar(db, orden, usuario, numero_bahia=datos.numero_bahia, id_responsable=datos.id_responsable,
                    colaboradores=datos.colaboradores)
    db.commit()
    return detalle_orden(orden)


@router.post("/ordenes/{folio}/diagnosticos", response_model=schemas.DiagnosticoSalida, status_code=201, tags=["Órdenes"])
def diagnosticar(folio: str, datos: schemas.DiagnosticoNuevo, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(requiere_rol(R.JefeMecanicos))):
    diagnostico = ordenes.registrar_diagnostico(db, ordenes.obtener_orden(db, folio), usuario, datos.descripcion)
    db.commit()
    return diagnostico


@router.post("/ordenes/{folio}/terminar", response_model=schemas.OrdenDetalle, tags=["Órdenes"])
def terminar(folio: str, db: Session = Depends(get_db), usuario: Usuario = Depends(requiere_rol(R.JefeMecanicos))):
    orden = ordenes.obtener_orden(db, folio)
    cobro.terminar_trabajo(db, orden, usuario)
    db.commit()
    return detalle_orden(orden)


@router.post("/ordenes/{folio}/cancelar", response_model=schemas.OrdenDetalle, tags=["Órdenes"])
def cancelar(folio: str, db: Session = Depends(get_db), usuario: Usuario = Depends(requiere_rol(R.Gerente))):
    orden = ordenes.obtener_orden(db, folio)
    ordenes.cancelar(db, orden, usuario)
    db.commit()
    return detalle_orden(orden)


# --- Cotizaciones (CU-05, CU-03, HU-12 a HU-16) ------------------------------
@router.post("/ordenes/{folio}/cotizaciones", response_model=schemas.CotizacionSalida, status_code=201, tags=["Cotizaciones"])
def cotizar(folio: str, datos: schemas.CotizacionNueva, db: Session = Depends(get_db),
            usuario: Usuario = Depends(requiere_rol(R.Recepcionista, R.JefeMecanicos))):
    cot = cotizaciones.crear_cotizacion(db, ordenes.obtener_orden(db, folio), usuario,
                                        [d.model_dump() for d in datos.detalles])
    db.commit()
    return cotizacion(cot)


@router.get("/ordenes/{folio}/cotizaciones", response_model=list[schemas.CotizacionSalida], tags=["Cotizaciones"])
def listar_cotizaciones(folio: str, db: Session = Depends(get_db), _: Usuario = Depends(requiere_rol(*OPERACION))):
    orden = ordenes.obtener_orden(db, folio)
    return [cotizacion(cotizaciones.actualizar_vencimiento(c)) for c in orden.cotizaciones]


@router.put("/cotizaciones/{id_cotizacion}/seleccion", response_model=schemas.CotizacionSalida, tags=["Cotizaciones"])
def seleccionar_presencial(id_cotizacion: int, datos: schemas.Seleccion, db: Session = Depends(get_db),
                           _: Usuario = Depends(requiere_rol(R.Recepcionista))):
    cot = cotizaciones.seleccionar_opcionales(cotizaciones.obtener_cotizacion(db, id_cotizacion), datos.seleccion)
    db.commit()
    return cotizacion(cot)


@router.post("/cotizaciones/{id_cotizacion}/codigo", status_code=202, tags=["Cotizaciones"])
def codigo_presencial(id_cotizacion: int, request: Request, db: Session = Depends(get_db),
                      _: Usuario = Depends(requiere_rol(R.Recepcionista))):
    """CU-03: el código llega al correo del cliente, que lo dicta en mostrador."""
    cot = cotizaciones.obtener_cotizacion(db, id_cotizacion)
    cotizaciones.solicitar_codigo(db, cot, MedioAutorizacion.Presencial, ip=request.client.host if request.client else None)
    db.commit()
    return {"detail": "Código enviado al correo registrado del cliente"}


@router.post("/cotizaciones/{id_cotizacion}/autorizacion", response_model=schemas.AutorizacionSalida, tags=["Cotizaciones"])
def autorizar_presencial(id_cotizacion: int, datos: schemas.CodigoPresencial, request: Request,
                         db: Session = Depends(get_db), usuario: Usuario = Depends(requiere_rol(R.Recepcionista))):
    cot = cotizaciones.obtener_cotizacion(db, id_cotizacion)
    aut = cotizaciones.confirmar_codigo(db, cot, datos.codigo, usuario=usuario,
                                        ip=request.client.host if request.client else None)
    db.commit()
    return aut


# --- Cobro y entrega (CU-04, CU-13) -----------------------------------------
def _saldo(o: OrdenServicio) -> schemas.Saldo:
    return schemas.Saldo(folio=o.folio, total_autorizado=cobro.total_autorizado(o), total_pagado=cobro.total_pagado(o),
                         saldo_pendiente=cobro.saldo_pendiente(o), entrega_a_credito=o.entrega_a_credito)


@router.get("/ordenes/{folio}/saldo", response_model=schemas.Saldo, tags=["Cobro"])
def saldo(folio: str, db: Session = Depends(get_db), _: Usuario = Depends(requiere_rol(R.Recepcionista, R.Gerente))):
    return _saldo(ordenes.obtener_orden(db, folio))


@router.post("/ordenes/{folio}/pagos", response_model=schemas.Saldo, status_code=201, tags=["Cobro"])
def pagar(folio: str, datos: schemas.PagoNuevo, db: Session = Depends(get_db),
          _: Usuario = Depends(requiere_rol(R.Recepcionista))):
    orden = ordenes.obtener_orden(db, folio)
    cobro.registrar_pago(db, orden, datos.monto, datos.metodo)
    db.commit()
    return _saldo(orden)


@router.post("/ordenes/{folio}/credito", response_model=schemas.Saldo, tags=["Cobro"])
def credito(folio: str, db: Session = Depends(get_db), usuario: Usuario = Depends(requiere_rol(R.Gerente))):
    orden = ordenes.obtener_orden(db, folio)
    cobro.autorizar_credito(db, orden, usuario)
    db.commit()
    return _saldo(orden)


@router.post("/ordenes/{folio}/entrega", response_model=schemas.OrdenDetalle, tags=["Cobro"])
def entregar(folio: str, db: Session = Depends(get_db), usuario: Usuario = Depends(requiere_rol(R.Recepcionista))):
    orden = ordenes.obtener_orden(db, folio)
    cobro.entregar(db, orden, usuario)
    db.commit()
    return detalle_orden(orden)


# --- Bahías y panel (HU-07, RF-11) -------------------------------------------
def _bahias(db: Session) -> list[schemas.BahiaSalida]:
    activas = {o.numero_bahia: o for o in db.scalars(select(OrdenServicio).where(
        OrdenServicio.estado.in_(ESTADOS_ABIERTOS), OrdenServicio.numero_bahia.is_not(None)))}
    return [schemas.BahiaSalida(numero=b.numero, estado=b.estado.value,
                                folio=activas[b.numero].folio if b.numero in activas else None,
                                placas=activas[b.numero].vehiculo.placas if b.numero in activas else None)
            for b in db.scalars(select(Bahia).order_by(Bahia.numero))]


@router.get("/bahias", response_model=list[schemas.BahiaSalida], tags=["Panel"])
def bahias(db: Session = Depends(get_db), _: Usuario = Depends(requiere_rol(*OPERACION))):
    return _bahias(db)


@router.get("/panel", response_model=schemas.Panel, tags=["Panel"])
def panel(db: Session = Depends(get_db), _: Usuario = Depends(requiere_rol(R.Gerente))):
    abiertas = db.scalars(select(OrdenServicio).where(OrdenServicio.estado.in_(ESTADOS_ABIERTOS))).all()
    ingresos = sum((Decimal(p.monto) for p in db.scalars(select(Pago))), Decimal("0.00"))
    return schemas.Panel(bahias=_bahias(db), ordenes_por_estado=dict(Counter(o.estado.value for o in abiertas)),
                         en_estacionamiento=sum(1 for o in abiertas if o.numero_bahia is None),
                         ingresos_acumulados=ingresos)
