"""Recepción, fotografías, bahías y diagnóstico (HU-01, HU-07, HU-08, HU-09)."""
from app.models import RolUsuario as R
from tests.conftest import PNG


def test_cpa01_recepcion_abre_orden_abierta(flujo, cliente_http, h):
    folio = flujo.abrir()
    orden = cliente_http.get(f"/ordenes/{folio}", headers=h[R.Recepcionista]).json()
    assert folio.startswith("OS-2026-")
    assert orden["estado"] == "Abierta"
    assert orden["kilometraje"] == 45210 and orden["nivel_combustible"] == "Mitad"
    assert orden["historial"][0]["estado_nuevo"] == "Abierta"


def test_cpa02_diagnostico_bloqueado_sin_cuatro_fotos(flujo, cliente_http, h):
    folio = flujo.abrir()
    flujo.fotos(folio, ("Frente", "Trasera", "Izquierda"))
    flujo.asignar(folio)
    r = cliente_http.post(f"/ordenes/{folio}/diagnosticos", headers=h[R.JefeMecanicos], json={"descripcion": "Revisión de frenos"})
    assert r.status_code == 409 and r.json()["regla"] == "RN-12"
    flujo.fotos(folio, ("Derecha",))
    flujo.diagnosticar(folio)
    assert cliente_http.get(f"/ordenes/{folio}", headers=h[R.JefeMecanicos]).json()["estado"] == "Diagnosticada"


def test_cpa03_checklist_incompleto_bloquea_diagnostico(flujo, cliente_http, h):
    folio = flujo.abrir(completo=False)
    flujo.fotos(folio)
    flujo.asignar(folio)
    r = cliente_http.post(f"/ordenes/{folio}/diagnosticos", headers=h[R.JefeMecanicos], json={"descripcion": "Revisión"})
    assert r.status_code == 409
    cliente_http.put(f"/ordenes/{folio}/checklist", headers=h[R.Recepcionista], json={"carroceria": "Sin daños", "completo": True})
    flujo.diagnosticar(folio)


def test_cpa04_una_foto_por_posicion_y_solo_imagenes(flujo, cliente_http, h):
    folio = flujo.abrir()
    flujo.fotos(folio, ("Frente",))
    r = cliente_http.post(f"/ordenes/{folio}/fotografias", headers=h[R.Recepcionista], data={"posicion": "Frente"},
                          files={"archivo": ("f.png", PNG, "image/png")})
    assert r.status_code == 409
    r = cliente_http.post(f"/ordenes/{folio}/fotografias", headers=h[R.Recepcionista], data={"posicion": "Otra"},
                          files={"archivo": ("virus.exe", b"MZ", "application/octet-stream")})
    assert r.status_code == 415


def _nuevo_vehiculo(cliente_http, h, n):
    r = cliente_http.post("/clientes", headers=h[R.Recepcionista], json={
        "tipo_cliente": "Particular", "nombre": f"Cliente Ficticio {n}", "telefono": f"97100000{n:02d}",
        "correo": f"c{n}@ejemplo.test",
        "vehiculos": [{"placas": f"TST-{n:03d}", "marca": "VW", "modelo": "Jetta", "anio": 2015, "tipo": "Automovil"}]})
    assert r.status_code == 201, r.text
    return r.json()["vehiculos"][0]["id_vehiculo"]


def test_cpa05_sin_bahias_la_orden_queda_en_espera_con_alerta(flujo, cliente_http, h):
    for n in range(1, 5):
        folio = flujo.abrir(_nuevo_vehiculo(cliente_http, h, n))
        flujo.asignar(folio, bahia=n)
    r = cliente_http.post("/ordenes", headers=h[R.Recepcionista], json={
        "id_vehiculo": flujo.datos["vehiculo"], "kilometraje": 100, "nivel_combustible": "Lleno"})
    assert r.status_code == 201
    assert r.json()["alerta_sin_bahias"] is True
    assert r.json()["orden"]["estado"] == "EnEsperaDeBahia"


def test_cpa06_estacionamiento_lleno_rechaza_recepcion(flujo, cliente_http, h):
    for n in range(1, 5):
        flujo.asignar(flujo.abrir(_nuevo_vehiculo(cliente_http, h, n)), bahia=n)
    for n in range(5, 10):  # 5 vehículos en espera: el estacionamiento se llena
        flujo.abrir(_nuevo_vehiculo(cliente_http, h, n))
    r = cliente_http.post("/ordenes", headers=h[R.Recepcionista], json={
        "id_vehiculo": _nuevo_vehiculo(cliente_http, h, 10), "kilometraje": 1, "nivel_combustible": "Lleno"})
    assert r.status_code == 409 and r.json()["regla"] == "RN-05"


def test_cpa07_bahia_ocupada_no_se_asigna_y_se_libera_al_cerrar(flujo, cliente_http, h):
    folio1 = flujo.abrir()
    flujo.asignar(folio1, bahia=2)
    folio2 = flujo.abrir(flujo.datos["vehiculo_flotilla"])
    r = cliente_http.post(f"/ordenes/{folio2}/asignacion", headers=h[R.JefeMecanicos],
                          json={"numero_bahia": 2, "id_responsable": flujo.datos["ids"][R.Mecanico]})
    assert r.status_code == 409
    cliente_http.post(f"/ordenes/{folio1}/cancelar", headers=h[R.Gerente])
    flujo.asignar(folio2, bahia=2)


def test_cpa08_responsable_debe_ser_mecanico(flujo, cliente_http, h):
    folio = flujo.abrir()
    r = cliente_http.post(f"/ordenes/{folio}/asignacion", headers=h[R.JefeMecanicos],
                          json={"numero_bahia": 1, "id_responsable": flujo.datos["ids"][R.Recepcionista]})
    assert r.status_code == 409 and r.json()["regla"] == "RN-09"


def test_cpa09_un_vehiculo_no_tiene_dos_ordenes_abiertas(flujo, cliente_http, h):
    flujo.abrir()
    r = cliente_http.post("/ordenes", headers=h[R.Recepcionista], json={
        "id_vehiculo": flujo.datos["vehiculo"], "kilometraje": 1, "nivel_combustible": "Lleno"})
    assert r.status_code == 409
