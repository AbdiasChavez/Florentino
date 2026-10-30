"""Autenticación, usuarios, clientes, vehículos y citas."""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app import schemas, seguridad
from app.db import get_db
from app.models import (Cita, Cliente, ClienteParticular, EstadoCita, Flotilla, OrdenServicio, RolUsuario,
                        Usuario, Vehiculo)
from app.rutas.serializar import resumen_orden
from app.seguridad import requiere_rol
from app.servicios import citas

R = RolUsuario
router = APIRouter()


# --- Autenticación (RF-01) ---------------------------------------------------
@router.post("/auth/login", response_model=schemas.Sesion, tags=["Autenticación"])
def login(datos: schemas.Login, db: Session = Depends(get_db)):
    usuario = db.scalar(select(Usuario).where(Usuario.correo == datos.correo.strip().lower()))
    if not usuario or not usuario.activo or not seguridad.verificar_secreto(datos.contrasena, usuario.contrasena_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Correo o contraseña incorrectos")
    return schemas.Sesion(token=seguridad.crear_sesion(usuario), rol=usuario.rol, nombre=usuario.nombre)


@router.get("/auth/yo", response_model=schemas.UsuarioSalida, tags=["Autenticación"])
def yo(usuario: Usuario = Depends(seguridad.usuario_actual)):
    return usuario


# --- Usuarios (HU-27) ----------------------------------------------------------
@router.post("/usuarios", response_model=schemas.UsuarioSalida, status_code=201, tags=["Usuarios"])
def crear_usuario(datos: schemas.UsuarioNuevo, db: Session = Depends(get_db),
                  _: Usuario = Depends(requiere_rol(R.Gerente))):
    correo = datos.correo.strip().lower()
    if db.scalar(select(Usuario).where(Usuario.correo == correo)):
        raise HTTPException(409, "Ya existe un usuario con ese correo")
    if datos.rol != R.Mecanico and not datos.contrasena:
        raise HTTPException(422, "El personal que opera el sistema necesita contraseña")
    usuario = Usuario(nombre=datos.nombre, correo=correo, rol=datos.rol, activo=True,
                      contrasena_hash=seguridad.hash_secreto(datos.contrasena) if datos.contrasena else None)
    db.add(usuario)
    db.commit()
    return usuario


@router.get("/usuarios", response_model=list[schemas.UsuarioSalida], tags=["Usuarios"])
def listar_usuarios(rol: RolUsuario | None = None, db: Session = Depends(get_db),
                    _: Usuario = Depends(requiere_rol(R.Gerente, R.JefeMecanicos))):
    consulta = select(Usuario).order_by(Usuario.nombre)
    if rol:
        consulta = consulta.where(Usuario.rol == rol)
    return db.scalars(consulta).all()


# --- Clientes y vehículos (RF-03.1, HU-05) ------------------------------------
def _cliente_salida(c: Cliente) -> schemas.ClienteSalida:
    return schemas.ClienteSalida(id_cliente=c.id_cliente, tipo_cliente=c.tipo_cliente, nombre=c.nombre,
                                 telefono=c.telefono, correo=c.correo,
                                 vehiculos=[schemas.VehiculoSalida.model_validate(v) for v in c.vehiculos])


@router.post("/clientes", response_model=schemas.ClienteSalida, status_code=201, tags=["Clientes"])
def crear_cliente(datos: schemas.ClienteNuevo, db: Session = Depends(get_db),
                  _: Usuario = Depends(requiere_rol(R.Recepcionista, R.Gerente))):
    cliente = Cliente(tipo_cliente=datos.tipo_cliente, telefono=datos.telefono, correo=datos.correo.strip())
    # {disjoint, complete}: el cliente se crea junto con su subclase.
    if datos.tipo_cliente == "Particular":
        cliente.particular = ClienteParticular(nombre=datos.nombre)
    else:
        cliente.flotilla = Flotilla(razon_social=datos.nombre, credito_habilitado=datos.credito_habilitado)
    for v in datos.vehiculos:
        if db.scalar(select(Vehiculo).where(Vehiculo.placas == v.placas.upper())):
            raise HTTPException(409, f"Las placas {v.placas} ya están registradas")
        cliente.vehiculos.append(Vehiculo(**v.model_dump() | {"placas": v.placas.upper()}))
    db.add(cliente)
    db.commit()
    return _cliente_salida(cliente)


@router.get("/clientes", response_model=list[schemas.ClienteSalida], tags=["Clientes"])
def buscar_clientes(q: str, db: Session = Depends(get_db),
                    _: Usuario = Depends(requiere_rol(R.Recepcionista, R.Gerente))):
    """Busca por teléfono o por placas (HU-05)."""
    texto = q.strip()
    ids = db.scalars(select(Cliente.id_cliente).outerjoin(Vehiculo).where(
        or_(Cliente.telefono == texto, Vehiculo.placas == texto.upper()))).unique().all()
    return [_cliente_salida(db.get(Cliente, i)) for i in ids]


@router.post("/clientes/{id_cliente}/vehiculos", response_model=schemas.VehiculoSalida, status_code=201, tags=["Clientes"])
def agregar_vehiculo(id_cliente: int, datos: schemas.VehiculoNuevo, db: Session = Depends(get_db),
                     _: Usuario = Depends(requiere_rol(R.Recepcionista, R.Gerente))):
    if not db.get(Cliente, id_cliente):
        raise HTTPException(404, "No existe el cliente")
    if db.scalar(select(Vehiculo).where(Vehiculo.placas == datos.placas.upper())):
        raise HTTPException(409, "Las placas ya están registradas")
    vehiculo = Vehiculo(id_cliente=id_cliente, **datos.model_dump() | {"placas": datos.placas.upper()})
    db.add(vehiculo)
    db.commit()
    return vehiculo


@router.get("/vehiculos/{id_vehiculo}/historial", response_model=list[schemas.OrdenResumen], tags=["Clientes"])
def historial_vehiculo(id_vehiculo: int, db: Session = Depends(get_db),
                       _: Usuario = Depends(requiere_rol(R.Recepcionista, R.Gerente, R.JefeMecanicos))):
    """RF-03.2: historial de servicios del vehículo."""
    ordenes = db.scalars(select(OrdenServicio).where(OrdenServicio.id_vehiculo == id_vehiculo)
                         .order_by(OrdenServicio.fecha_apertura.desc())).all()
    return [resumen_orden(o) for o in ordenes]


# --- Citas (RF-09) -----------------------------------------------------------
@router.post("/citas/solicitudes", response_model=schemas.CitaSalida, status_code=201, tags=["Citas"])
def solicitar_cita(datos: schemas.SolicitudCita, db: Session = Depends(get_db)):
    """Público: el cliente solicita una cita; queda Pendiente (RN-08)."""
    cita = citas.solicitar(db, **datos.model_dump())
    db.commit()
    return cita


@router.get("/citas", response_model=list[schemas.CitaSalida], tags=["Citas"])
def agenda(fecha: date | None = None, estado: EstadoCita | None = None, db: Session = Depends(get_db),
           _: Usuario = Depends(requiere_rol(R.Recepcionista, R.Gerente))):
    """HU-04: agenda por día (y por bahía en la respuesta)."""
    consulta = select(Cita).order_by(Cita.fecha, Cita.hora, Cita.numero_bahia)
    if fecha:
        consulta = consulta.where(Cita.fecha == fecha)
    if estado:
        consulta = consulta.where(Cita.estado == estado)
    return db.scalars(consulta).all()


@router.post("/citas/{id_cita}/confirmar", response_model=schemas.CitaSalida, tags=["Citas"])
def confirmar_cita(id_cita: int, datos: schemas.ConfirmarCita, db: Session = Depends(get_db),
                   usuario: Usuario = Depends(requiere_rol(R.Recepcionista))):
    cita = citas.confirmar(db, id_cita, usuario, datos.numero_bahia)
    db.commit()
    return cita


@router.post("/citas/{id_cita}/cancelar", response_model=schemas.CitaSalida, tags=["Citas"])
def cancelar_cita(id_cita: int, db: Session = Depends(get_db),
                  _: Usuario = Depends(requiere_rol(R.Recepcionista))):
    cita = citas.cancelar(db, id_cita)
    db.commit()
    return cita
