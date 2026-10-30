"""Entidades del dominio. Tablas y columnas iguales a db/schema.sql.

Las columnas generadas de PostgreSQL (fecha_vencimiento, fecha_fin) no se
mapean: se calculan como propiedades. Las restricciones que el esquema
implementa con disparadores también se validan en app/servicios, para que la
regla se cumpla igual con SQLite (desarrollo y pruebas).
"""
import enum
from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import (Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric,
                        SmallInteger, String, Text, Time, Uuid)
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import reloj
from app.db import Base


def _enum(cls, nombre):
    return Enum(cls, name=nombre, values_callable=lambda e: [m.value for m in e])


class RolUsuario(str, enum.Enum):
    Gerente = "Gerente"
    Recepcionista = "Recepcionista"
    Mecanico = "Mecanico"
    JefeMecanicos = "JefeMecanicos"
    EncargadoAlmacen = "EncargadoAlmacen"


class TipoVehiculo(str, enum.Enum):
    Automovil = "Automovil"
    Motocicleta = "Motocicleta"
    Camioneta = "Camioneta"


class EstadoCita(str, enum.Enum):
    Pendiente = "Pendiente"
    Confirmada = "Confirmada"
    Cancelada = "Cancelada"


class EstadoBahia(str, enum.Enum):
    Libre = "Libre"
    Ocupada = "Ocupada"


class EstadoOrden(str, enum.Enum):
    Abierta = "Abierta"
    EnEsperaDeBahia = "EnEsperaDeBahia"
    Diagnosticada = "Diagnosticada"
    Autorizada = "Autorizada"
    ListaParaEntrega = "ListaParaEntrega"
    Cerrada = "Cerrada"
    Cancelada = "Cancelada"


ESTADOS_ABIERTOS = [e for e in EstadoOrden if e not in (EstadoOrden.Cerrada, EstadoOrden.Cancelada)]


class NivelCombustible(str, enum.Enum):
    Reserva = "Reserva"
    UnCuarto = "UnCuarto"
    Mitad = "Mitad"
    TresCuartos = "TresCuartos"
    Lleno = "Lleno"


class PosicionFoto(str, enum.Enum):
    Frente = "Frente"
    Trasera = "Trasera"
    Izquierda = "Izquierda"
    Derecha = "Derecha"
    Otra = "Otra"


POSICIONES_OBLIGATORIAS = {PosicionFoto.Frente, PosicionFoto.Trasera, PosicionFoto.Izquierda, PosicionFoto.Derecha}


class Canal(str, enum.Enum):
    Correo = "Correo"
    SMS = "SMS"


class EstadoCotizacion(str, enum.Enum):
    Pendiente = "Pendiente"
    Autorizada = "Autorizada"
    Rechazada = "Rechazada"
    Vencida = "Vencida"


class TipoConcepto(str, enum.Enum):
    ManoDeObra = "ManoDeObra"
    Refaccion = "Refaccion"
    Insumo = "Insumo"


class MedioAutorizacion(str, enum.Enum):
    Remoto = "Remoto"
    Presencial = "Presencial"


class TipoAutorizacion(str, enum.Enum):
    Inicial = "Inicial"
    IncrementoMayor10 = "IncrementoMayor10"


class EstadoAutorizacion(str, enum.Enum):
    Pendiente = "Pendiente"
    Confirmada = "Confirmada"
    Rechazada = "Rechazada"
    Expirada = "Expirada"


# ---------------------------------------------------------------------------
class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    correo: Mapped[str] = mapped_column(String(160), unique=True)
    contrasena_hash: Mapped[str | None] = mapped_column(String(255))
    rol: Mapped[RolUsuario] = mapped_column(_enum(RolUsuario, "rol_usuario"))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)


class Cliente(Base):
    __tablename__ = "cliente"
    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_cliente: Mapped[str] = mapped_column(String(10))
    telefono: Mapped[str] = mapped_column(String(20))
    correo: Mapped[str] = mapped_column(String(160))
    particular: Mapped["ClienteParticular | None"] = relationship(uselist=False, cascade="all, delete-orphan")
    flotilla: Mapped["Flotilla | None"] = relationship(uselist=False, cascade="all, delete-orphan")
    vehiculos: Mapped[list["Vehiculo"]] = relationship(back_populates="cliente")

    @property
    def nombre(self) -> str:
        if self.particular:
            return self.particular.nombre
        return self.flotilla.razon_social if self.flotilla else ""


class ClienteParticular(Base):
    __tablename__ = "cliente_particular"
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente", ondelete="CASCADE"), primary_key=True)
    tipo_cliente: Mapped[str] = mapped_column(String(10), default="Particular")
    nombre: Mapped[str] = mapped_column(String(120))


class Flotilla(Base):
    __tablename__ = "flotilla"
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente", ondelete="CASCADE"), primary_key=True)
    tipo_cliente: Mapped[str] = mapped_column(String(10), default="Flotilla")
    razon_social: Mapped[str] = mapped_column(String(160))
    credito_habilitado: Mapped[bool] = mapped_column(Boolean, default=False)


class Vehiculo(Base):
    __tablename__ = "vehiculo"
    id_vehiculo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente"))
    placas: Mapped[str] = mapped_column(String(15), unique=True)
    marca: Mapped[str] = mapped_column(String(60))
    modelo: Mapped[str] = mapped_column(String(60))
    anio: Mapped[int] = mapped_column(SmallInteger)
    vin: Mapped[str | None] = mapped_column(String(17), unique=True)
    tipo: Mapped[TipoVehiculo] = mapped_column(_enum(TipoVehiculo, "tipo_vehiculo"))
    cliente: Mapped[Cliente] = relationship(back_populates="vehiculos")


class Bahia(Base):
    __tablename__ = "bahia"
    numero: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=False)
    estado: Mapped[EstadoBahia] = mapped_column(_enum(EstadoBahia, "estado_bahia"), default=EstadoBahia.Libre)


class Cita(Base):
    __tablename__ = "cita"
    id_cita: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente"))
    id_vehiculo: Mapped[int] = mapped_column(ForeignKey("vehiculo.id_vehiculo"))
    fecha: Mapped[date] = mapped_column(Date)
    hora: Mapped[object] = mapped_column(Time)
    estado: Mapped[EstadoCita] = mapped_column(_enum(EstadoCita, "estado_cita"), default=EstadoCita.Pendiente)
    numero_bahia: Mapped[int | None] = mapped_column(ForeignKey("bahia.numero"))
    id_usuario_confirma: Mapped[int | None] = mapped_column(ForeignKey("usuario.id_usuario"))
    vehiculo: Mapped[Vehiculo] = relationship()


class OrdenServicio(Base):
    __tablename__ = "orden_servicio"
    folio: Mapped[str] = mapped_column(String(20), primary_key=True)
    fecha_apertura: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=reloj.ahora)
    estado: Mapped[EstadoOrden] = mapped_column(_enum(EstadoOrden, "estado_orden"), default=EstadoOrden.Abierta)
    fecha_entrega: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    entrega_a_credito: Mapped[bool] = mapped_column(Boolean, default=False)
    id_vehiculo: Mapped[int] = mapped_column(ForeignKey("vehiculo.id_vehiculo"))
    id_usuario_abre: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_usuario_responsable: Mapped[int | None] = mapped_column(ForeignKey("usuario.id_usuario"))
    numero_bahia: Mapped[int | None] = mapped_column(ForeignKey("bahia.numero"))
    id_usuario_autoriza_credito: Mapped[int | None] = mapped_column(ForeignKey("usuario.id_usuario"))

    vehiculo: Mapped[Vehiculo] = relationship()
    responsable: Mapped[Usuario | None] = relationship(foreign_keys=[id_usuario_responsable])
    recepcion: Mapped["RecepcionVehicular | None"] = relationship(back_populates="orden", uselist=False)
    cotizaciones: Mapped[list["Cotizacion"]] = relationship(back_populates="orden", order_by="Cotizacion.version")
    diagnosticos: Mapped[list["Diagnostico"]] = relationship(order_by="Diagnostico.fecha_hora")
    historial: Mapped[list["HistorialEstado"]] = relationship(order_by="HistorialEstado.id_historial")
    colaboradores: Mapped[list["AsignacionColaborador"]] = relationship(cascade="all, delete-orphan")


class AsignacionColaborador(Base):
    __tablename__ = "asignacion_colaborador"
    folio: Mapped[str] = mapped_column(ForeignKey("orden_servicio.folio", ondelete="CASCADE"), primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"), primary_key=True)
    fecha_asignacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=reloj.ahora)


class HistorialEstado(Base):
    __tablename__ = "historial_estado"
    id_historial: Mapped[int] = mapped_column(Integer, primary_key=True)
    folio: Mapped[str] = mapped_column(ForeignKey("orden_servicio.folio"))
    estado_anterior: Mapped[EstadoOrden | None] = mapped_column(_enum(EstadoOrden, "estado_orden"))
    estado_nuevo: Mapped[EstadoOrden] = mapped_column(_enum(EstadoOrden, "estado_orden"))
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=reloj.ahora)
    id_usuario: Mapped[int | None] = mapped_column(ForeignKey("usuario.id_usuario"))


class Diagnostico(Base):
    __tablename__ = "diagnostico"
    id_diagnostico: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid_local: Mapped[object | None] = mapped_column(Uuid, unique=True)
    folio: Mapped[str] = mapped_column(ForeignKey("orden_servicio.folio"))
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    descripcion: Mapped[str] = mapped_column(Text)


class RecepcionVehicular(Base):
    __tablename__ = "recepcion_vehicular"
    id_recepcion: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid_local: Mapped[object | None] = mapped_column(Uuid, unique=True)
    folio: Mapped[str] = mapped_column(ForeignKey("orden_servicio.folio", ondelete="CASCADE"), unique=True)
    id_cita: Mapped[int | None] = mapped_column(ForeignKey("cita.id_cita"), unique=True)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    kilometraje: Mapped[int] = mapped_column(Integer)
    nivel_combustible: Mapped[NivelCombustible] = mapped_column(_enum(NivelCombustible, "nivel_combustible"))

    orden: Mapped[OrdenServicio] = relationship(back_populates="recepcion")
    checklist: Mapped["ChecklistInspeccion | None"] = relationship(uselist=False, cascade="all, delete-orphan")
    fotografias: Mapped[list["Fotografia"]] = relationship(cascade="all, delete-orphan")

    def esta_completa(self) -> bool:
        """RN-12: checklist completo y las 4 fotos obligatorias."""
        posiciones = {f.posicion for f in self.fotografias}
        return bool(self.checklist and self.checklist.completo) and POSICIONES_OBLIGATORIAS <= posiciones


class ChecklistInspeccion(Base):
    __tablename__ = "checklist_inspeccion"
    id_checklist: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid_local: Mapped[object | None] = mapped_column(Uuid, unique=True)
    id_recepcion: Mapped[int] = mapped_column(ForeignKey("recepcion_vehicular.id_recepcion", ondelete="CASCADE"), unique=True)
    carroceria: Mapped[str | None] = mapped_column(Text)
    interiores: Mapped[str | None] = mapped_column(Text)
    observaciones: Mapped[str | None] = mapped_column(Text)
    completo: Mapped[bool] = mapped_column(Boolean, default=False)


class Fotografia(Base):
    __tablename__ = "fotografia"
    id_foto: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid_local: Mapped[object | None] = mapped_column(Uuid, unique=True)
    id_recepcion: Mapped[int] = mapped_column(ForeignKey("recepcion_vehicular.id_recepcion", ondelete="CASCADE"))
    archivo: Mapped[str] = mapped_column(String(255))
    posicion: Mapped[PosicionFoto] = mapped_column(_enum(PosicionFoto, "posicion_foto"))
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TokenAcceso(Base):
    __tablename__ = "token_acceso"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    folio: Mapped[str] = mapped_column(ForeignKey("orden_servicio.folio", ondelete="CASCADE"))
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente"))
    canal: Mapped[Canal] = mapped_column(_enum(Canal, "canal"), default=Canal.Correo)
    fecha_emision: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=reloj.ahora)
    fecha_expiracion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    orden: Mapped[OrdenServicio] = relationship()

    def es_valido(self) -> bool:
        if not self.activo:
            return False
        return self.fecha_expiracion is None or reloj.utc(self.fecha_expiracion) > reloj.ahora()


class Cotizacion(Base):
    __tablename__ = "cotizacion"
    id_cotizacion: Mapped[int] = mapped_column(Integer, primary_key=True)
    folio: Mapped[str] = mapped_column(ForeignKey("orden_servicio.folio"))
    version: Mapped[int] = mapped_column(Integer, default=1)
    fecha_emision: Mapped[date] = mapped_column(Date, default=reloj.hoy)
    vigencia_dias: Mapped[int] = mapped_column(Integer, default=5)
    estado: Mapped[EstadoCotizacion] = mapped_column(_enum(EstadoCotizacion, "estado_cotizacion"), default=EstadoCotizacion.Pendiente)
    id_cotizacion_reemplazada: Mapped[int | None] = mapped_column(ForeignKey("cotizacion.id_cotizacion"), unique=True)

    orden: Mapped[OrdenServicio] = relationship(back_populates="cotizaciones")
    detalles: Mapped[list["DetalleCotizacion"]] = relationship(cascade="all, delete-orphan", order_by="DetalleCotizacion.id_detalle")
    autorizaciones: Mapped[list["Autorizacion"]] = relationship(back_populates="cotizacion", order_by="Autorizacion.id_autorizacion")
    pagos: Mapped[list["Pago"]] = relationship()

    @property
    def fecha_vencimiento(self) -> date:
        return self.fecha_emision + timedelta(days=self.vigencia_dias)

    def esta_vigente(self) -> bool:
        """RN-11: vigente hasta el día de vencimiento inclusive."""
        return reloj.hoy() <= self.fecha_vencimiento

    @property
    def total(self) -> Decimal:
        return sum((d.subtotal for d in self.detalles if d.seleccionado), Decimal("0.00"))


class DetalleCotizacion(Base):
    __tablename__ = "detalle_cotizacion"
    id_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cotizacion: Mapped[int] = mapped_column(ForeignKey("cotizacion.id_cotizacion", ondelete="CASCADE"))
    concepto: Mapped[str] = mapped_column(String(200))
    tipo: Mapped[TipoConcepto] = mapped_column(_enum(TipoConcepto, "tipo_concepto"))
    cantidad: Mapped[int] = mapped_column(Integer)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    opcional: Mapped[bool] = mapped_column(Boolean, default=False)
    seleccionado: Mapped[bool] = mapped_column(Boolean, default=True)

    @property
    def subtotal(self) -> Decimal:
        return Decimal(self.cantidad) * Decimal(self.precio_unitario)


class Autorizacion(Base):
    __tablename__ = "autorizacion"
    id_autorizacion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cotizacion: Mapped[int] = mapped_column(ForeignKey("cotizacion.id_cotizacion"))
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=reloj.ahora)
    ip: Mapped[str | None] = mapped_column(String(45).with_variant(INET(), "postgresql"))
    medio: Mapped[MedioAutorizacion] = mapped_column(_enum(MedioAutorizacion, "medio_autorizacion"))
    tipo: Mapped[TipoAutorizacion] = mapped_column(_enum(TipoAutorizacion, "tipo_autorizacion"), default=TipoAutorizacion.Inicial)
    monto_aceptado: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    codigo_verificacion_hash: Mapped[str] = mapped_column(String(255))
    estado: Mapped[EstadoAutorizacion] = mapped_column(_enum(EstadoAutorizacion, "estado_autorizacion"), default=EstadoAutorizacion.Pendiente)
    token_hash: Mapped[str | None] = mapped_column(ForeignKey("token_acceso.token_hash"))
    huella_sha256: Mapped[str | None] = mapped_column(String(64))
    cotizacion: Mapped[Cotizacion] = relationship(back_populates="autorizaciones")


class Pago(Base):
    __tablename__ = "pago"
    id_pago: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cotizacion: Mapped[int] = mapped_column(ForeignKey("cotizacion.id_cotizacion"))
    monto: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=reloj.ahora)
    metodo: Mapped[str] = mapped_column(String(30))


class Garantia(Base):
    __tablename__ = "garantia"
    folio: Mapped[str] = mapped_column(ForeignKey("orden_servicio.folio", ondelete="CASCADE"), primary_key=True)
    fecha_inicio: Mapped[date] = mapped_column(Date)
    duracion_dias: Mapped[int] = mapped_column(Integer, default=30)
    alcance: Mapped[str] = mapped_column(String(20).with_variant(Enum("ManoDeObra", name="alcance_garantia"), "postgresql"), default="ManoDeObra")

    @property
    def fecha_fin(self) -> date:
        return self.fecha_inicio + timedelta(days=self.duracion_dias)

    def esta_vigente(self) -> bool:
        return self.fecha_inicio <= reloj.hoy() <= self.fecha_fin
