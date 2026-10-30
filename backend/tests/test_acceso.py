"""Autenticación y control de acceso por rol (RF-01, HU-27; OWASP A01)."""
from app.models import RolUsuario as R
from tests.conftest import enlace_cliente


def test_cpa26_sin_sesion_no_hay_acceso(cliente_http, datos):
    assert cliente_http.get("/ordenes").status_code == 401
    assert cliente_http.get("/ordenes", headers={"Authorization": "Bearer token.falso"}).status_code == 401


def test_cpa27_credenciales_incorrectas(cliente_http, datos):
    r = cliente_http.post("/auth/login", json={"correo": "gerente@taller.test", "contrasena": "otra-contrasena"})
    assert r.status_code == 401
    # El mecánico de bahía no opera el sistema: no tiene contraseña.
    r = cliente_http.post("/auth/login", json={"correo": "mecanico@taller.test", "contrasena": ""})
    assert r.status_code == 401


def test_cpa28_cada_rol_solo_hace_lo_suyo(flujo, cliente_http, h):
    folio = flujo.abrir()
    cuerpo = {"numero_bahia": 1, "id_responsable": flujo.datos["ids"][R.Mecanico]}
    assert cliente_http.post(f"/ordenes/{folio}/asignacion", headers=h[R.Recepcionista], json=cuerpo).status_code == 403
    assert cliente_http.post(f"/ordenes/{folio}/cancelar", headers=h[R.JefeMecanicos]).status_code == 403
    assert cliente_http.get("/panel", headers=h[R.Recepcionista]).status_code == 403
    assert cliente_http.get("/ordenes", headers=h[R.EncargadoAlmacen]).status_code == 403
    assert cliente_http.post("/usuarios", headers=h[R.Recepcionista], json={
        "nombre": "Intruso", "correo": "x@taller.test", "rol": "Gerente", "contrasena": "x" * 12}).status_code == 403


def test_cpa29_gerente_da_de_alta_personal(cliente_http, h):
    r = cliente_http.post("/usuarios", headers=h[R.Gerente], json={
        "nombre": "Nueva Recepcionista", "correo": "Nueva@Taller.test", "rol": "Recepcionista", "contrasena": "clave-segura-123"})
    assert r.status_code == 201 and r.json()["correo"] == "nueva@taller.test"
    r = cliente_http.post("/auth/login", json={"correo": "nueva@taller.test", "contrasena": "clave-segura-123"})
    assert r.status_code == 200 and r.json()["rol"] == "Recepcionista"


def test_cpa30_enlace_del_cliente_solo_abre_su_orden(flujo, cliente_http):
    folio = flujo.hasta_diagnostico()
    flujo.cotizar(folio)
    token = enlace_cliente()
    r = cliente_http.get(f"/portal/{token}")
    assert r.status_code == 200 and r.json()["folio"] == folio
    assert cliente_http.get(f"/portal/{token[:-1]}x").status_code == 404
    assert cliente_http.get("/portal/OS-2026-0001").status_code == 404  # adivinar el folio no sirve
