"""Cotización y autorización 2FA (HU-02, HU-12 a HU-16; RN-02, RN-03, RN-04, RN-11; RNF-04)."""
from decimal import Decimal

from app.models import Autorizacion
from app.models import RolUsuario as R
from app.servicios.cotizaciones import verificar_huella
from tests.conftest import codigo_cliente, enlace_cliente


def _autorizar_remoto(c, token):
    assert c.post(f"/portal/{token}/codigo").status_code == 202
    return c.post(f"/portal/{token}/autorizacion", json={"codigo": codigo_cliente()})


def test_cpa10_cotizacion_desglosada_con_vigencia_y_enlace(flujo):
    folio = flujo.hasta_diagnostico()
    cot = flujo.cotizar(folio)
    assert Decimal(cot["total"]) == Decimal("1750.00")
    assert cot["fecha_emision"] == "2026-11-02" and cot["fecha_vencimiento"] == "2026-11-07"
    assert {d["tipo"] for d in cot["detalles"]} == {"ManoDeObra", "Refaccion"}
    assert enlace_cliente()  # HU-02: el cliente recibió su enlace seguro


def test_cpa11_vigencia_limite_cinco_dias_si_seis_no(flujo, cliente_http, reloj_fijo):
    folio = flujo.hasta_diagnostico()
    flujo.cotizar(folio)
    token = enlace_cliente()
    reloj_fijo.avanzar(days=5)
    assert cliente_http.post(f"/portal/{token}/codigo").status_code == 202
    reloj_fijo.avanzar(days=1)
    r = cliente_http.post(f"/portal/{token}/autorizacion", json={"codigo": codigo_cliente()})
    assert r.status_code == 409 and r.json()["regla"] == "RN-11"


def test_cpa12_cliente_elige_opcionales_pero_no_obligatorios(flujo, cliente_http):
    folio = flujo.hasta_diagnostico()
    cot = flujo.cotizar(folio)
    token = enlace_cliente()
    opcional = next(d for d in cot["detalles"] if d["opcional"])
    obligatorio = next(d for d in cot["detalles"] if not d["opcional"])
    r = cliente_http.put(f"/portal/{token}/seleccion", json={"seleccion": {str(opcional["id_detalle"]): False}})
    assert r.status_code == 200 and Decimal(r.json()["total"]) == Decimal("1500.00")
    r = cliente_http.put(f"/portal/{token}/seleccion", json={"seleccion": {str(obligatorio["id_detalle"]): False}})
    assert r.status_code == 409 and r.json()["regla"] == "RN-03"


def test_cpa13_autorizacion_remota_registra_evidencia(flujo, cliente_http, h, sesion_db):
    folio = flujo.hasta_diagnostico()
    flujo.cotizar(folio)
    r = _autorizar_remoto(cliente_http, enlace_cliente())
    assert r.status_code == 200 and r.json()["estado"] == "Confirmada"
    orden = cliente_http.get(f"/ordenes/{folio}", headers=h[R.Recepcionista]).json()
    assert orden["estado"] == "Autorizada"
    assert orden["historial"][-1]["id_usuario"] is None  # el cambio lo originó el cliente
    with sesion_db() as db:
        aut = db.get(Autorizacion, r.json()["id_autorizacion"])
        assert aut.ip and aut.token_hash and verificar_huella(aut)


def test_cpa14_codigo_expira_a_los_cinco_minutos(flujo, cliente_http, reloj_fijo):
    folio = flujo.hasta_diagnostico()
    flujo.cotizar(folio)
    token = enlace_cliente()
    cliente_http.post(f"/portal/{token}/codigo")
    codigo = codigo_cliente()
    reloj_fijo.avanzar(minutes=5, seconds=1)
    r = cliente_http.post(f"/portal/{token}/autorizacion", json={"codigo": codigo})
    assert r.status_code == 409 and r.json()["regla"] == "RN-02"


def test_cpa15_codigo_incorrecto_y_de_un_solo_uso(flujo, cliente_http):
    folio = flujo.hasta_diagnostico()
    flujo.cotizar(folio)
    token = enlace_cliente()
    cliente_http.post(f"/portal/{token}/codigo")
    codigo = codigo_cliente()
    incorrecto = f"{(int(codigo) + 1) % 10**6:06d}"
    assert cliente_http.post(f"/portal/{token}/autorizacion", json={"codigo": incorrecto}).status_code == 409
    assert cliente_http.post(f"/portal/{token}/autorizacion", json={"codigo": codigo}).status_code == 200
    assert cliente_http.post(f"/portal/{token}/autorizacion", json={"codigo": codigo}).status_code == 409


def test_cpa16_autorizacion_presencial_en_mostrador(flujo, cliente_http, h):
    folio = flujo.hasta_diagnostico()
    cot = flujo.cotizar(folio)
    cliente_http.post(f"/cotizaciones/{cot['id_cotizacion']}/codigo", headers=h[R.Recepcionista])
    r = cliente_http.post(f"/cotizaciones/{cot['id_cotizacion']}/autorizacion", headers=h[R.Recepcionista],
                          json={"codigo": codigo_cliente()})
    assert r.status_code == 200 and r.json()["medio"] == "Presencial"


def test_cpa17_rechazo_del_cliente_cancela_la_orden(flujo, cliente_http, h):
    folio = flujo.hasta_diagnostico()
    flujo.cotizar(folio)
    r = cliente_http.post(f"/portal/{enlace_cliente()}/rechazo")
    assert r.status_code == 200 and r.json()["estado"] == "Rechazada"
    assert cliente_http.get(f"/ordenes/{folio}", headers=h[R.Recepcionista]).json()["estado"] == "Cancelada"


def _orden_autorizada(flujo, cliente_http):
    folio = flujo.hasta_diagnostico()
    flujo.cotizar(folio)
    assert _autorizar_remoto(cliente_http, enlace_cliente()).status_code == 200
    return folio


ADICIONAL = {"concepto": "Disco de freno", "tipo": "Refaccion", "cantidad": 1}


def test_cpa18_incremento_mayor_al_10_requiere_nueva_autorizacion(flujo, cliente_http, h):
    folio = _orden_autorizada(flujo, cliente_http)  # total autorizado: 1750.00
    base = [{"concepto": "Cambio de balatas", "tipo": "ManoDeObra", "cantidad": 1, "precio_unitario": "600.00"},
            {"concepto": "Juego de balatas", "tipo": "Refaccion", "cantidad": 1, "precio_unitario": "900.00"},
            {"concepto": "Lavado de motor", "tipo": "ManoDeObra", "cantidad": 1, "precio_unitario": "250.00"}]
    cot = flujo.cotizar(folio, base + [ADICIONAL | {"precio_unitario": "176.00"}])  # +10.06 %
    assert cot["estado"] == "Pendiente"
    r = cliente_http.post(f"/ordenes/{folio}/terminar", headers=h[R.JefeMecanicos])
    assert r.status_code == 409 and r.json()["regla"] == "RN-04"
    assert _autorizar_remoto(cliente_http, enlace_cliente()).status_code == 200
    assert cliente_http.post(f"/ordenes/{folio}/terminar", headers=h[R.JefeMecanicos]).status_code == 200


def test_cpa19_incremento_de_hasta_10_no_detiene_el_trabajo(flujo, cliente_http, h):
    folio = _orden_autorizada(flujo, cliente_http)
    base = [{"concepto": "Cambio de balatas", "tipo": "ManoDeObra", "cantidad": 1, "precio_unitario": "600.00"},
            {"concepto": "Juego de balatas", "tipo": "Refaccion", "cantidad": 1, "precio_unitario": "900.00"},
            {"concepto": "Lavado de motor", "tipo": "ManoDeObra", "cantidad": 1, "precio_unitario": "250.00"}]
    cot = flujo.cotizar(folio, base + [ADICIONAL | {"precio_unitario": "175.00"}])  # exactamente +10 %
    assert cot["estado"] == "Autorizada"
    saldo = cliente_http.get(f"/ordenes/{folio}/saldo", headers=h[R.Recepcionista]).json()
    assert Decimal(saldo["total_autorizado"]) == Decimal("1925.00")


def test_cpa20_alterar_una_autorizacion_se_detecta(flujo, cliente_http, sesion_db):
    folio = flujo.hasta_diagnostico()
    flujo.cotizar(folio)
    id_aut = _autorizar_remoto(cliente_http, enlace_cliente()).json()["id_autorizacion"]
    with sesion_db() as db:
        aut = db.get(Autorizacion, id_aut)
        assert verificar_huella(aut)
        aut.monto_aceptado = Decimal("1.00")  # alguien modifica el registro directamente
        assert not verificar_huella(aut)
