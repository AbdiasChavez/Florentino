"""Solicitud de citas en línea y confirmación manual (RN-08)."""
from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import reloj
from app.errores import NoEncontradoError, ReglaNegocioError
from app.models import Bahia, Cita, Cliente, ClienteParticular, EstadoCita, TipoVehiculo, Usuario, Vehiculo


def solicitar(db: Session, *, nombre: str, telefono: str, correo: str, placas: str, marca: str,
              modelo: str, anio: int, tipo: TipoVehiculo, fecha: date, hora: time,
              acepta_aviso: bool) -> Cita:
    """HU-03 / CU-09. La cita entra Pendiente y no aparta lugar (RN-08)."""
    if not acepta_aviso:
        raise ReglaNegocioError("Debes aceptar el aviso de privacidad para enviar tus datos", "LFPDPPP")
    if fecha < reloj.hoy():
        raise ReglaNegocioError("La fecha de la cita ya pasó")
    placas = placas.strip().upper()
    vehiculo = db.scalar(select(Vehiculo).where(Vehiculo.placas == placas))
    if vehiculo:
        cliente = vehiculo.cliente
        # Evita que alguien agende a nombre de otro propietario con solo conocer las placas.
        if cliente.correo.lower() != correo.strip().lower() and cliente.telefono != telefono.strip():
            raise ReglaNegocioError("Las placas ya están registradas con otros datos de contacto; llama al taller")
    else:
        cliente = Cliente(tipo_cliente="Particular", telefono=telefono.strip(), correo=correo.strip())
        cliente.particular = ClienteParticular(nombre=nombre.strip())
        vehiculo = Vehiculo(placas=placas, marca=marca, modelo=modelo, anio=anio, tipo=tipo, cliente=cliente)
        db.add(vehiculo)
        db.flush()
    cita = Cita(id_cliente=cliente.id_cliente, id_vehiculo=vehiculo.id_vehiculo, fecha=fecha, hora=hora,
                estado=EstadoCita.Pendiente)
    db.add(cita)
    db.flush()
    return cita


def confirmar(db: Session, id_cita: int, recepcionista: Usuario, numero_bahia: int) -> Cita:
    """HU-04 / CU-01: una bahía no admite dos citas confirmadas a la misma fecha y hora."""
    cita = db.get(Cita, id_cita)
    if not cita:
        raise NoEncontradoError(f"No existe la cita {id_cita}")
    if cita.estado != EstadoCita.Pendiente:
        raise ReglaNegocioError(f"La cita ya está {cita.estado.value}")
    if not db.get(Bahia, numero_bahia):
        raise NoEncontradoError(f"No existe la bahía {numero_bahia}")
    choque = db.scalar(select(Cita).where(Cita.numero_bahia == numero_bahia, Cita.fecha == cita.fecha,
                                          Cita.hora == cita.hora, Cita.estado == EstadoCita.Confirmada))
    if choque:
        raise ReglaNegocioError(f"La bahía {numero_bahia} ya tiene una cita confirmada a esa hora", "RN-05")
    cita.estado = EstadoCita.Confirmada
    cita.numero_bahia = numero_bahia
    cita.id_usuario_confirma = recepcionista.id_usuario
    return cita


def cancelar(db: Session, id_cita: int) -> Cita:
    cita = db.get(Cita, id_cita)
    if not cita:
        raise NoEncontradoError(f"No existe la cita {id_cita}")
    cita.estado = EstadoCita.Cancelada
    return cita
