"""Pago, entrega, crédito a flotillas, garantía y expiración del enlace (RN-01, RN-10, RN-13)."""
from app.models import RolUsuario as R
from tests.conftest import codigo_cliente, enlace_cliente


def _lista_para_entrega(flujo, c, h, vehiculo=None, correo="cliente@ejemplo.test"):
    folio = flujo.hasta_diagnostico(vehiculo)
    flujo.cotizar(folio)
    token = enlace_cliente(correo)
    c.post(f"/portal/{token}/codigo")
    assert c.post(f"/portal/{token}/autorizacion", json={"codigo": codigo_cliente(correo)}).status_code == 200
    assert c.post(f"/ordenes/{folio}/terminar", headers=h[R.JefeMecanicos]).status_code == 200
    return folio, token


def test_cpa21_no_se_entrega_con_saldo_pendiente(flujo, cliente_http, h):
    folio, _ = _lista_para_entrega(flujo, cliente_http, h)
    cliente_http.post(f"/ordenes/{folio}/pagos", headers=h[R.Recepcionista], json={"monto": "1000.00", "metodo": "Efectivo"})
    r = cliente_http.post(f"/ordenes/{folio}/entrega", headers=h[R.Recepcionista])
    assert r.status_code == 409 and r.json()["regla"] == "RN-10"


def test_cpa22_pago_total_cierra_orden_da_garantia_y_expira_enlace(flujo, cliente_http, h):
    folio, token = _lista_para_entrega(flujo, cliente_http, h)
    r = cliente_http.post(f"/ordenes/{folio}/pagos", headers=h[R.Recepcionista], json={"monto": "1750.00", "metodo": "Tarjeta"})
    assert r.json()["saldo_pendiente"] == "0.00"
    r = cliente_http.post(f"/ordenes/{folio}/entrega", headers=h[R.Recepcionista])
    assert r.status_code == 200 and r.json()["estado"] == "Cerrada"
    assert cliente_http.get(f"/portal/{token}").status_code == 404  # RN-01
    bahias = cliente_http.get("/bahias", headers=h[R.Recepcionista]).json()
    assert all(b["estado"] == "Libre" for b in bahias)


def test_cpa23_pago_no_excede_el_saldo(flujo, cliente_http, h):
    folio, _ = _lista_para_entrega(flujo, cliente_http, h)
    r = cliente_http.post(f"/ordenes/{folio}/pagos", headers=h[R.Recepcionista], json={"monto": "1750.01", "metodo": "Efectivo"})
    assert r.status_code == 409


def test_cpa24_credito_solo_flotillas_y_solo_gerente(flujo, cliente_http, h):
    folio, _ = _lista_para_entrega(flujo, cliente_http, h)
    assert cliente_http.post(f"/ordenes/{folio}/credito", headers=h[R.Recepcionista]).status_code == 403
    r = cliente_http.post(f"/ordenes/{folio}/credito", headers=h[R.Gerente])
    assert r.status_code == 409 and r.json()["regla"] == "RN-10"  # cliente particular


def test_cpa25_flotilla_con_credito_se_entrega_con_saldo(flujo, cliente_http, h):
    folio, token = _lista_para_entrega(flujo, cliente_http, h, flujo.datos["vehiculo_flotilla"], "flotilla@ejemplo.test")
    assert cliente_http.post(f"/ordenes/{folio}/credito", headers=h[R.Gerente]).status_code == 200
    r = cliente_http.post(f"/ordenes/{folio}/entrega", headers=h[R.Recepcionista])
    assert r.status_code == 200 and r.json()["saldo_pendiente"] == "1750.00"
    # Con saldo pendiente el enlace sigue activo para consultar el adeudo (RN-01).
    assert cliente_http.get(f"/portal/{token}").status_code == 200
