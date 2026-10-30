"""Recepción, asignación de bahía, diagnóstico y ciclo de estados de la orden."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import config, reloj
from app.errores import NoEncontradoError, ReglaNegocioError
from app.models import (ESTADOS_ABIERTOS, AsignacionColaborador, Bahia, ChecklistInspeccion, Cita,
                        Diagnostico, EstadoBahia, EstadoCita, EstadoOrden, Fotografia,
                        HistorialEstado, NivelCombustible, OrdenServicio, PosicionFoto,
                        RecepcionVehicular, RolUsuario, Usuario, Vehiculo)

E = EstadoOrden

# Máquina de estados de OrdenServicio (sección 6.5 del documento).
TRANSICIONES: dict[EstadoOrden, set[EstadoOrden]] = {
    E.Abierta: {E.EnEsperaDeBahia, E.Diagnosticada, E.Cancelada},
    E.EnEsperaDeBahia: {E.Abierta, E.Cancelada},
    E.Diagnosticada: {E.Autorizada, E.Cancelada},
    E.Autorizada: {E.ListaParaEntrega},
    E.ListaParaEntrega: {E.Cerrada},
    E.Cerrada: set(),
    E.Cancelada: set(),
}


def obtener_orden(db: Session, folio: str) -> OrdenServicio:
    orden = db.get(OrdenServicio, folio)
    if not orden:
        raise NoEncontradoError(f"No existe la orden {folio}")
    return orden


def cambiar_estado(db: Session, orden: OrdenServicio, nuevo: EstadoOrden, usuario: Usuario | None) -> None:
    """Toda transición pasa por aquí y queda en HistorialEstado (registro inmutable)."""
    if nuevo not in TRANSICIONES[orden.estado]:
        raise ReglaNegocioError(f"La orden {orden.folio} no puede pasar de {orden.estado.value} a {nuevo.value}")
    db.add(HistorialEstado(folio=orden.folio, estado_anterior=orden.estado, estado_nuevo=nuevo,
                           fecha_hora=reloj.ahora(), id_usuario=usuario.id_usuario if usuario else None))
    orden.estado = nuevo
    if nuevo in (E.Cerrada, E.Cancelada):
        liberar_bahia(db, orden)


def bahias_libres(db: Session) -> list[Bahia]:
    return list(db.scalars(select(Bahia).where(Bahia.estado == EstadoBahia.Libre).order_by(Bahia.numero)))


def liberar_bahia(db: Session, orden: OrdenServicio) -> None:
    if orden.numero_bahia:
        db.get(Bahia, orden.numero_bahia).estado = EstadoBahia.Libre


def _siguiente_folio(db: Session) -> str:
    prefijo = f"OS-{reloj.hoy().year}-"
    n = db.scalar(select(func.count()).select_from(OrdenServicio).where(OrdenServicio.folio.like(prefijo + "%")))
    return f"{prefijo}{n + 1:04d}"


def abrir_orden(db: Session, recepcionista: Usuario, *, kilometraje: int, nivel_combustible: NivelCombustible,
                id_vehiculo: int | None = None, id_cita: int | None = None,
                checklist: dict | None = None) -> tuple[OrdenServicio, bool]:
    """CU-02 / HU-01: registra la recepción y abre la orden en estado Abierta.

    Devuelve (orden, sin_bahias). Si las 4 bahías están ocupadas, la orden
    queda EnEsperaDeBahia y se avisa a la recepcionista (HU-07, RN-05).
    """
    cita = None
    if id_cita is not None:
        cita = db.get(Cita, id_cita)
        if not cita:
            raise NoEncontradoError(f"No existe la cita {id_cita}")
        if cita.estado != EstadoCita.Confirmada:
            raise ReglaNegocioError("Solo una cita Confirmada puede convertirse en recepción", "RN-08")
        if id_vehiculo is not None and id_vehiculo != cita.id_vehiculo:
            raise ReglaNegocioError("El vehículo no corresponde al de la cita")
        id_vehiculo = cita.id_vehiculo
    if id_vehiculo is None or not db.get(Vehiculo, id_vehiculo):
        raise NoEncontradoError("Indica un vehículo registrado o una cita confirmada")
    if kilometraje < 0:
        raise ReglaNegocioError("El kilometraje no puede ser negativo")
    if db.scalar(select(OrdenServicio).where(OrdenServicio.id_vehiculo == id_vehiculo,
                                             OrdenServicio.estado.in_(ESTADOS_ABIERTOS))):
        raise ReglaNegocioError("El vehículo ya tiene una orden abierta")

    sin_bahias = not bahias_libres(db)
    if sin_bahias:
        en_espera = db.scalar(select(func.count()).select_from(OrdenServicio).where(
            OrdenServicio.estado.in_(ESTADOS_ABIERTOS), OrdenServicio.numero_bahia.is_(None)))
        if en_espera >= config.CAPACIDAD_ESTACIONAMIENTO:
            raise ReglaNegocioError("No hay bahías libres y el estacionamiento está lleno (5 vehículos)", "RN-05")

    ahora = reloj.ahora()
    orden = OrdenServicio(folio=_siguiente_folio(db), fecha_apertura=ahora, estado=E.Abierta,
                          id_vehiculo=id_vehiculo, id_usuario_abre=recepcionista.id_usuario)
    db.add(orden)
    db.add(HistorialEstado(folio=orden.folio, estado_anterior=None, estado_nuevo=E.Abierta,
                           fecha_hora=ahora, id_usuario=recepcionista.id_usuario))
    recepcion = RecepcionVehicular(folio=orden.folio, id_cita=id_cita, fecha_hora=ahora,
                                   kilometraje=kilometraje, nivel_combustible=nivel_combustible)
    recepcion.checklist = ChecklistInspeccion(**(checklist or {}))
    db.add(recepcion)
    db.flush()
    if sin_bahias:
        cambiar_estado(db, orden, E.EnEsperaDeBahia, recepcionista)
    return orden, sin_bahias


def actualizar_checklist(db: Session, orden: OrdenServicio, datos: dict) -> ChecklistInspeccion:
    if orden.estado not in (E.Abierta, E.EnEsperaDeBahia):
        raise ReglaNegocioError("El checklist solo se modifica durante la recepción")
    checklist = orden.recepcion.checklist
    for campo, valor in datos.items():
        setattr(checklist, campo, valor)
    return checklist


def agregar_fotografia(db: Session, orden: OrdenServicio, posicion: PosicionFoto, archivo: str) -> Fotografia:
    if orden.estado not in (E.Abierta, E.EnEsperaDeBahia):
        raise ReglaNegocioError("Las fotografías de recepción se agregan antes del diagnóstico")
    recepcion = orden.recepcion
    if posicion != PosicionFoto.Otra and any(f.posicion == posicion for f in recepcion.fotografias):
        raise ReglaNegocioError(f"Ya existe la fotografía {posicion.value}; solo una por posición", "RN-12")
    foto = Fotografia(posicion=posicion, archivo=archivo, fecha_hora=reloj.ahora())
    recepcion.fotografias.append(foto)
    return foto


def asignar(db: Session, orden: OrdenServicio, jefe: Usuario, *, numero_bahia: int,
            id_responsable: int, colaboradores: list[int] | None = None) -> None:
    """HU-08 / RN-05 / RN-09: una bahía libre y un mecánico responsable."""
    if orden.estado not in (E.Abierta, E.EnEsperaDeBahia):
        raise ReglaNegocioError("Solo se asigna bahía a órdenes abiertas o en espera de bahía")
    bahia = db.get(Bahia, numero_bahia)
    if not bahia:
        raise NoEncontradoError(f"No existe la bahía {numero_bahia} (el taller tiene 4)")
    if bahia.estado == EstadoBahia.Ocupada and orden.numero_bahia != numero_bahia:
        raise ReglaNegocioError(f"La bahía {numero_bahia} está ocupada", "RN-05")
    responsable = db.get(Usuario, id_responsable)
    if not responsable or not responsable.activo or responsable.rol not in (RolUsuario.Mecanico, RolUsuario.JefeMecanicos):
        raise ReglaNegocioError("El responsable debe ser un mecánico activo", "RN-09")

    liberar_bahia(db, orden)
    bahia.estado = EstadoBahia.Ocupada
    orden.numero_bahia = numero_bahia
    orden.id_usuario_responsable = id_responsable
    orden.colaboradores = [AsignacionColaborador(id_usuario=i, fecha_asignacion=reloj.ahora())
                           for i in dict.fromkeys(colaboradores or []) if i != id_responsable]
    if orden.estado == E.EnEsperaDeBahia:
        cambiar_estado(db, orden, E.Abierta, jefe)


def registrar_diagnostico(db: Session, orden: OrdenServicio, jefe: Usuario, descripcion: str) -> Diagnostico:
    """HU-09: el diagnóstico es un registro histórico; uno nuevo se agrega, no reemplaza."""
    if orden.estado not in (E.Abierta, E.Diagnosticada, E.Autorizada):
        raise ReglaNegocioError(f"No se puede diagnosticar una orden en estado {orden.estado.value}")
    if not orden.recepcion.esta_completa():
        raise ReglaNegocioError("La recepción está incompleta: faltan el checklist o las 4 fotografías", "RN-12")
    if not orden.numero_bahia or not orden.id_usuario_responsable:
        raise ReglaNegocioError("Asigna bahía y mecánico responsable antes del diagnóstico", "RN-09")
    diagnostico = Diagnostico(folio=orden.folio, id_usuario=jefe.id_usuario,
                              fecha_hora=reloj.ahora(), descripcion=descripcion)
    db.add(diagnostico)
    if orden.estado == E.Abierta:
        cambiar_estado(db, orden, E.Diagnosticada, jefe)
    return diagnostico


def cancelar(db: Session, orden: OrdenServicio, usuario: Usuario) -> None:
    cambiar_estado(db, orden, E.Cancelada, usuario)
