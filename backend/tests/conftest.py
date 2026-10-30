"""Fixtures de prueba. Base SQLite en memoria y SOLO datos ficticios (RNF-05)."""
import re
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config, notificaciones, reloj, seguridad
from app.db import Base, crear_motor, get_db
from app.main import app
from app.models import Bahia, Cliente, ClienteParticular, Flotilla, RolUsuario, TipoVehiculo, Usuario, Vehiculo

CONTRASENA = "contrasena-de-prueba"
PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 64


class Reloj:
    """Reloj controlable para probar vigencias (RN-02, RN-11)."""

    def __init__(self):
        self.actual = datetime(2026, 11, 2, 15, 0, tzinfo=timezone.utc)

    def avanzar(self, **kwargs):
        self.actual += timedelta(**kwargs)


@pytest.fixture
def reloj_fijo(monkeypatch):
    r = Reloj()
    monkeypatch.setattr(reloj, "ahora", lambda: r.actual)
    monkeypatch.setattr(reloj, "hoy", lambda: r.actual.date())
    return r


@pytest.fixture
def sesion_db(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "MEDIA_DIR", tmp_path / "media")
    motor = crear_motor("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(motor)
    Sesion = sessionmaker(bind=motor, autoflush=False, expire_on_commit=False)
    with Sesion() as db:
        db.add_all([Bahia(numero=n) for n in range(1, 5)])
        db.commit()
    app.dependency_overrides[get_db] = lambda: (yield from _sesion(Sesion))
    notificaciones.BANDEJA.clear()
    yield Sesion
    app.dependency_overrides.clear()


def _sesion(Sesion):
    db = Sesion()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def cliente_http(sesion_db, reloj_fijo):
    return TestClient(app)


@pytest.fixture
def datos(sesion_db, reloj_fijo):
    """Personal, un cliente particular y una flotilla con crédito (ficticios)."""
    with sesion_db() as db:
        personal = {}
        for rol in RolUsuario:
            u = Usuario(nombre=f"{rol.value} Prueba", correo=f"{rol.value.lower()}@taller.test", rol=rol,
                        contrasena_hash=None if rol == RolUsuario.Mecanico else seguridad.hash_secreto(CONTRASENA))
            db.add(u)
            personal[rol] = u
        part = Cliente(tipo_cliente="Particular", telefono="9711111111", correo="cliente@ejemplo.test")
        part.particular = ClienteParticular(nombre="Cliente Ficticio")
        part.vehiculos.append(Vehiculo(placas="PRB-001", marca="Nissan", modelo="Versa", anio=2019, tipo=TipoVehiculo.Automovil))
        flo = Cliente(tipo_cliente="Flotilla", telefono="9712222222", correo="flotilla@ejemplo.test")
        flo.flotilla = Flotilla(razon_social="Flotilla Ficticia S.A.", credito_habilitado=True)
        flo.vehiculos.append(Vehiculo(placas="FLT-001", marca="Ford", modelo="Ranger", anio=2021, tipo=TipoVehiculo.Camioneta))
        db.add_all([part, flo])
        db.commit()
        return {
            "ids": {rol: u.id_usuario for rol, u in personal.items()},
            "vehiculo": part.vehiculos[0].id_vehiculo,
            "vehiculo_flotilla": flo.vehiculos[0].id_vehiculo,
        }


def encabezado(rol: RolUsuario, cliente: TestClient) -> dict:
    r = cliente.post("/auth/login", json={"correo": f"{rol.value.lower()}@taller.test", "contrasena": CONTRASENA})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['token']}"}


@pytest.fixture
def h(cliente_http, datos):
    """Encabezados de sesión por rol: h[RolUsuario.Recepcionista]."""
    return {rol: encabezado(rol, cliente_http) for rol in RolUsuario if rol != RolUsuario.Mecanico}


# --- Pasos del flujo núcleo, reutilizables ----------------------------------
class Flujo:
    def __init__(self, c: TestClient, h: dict, datos: dict):
        self.c, self.h, self.datos = c, h, datos
        self.R = RolUsuario

    def abrir(self, vehiculo=None, completo=True):
        r = self.c.post("/ordenes", headers=self.h[self.R.Recepcionista], json={
            "id_vehiculo": vehiculo or self.datos["vehiculo"], "kilometraje": 45210, "nivel_combustible": "Mitad",
            "checklist": {"carroceria": "Rayón puerta izquierda", "interiores": "Sin daños", "completo": completo}})
        assert r.status_code == 201, r.text
        return r.json()["orden"]["folio"]

    def fotos(self, folio, posiciones=("Frente", "Trasera", "Izquierda", "Derecha")):
        for p in posiciones:
            r = self.c.post(f"/ordenes/{folio}/fotografias", headers=self.h[self.R.Recepcionista],
                            data={"posicion": p}, files={"archivo": (f"{p}.png", PNG, "image/png")})
            assert r.status_code == 201, r.text

    def asignar(self, folio, bahia=1):
        r = self.c.post(f"/ordenes/{folio}/asignacion", headers=self.h[self.R.JefeMecanicos],
                        json={"numero_bahia": bahia, "id_responsable": self.datos["ids"][self.R.Mecanico]})
        assert r.status_code == 200, r.text

    def diagnosticar(self, folio):
        r = self.c.post(f"/ordenes/{folio}/diagnosticos", headers=self.h[self.R.JefeMecanicos],
                        json={"descripcion": "Balatas delanteras desgastadas al 90 %"})
        assert r.status_code == 201, r.text

    def cotizar(self, folio, conceptos=None):
        conceptos = conceptos or [
            {"concepto": "Cambio de balatas", "tipo": "ManoDeObra", "cantidad": 1, "precio_unitario": "600.00"},
            {"concepto": "Juego de balatas", "tipo": "Refaccion", "cantidad": 1, "precio_unitario": "900.00"},
            {"concepto": "Lavado de motor", "tipo": "ManoDeObra", "cantidad": 1, "precio_unitario": "250.00", "opcional": True},
        ]
        r = self.c.post(f"/ordenes/{folio}/cotizaciones", headers=self.h[self.R.JefeMecanicos], json={"detalles": conceptos})
        assert r.status_code == 201, r.text
        return r.json()

    def hasta_diagnostico(self, vehiculo=None, bahia=1):
        folio = self.abrir(vehiculo)
        self.fotos(folio)
        self.asignar(folio, bahia)
        self.diagnosticar(folio)
        return folio


@pytest.fixture
def flujo(cliente_http, h, datos):
    return Flujo(cliente_http, h, datos)


def enlace_cliente(correo="cliente@ejemplo.test") -> str:
    return re.search(r"/portal/([\w-]+)", notificaciones.ultimo_mensaje(correo).cuerpo).group(1)


def codigo_cliente(correo="cliente@ejemplo.test") -> str:
    return re.search(r"\b(\d{6})\b", notificaciones.ultimo_mensaje(correo).cuerpo).group(1)
