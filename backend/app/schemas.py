"""Esquemas de entrada y salida de la API (validación con Pydantic)."""
from datetime import date, datetime, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import (EstadoCita, EstadoCotizacion, EstadoOrden, MedioAutorizacion, NivelCombustible,
                        PosicionFoto, RolUsuario, TipoConcepto, TipoVehiculo)


class Esquema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- Autenticación y usuarios --------------------------------------------
class Login(BaseModel):
    correo: str
    contrasena: str


class Sesion(BaseModel):
    token: str
    rol: RolUsuario
    nombre: str


class UsuarioNuevo(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    correo: str = Field(max_length=160)
    rol: RolUsuario
    contrasena: str | None = Field(default=None, min_length=10)


class UsuarioSalida(Esquema):
    id_usuario: int
    nombre: str
    correo: str
    rol: RolUsuario
    activo: bool


# --- Clientes y vehículos --------------------------------------------------
class VehiculoNuevo(BaseModel):
    placas: str = Field(min_length=3, max_length=15)
    marca: str
    modelo: str
    anio: int = Field(ge=1900, le=2100)
    vin: str | None = Field(default=None, max_length=17)
    tipo: TipoVehiculo


class ClienteNuevo(BaseModel):
    tipo_cliente: str = Field(pattern="^(Particular|Flotilla)$")
    nombre: str = Field(min_length=2, description="Nombre (particular) o razón social (flotilla)")
    telefono: str = Field(min_length=7, max_length=20)
    correo: str = Field(max_length=160)
    credito_habilitado: bool = False
    vehiculos: list[VehiculoNuevo] = []


class VehiculoSalida(Esquema):
    id_vehiculo: int
    id_cliente: int
    placas: str
    marca: str
    modelo: str
    anio: int
    vin: str | None
    tipo: TipoVehiculo


class ClienteSalida(Esquema):
    id_cliente: int
    tipo_cliente: str
    nombre: str
    telefono: str
    correo: str
    vehiculos: list[VehiculoSalida] = []


# --- Citas -------------------------------------------------------------------
class SolicitudCita(BaseModel):
    nombre: str = Field(min_length=2)
    telefono: str = Field(min_length=7, max_length=20)
    correo: str
    placas: str
    marca: str
    modelo: str
    anio: int = Field(ge=1900, le=2100)
    tipo: TipoVehiculo
    fecha: date
    hora: time
    acepta_aviso: bool


class ConfirmarCita(BaseModel):
    numero_bahia: int = Field(ge=1, le=4)


class CitaSalida(Esquema):
    id_cita: int
    id_cliente: int
    id_vehiculo: int
    fecha: date
    hora: time
    estado: EstadoCita
    numero_bahia: int | None


# --- Órdenes -----------------------------------------------------------------
class Checklist(BaseModel):
    carroceria: str | None = None
    interiores: str | None = None
    observaciones: str | None = None
    completo: bool = False


class Recepcion(BaseModel):
    id_vehiculo: int | None = None
    id_cita: int | None = None
    kilometraje: int = Field(ge=0)
    nivel_combustible: NivelCombustible
    checklist: Checklist = Checklist()


class Asignacion(BaseModel):
    numero_bahia: int = Field(ge=1, le=4)
    id_responsable: int
    colaboradores: list[int] = []


class DiagnosticoNuevo(BaseModel):
    descripcion: str = Field(min_length=5)


class FotoSalida(Esquema):
    id_foto: int
    posicion: PosicionFoto
    fecha_hora: datetime


class DiagnosticoSalida(Esquema):
    id_diagnostico: int
    id_usuario: int
    fecha_hora: datetime
    descripcion: str


class HistorialSalida(Esquema):
    estado_anterior: EstadoOrden | None
    estado_nuevo: EstadoOrden
    fecha_hora: datetime
    id_usuario: int | None


class OrdenResumen(BaseModel):
    folio: str
    estado: EstadoOrden
    placas: str
    vehiculo: str
    cliente: str
    numero_bahia: int | None
    responsable: str | None
    fecha_apertura: datetime
    dias_estancia: int


class OrdenDetalle(OrdenResumen):
    kilometraje: int
    nivel_combustible: NivelCombustible
    checklist: Checklist
    fotografias: list[FotoSalida]
    recepcion_completa: bool
    diagnosticos: list[DiagnosticoSalida]
    historial: list[HistorialSalida]
    total_autorizado: Decimal
    saldo_pendiente: Decimal
    entrega_a_credito: bool


class OrdenAbierta(BaseModel):
    orden: OrdenDetalle
    alerta_sin_bahias: bool


# --- Cotizaciones ----------------------------------------------------------
class ConceptoNuevo(BaseModel):
    concepto: str = Field(min_length=2, max_length=200)
    tipo: TipoConcepto
    cantidad: int = Field(gt=0)
    precio_unitario: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    opcional: bool = False


class CotizacionNueva(BaseModel):
    detalles: list[ConceptoNuevo] = Field(min_length=1)


class ConceptoSalida(Esquema):
    id_detalle: int
    concepto: str
    tipo: TipoConcepto
    cantidad: int
    precio_unitario: Decimal
    opcional: bool
    seleccionado: bool
    subtotal: Decimal


class CotizacionSalida(Esquema):
    id_cotizacion: int
    folio: str
    version: int
    fecha_emision: date
    fecha_vencimiento: date
    estado: EstadoCotizacion
    total: Decimal
    detalles: list[ConceptoSalida]


class Seleccion(BaseModel):
    seleccion: dict[int, bool] = Field(description="id_detalle -> seleccionado (solo opcionales)")


class CodigoPresencial(BaseModel):
    codigo: str = Field(pattern=r"^\d{6}$")


class AutorizacionSalida(Esquema):
    id_autorizacion: int
    medio: MedioAutorizacion
    estado: str
    monto_aceptado: Decimal
    fecha_hora: datetime


# --- Cobro -------------------------------------------------------------------
class PagoNuevo(BaseModel):
    monto: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    metodo: str = Field(min_length=3, max_length=30)


class Saldo(BaseModel):
    folio: str
    total_autorizado: Decimal
    total_pagado: Decimal
    saldo_pendiente: Decimal
    entrega_a_credito: bool


# --- Portal del cliente -----------------------------------------------------
class PortalEstado(BaseModel):
    folio: str
    vehiculo: str
    placas: str
    estado: EstadoOrden
    historial: list[HistorialSalida]
    cotizacion: CotizacionSalida | None
    saldo_pendiente: Decimal


# --- Panel -------------------------------------------------------------------
class BahiaSalida(BaseModel):
    numero: int
    estado: str
    folio: str | None
    placas: str | None


class Panel(BaseModel):
    bahias: list[BahiaSalida]
    ordenes_por_estado: dict[str, int]
    en_estacionamiento: int
    ingresos_acumulados: Decimal
