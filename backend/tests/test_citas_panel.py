"""Citas en línea (RN-08, HU-03, HU-04) y lista de órdenes abiertas / panel (RF-11)."""
from app.models import RolUsuario as R

SOLICITUD = {"nombre": "Cliente Web Ficticio", "telefono": "9713333333", "correo": "web@ejemplo.test",
             "placas": "web-123", "marca": "Chevrolet", "modelo": "Aveo", "anio": 2018, "tipo": "Automovil",
             "fecha": "2026-11-05", "hora": "10:00:00", "acepta_aviso": True}


def test_cpa31_cita_web_queda_pendiente_y_exige_aviso(cliente_http, datos):
    assert cliente_http.post("/citas/solicitudes", json=SOLICITUD | {"acepta_aviso": False}).status_code == 409
    r = cliente_http.post("/citas/solicitudes", json=SOLICITUD)
    assert r.status_code == 201 and r.json()["estado"] == "Pendiente" and r.json()["numero_bahia"] is None


def test_cpa32_confirmacion_manual_sin_choques_de_bahia(cliente_http, h):
    id1 = cliente_http.post("/citas/solicitudes", json=SOLICITUD).json()["id_cita"]
    id2 = cliente_http.post("/citas/solicitudes", json=SOLICITUD | {"placas": "WEB-456"}).json()["id_cita"]
    assert cliente_http.post(f"/citas/{id1}/confirmar", headers=h[R.Recepcionista], json={"numero_bahia": 3}).status_code == 200
    r = cliente_http.post(f"/citas/{id2}/confirmar", headers=h[R.Recepcionista], json={"numero_bahia": 3})
    assert r.status_code == 409
    assert cliente_http.post(f"/citas/{id2}/confirmar", headers=h[R.Recepcionista], json={"numero_bahia": 4}).status_code == 200


def test_cpa33_solo_cita_confirmada_se_convierte_en_recepcion(cliente_http, h):
    id_cita = cliente_http.post("/citas/solicitudes", json=SOLICITUD).json()["id_cita"]
    cuerpo = {"id_cita": id_cita, "kilometraje": 1000, "nivel_combustible": "Lleno"}
    r = cliente_http.post("/ordenes", headers=h[R.Recepcionista], json=cuerpo)
    assert r.status_code == 409 and r.json()["regla"] == "RN-08"
    cliente_http.post(f"/citas/{id_cita}/confirmar", headers=h[R.Recepcionista], json={"numero_bahia": 1})
    assert cliente_http.post("/ordenes", headers=h[R.Recepcionista], json=cuerpo).status_code == 201


def test_cpa34_placas_ajenas_no_se_agendan_con_otros_datos(cliente_http, datos):
    r = cliente_http.post("/citas/solicitudes", json=SOLICITUD | {"placas": "PRB-001"})
    assert r.status_code == 409


def test_cpa35_lista_de_ordenes_abiertas_y_panel(flujo, cliente_http, h):
    folio = flujo.hasta_diagnostico()
    otra = flujo.abrir(flujo.datos["vehiculo_flotilla"])
    cliente_http.post(f"/ordenes/{otra}/cancelar", headers=h[R.Gerente])
    abiertas = cliente_http.get("/ordenes", headers=h[R.Recepcionista]).json()
    assert [o["folio"] for o in abiertas] == [folio]
    assert abiertas[0]["numero_bahia"] == 1 and abiertas[0]["responsable"] == "Mecanico Prueba"
    panel = cliente_http.get("/panel", headers=h[R.Gerente]).json()
    assert panel["ordenes_por_estado"] == {"Diagnosticada": 1}
    assert [b["estado"] for b in panel["bahias"]] == ["Ocupada", "Libre", "Libre", "Libre"]
