-- =============================================================================
-- Sistema de Órdenes de Servicio y Citas
-- Servicio Automotriz Hermanos Ruiz, S.A. de C.V. · Equipo B
--
-- Esquema de base de datos (PostgreSQL 14 o superior) derivado del
-- Diagrama de Clases UML v4, láminas 1/2 (Operación del taller) y 2/2
-- (Cotización, compras, pagos y garantía).
--
-- Convenciones:
--   * Clases -> tablas en snake_case singular; atributos -> columnas snake_case.
--   * «enumeration» -> tipos ENUM de PostgreSQL con los mismos literales.
--   * Atributos derivados (/total, /saldoPendiente, /fechaFin...) no se
--     almacenan: se calculan en columnas generadas o en vistas.
--   * Las notas {restricción} del diagrama se implementan como CHECK, índices
--     únicos parciales o disparadores; las que dependen del flujo de la
--     aplicación quedan documentadas en comentarios «Validación en la API».
--   * Solo datos ficticios en desarrollo y pruebas (LFPDPPP, RNF-05).
--
-- Uso:  psql -d taller -f db/schema.sql
-- =============================================================================

BEGIN;

-- -----------------------------------------------------------------------------
-- Enumeraciones
-- -----------------------------------------------------------------------------
CREATE TYPE rol_usuario         AS ENUM ('Gerente', 'Recepcionista', 'Mecanico', 'JefeMecanicos', 'EncargadoAlmacen');
CREATE TYPE tipo_vehiculo       AS ENUM ('Automovil', 'Motocicleta', 'Camioneta');
CREATE TYPE estado_cita         AS ENUM ('Pendiente', 'Confirmada', 'Cancelada');
CREATE TYPE estado_bahia        AS ENUM ('Libre', 'Ocupada');
CREATE TYPE estado_orden        AS ENUM ('Abierta', 'EnEsperaDeBahia', 'Diagnosticada', 'Autorizada', 'ListaParaEntrega', 'Cerrada', 'Cancelada');
CREATE TYPE nivel_combustible   AS ENUM ('Reserva', 'UnCuarto', 'Mitad', 'TresCuartos', 'Lleno');
CREATE TYPE posicion_foto       AS ENUM ('Frente', 'Trasera', 'Izquierda', 'Derecha', 'Otra');
CREATE TYPE canal               AS ENUM ('Correo', 'SMS');
CREATE TYPE estado_cotizacion   AS ENUM ('Pendiente', 'Autorizada', 'Rechazada', 'Vencida');
CREATE TYPE tipo_concepto       AS ENUM ('ManoDeObra', 'Refaccion', 'Insumo');
CREATE TYPE medio_autorizacion  AS ENUM ('Remoto', 'Presencial');
CREATE TYPE tipo_autorizacion   AS ENUM ('Inicial', 'IncrementoMayor10');
CREATE TYPE estado_autorizacion AS ENUM ('Pendiente', 'Confirmada', 'Rechazada', 'Expirada');
CREATE TYPE estado_solicitud    AS ENUM ('Solicitada', 'Pedida', 'RecibidaParcial', 'Recibida');
CREATE TYPE alcance_garantia    AS ENUM ('ManoDeObra');

-- -----------------------------------------------------------------------------
-- Usuario (personal interno; el cliente no usa contraseña, accede con TokenAcceso)
-- -----------------------------------------------------------------------------
CREATE TABLE usuario (
    id_usuario      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(120) NOT NULL,
    correo          VARCHAR(160) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255),
    rol             rol_usuario  NOT NULL,
    activo          BOOLEAN      NOT NULL DEFAULT TRUE,
    -- Los mecánicos de bahía no operan el sistema (4.3.1): pueden no tener contraseña.
    CONSTRAINT ck_usuario_contrasena CHECK (contrasena_hash IS NOT NULL OR rol = 'Mecanico')
);

-- -----------------------------------------------------------------------------
-- Cliente {abstract} con especialización {disjoint, complete}:
-- ClienteParticular | Flotilla. Patrón tabla por subclase; la columna
-- tipo_cliente + FK compuesta impide que un cliente esté en ambas subclases.
-- -----------------------------------------------------------------------------
CREATE TABLE cliente (
    id_cliente   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo_cliente VARCHAR(10)  NOT NULL CHECK (tipo_cliente IN ('Particular', 'Flotilla')),
    telefono     VARCHAR(20)  NOT NULL,
    correo       VARCHAR(160) NOT NULL,
    UNIQUE (id_cliente, tipo_cliente)
);

CREATE TABLE cliente_particular (
    id_cliente   INTEGER PRIMARY KEY,
    tipo_cliente VARCHAR(10)  NOT NULL DEFAULT 'Particular' CHECK (tipo_cliente = 'Particular'),
    nombre       VARCHAR(120) NOT NULL,
    FOREIGN KEY (id_cliente, tipo_cliente) REFERENCES cliente (id_cliente, tipo_cliente) ON DELETE CASCADE
);

CREATE TABLE flotilla (
    id_cliente         INTEGER PRIMARY KEY,
    tipo_cliente       VARCHAR(10)  NOT NULL DEFAULT 'Flotilla' CHECK (tipo_cliente = 'Flotilla'),
    razon_social       VARCHAR(160) NOT NULL,
    credito_habilitado BOOLEAN      NOT NULL DEFAULT FALSE,
    FOREIGN KEY (id_cliente, tipo_cliente) REFERENCES cliente (id_cliente, tipo_cliente) ON DELETE CASCADE
);
-- Validación en la API: {complete} — todo cliente se da de alta junto con su
-- fila en cliente_particular o en flotilla, en la misma transacción.

-- -----------------------------------------------------------------------------
-- Vehiculo (Cliente 1 —es propietario de— 0..* Vehiculo)
-- -----------------------------------------------------------------------------
CREATE TABLE vehiculo (
    id_vehiculo INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente  INTEGER       NOT NULL REFERENCES cliente (id_cliente),
    placas      VARCHAR(15)   NOT NULL UNIQUE,
    marca       VARCHAR(60)   NOT NULL,
    modelo      VARCHAR(60)   NOT NULL,
    anio        SMALLINT      NOT NULL CHECK (anio BETWEEN 1900 AND 2100),
    vin         VARCHAR(17)   UNIQUE,                -- opcional (RF-03.1)
    tipo        tipo_vehiculo NOT NULL,              -- solo vehículos ligeros (RN-07)
    UNIQUE (id_vehiculo, id_cliente)                 -- destino de la FK compuesta de cita
);

-- -----------------------------------------------------------------------------
-- Bahia {exactamente 4 bahías (número 1 a 4)}
-- -----------------------------------------------------------------------------
CREATE TABLE bahia (
    numero SMALLINT     PRIMARY KEY CHECK (numero BETWEEN 1 AND 4),
    estado estado_bahia NOT NULL DEFAULT 'Libre'
);

INSERT INTO bahia (numero) VALUES (1), (2), (3), (4);

-- -----------------------------------------------------------------------------
-- Cita
--   Cliente 1 —solicita— 0..*; Vehiculo 1 —se agenda para— 0..*;
--   Bahia 0..1 —se agenda en— 0..*; Usuario 0..1 —confirma— 0..*.
-- -----------------------------------------------------------------------------
CREATE TABLE cita (
    id_cita             INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente          INTEGER     NOT NULL REFERENCES cliente (id_cliente),
    id_vehiculo         INTEGER     NOT NULL,
    fecha               DATE        NOT NULL,
    hora                TIME        NOT NULL,
    estado              estado_cita NOT NULL DEFAULT 'Pendiente',
    numero_bahia        SMALLINT    REFERENCES bahia (numero),
    id_usuario_confirma INTEGER     REFERENCES usuario (id_usuario),
    -- {el Vehiculo de la Cita pertenece al Cliente de la Cita}
    FOREIGN KEY (id_vehiculo, id_cliente) REFERENCES vehiculo (id_vehiculo, id_cliente),
    -- Una cita confirmada tiene bahía y recepcionista que la confirmó (RN-08).
    CONSTRAINT ck_cita_confirmada CHECK (
        estado <> 'Confirmada' OR (numero_bahia IS NOT NULL AND id_usuario_confirma IS NOT NULL))
);

-- {una Bahia no admite dos Cita Confirmada con la misma fecha y hora}
CREATE UNIQUE INDEX ux_cita_bahia_horario
    ON cita (numero_bahia, fecha, hora) WHERE estado = 'Confirmada';

-- -----------------------------------------------------------------------------
-- OrdenServicio
--   Vehiculo 1 —ingresa en— 0..*; Usuario 1 —abre (recepcionista)— 0..*;
--   Usuario 0..1 —es responsable de— 0..*; Bahia 0..1 —aloja— 0..*;
--   Usuario 0..1 —autoriza crédito (gerente)— 0..*.
--   /totalAutorizado y /saldoPendiente: vista v_orden_saldo.
-- -----------------------------------------------------------------------------
CREATE TABLE orden_servicio (
    folio                       VARCHAR(20)  PRIMARY KEY,
    fecha_apertura              TIMESTAMPTZ  NOT NULL DEFAULT now(),
    estado                      estado_orden NOT NULL DEFAULT 'Abierta',
    fecha_entrega               TIMESTAMPTZ,
    entrega_a_credito           BOOLEAN      NOT NULL DEFAULT FALSE,
    id_vehiculo                 INTEGER      NOT NULL REFERENCES vehiculo (id_vehiculo),
    id_usuario_abre             INTEGER      NOT NULL REFERENCES usuario (id_usuario),
    id_usuario_responsable      INTEGER      REFERENCES usuario (id_usuario),
    numero_bahia                SMALLINT     REFERENCES bahia (numero),
    id_usuario_autoriza_credito INTEGER      REFERENCES usuario (id_usuario),
    CONSTRAINT ck_orden_entrega CHECK (fecha_entrega IS NULL OR fecha_entrega >= fecha_apertura),
    CONSTRAINT ck_orden_credito CHECK (NOT entrega_a_credito OR id_usuario_autoriza_credito IS NOT NULL)
);

-- {una Bahia Ocupada tiene una sola OrdenServicio activa}
CREATE UNIQUE INDEX ux_orden_bahia_activa
    ON orden_servicio (numero_bahia)
    WHERE numero_bahia IS NOT NULL AND estado NOT IN ('Cerrada', 'Cancelada');

CREATE INDEX ix_orden_vehiculo ON orden_servicio (id_vehiculo);
CREATE INDEX ix_orden_estado   ON orden_servicio (estado);

-- Validación en la API: abre = Recepcionista; responsable = Mecanico o
-- JefeMecanicos; confirma (cita) = Recepcionista; registra compra =
-- EncargadoAlmacen. El rol del gerente que autoriza crédito sí se valida
-- en la base de datos (fn_validar_credito) por ser regla de cobro (RN-10).

-- -----------------------------------------------------------------------------
-- AsignacionColaborador (Usuario 1 —colabora— 0..*; OrdenServicio ◆ 0..*)
-- {un solo responsable; los colaboradores van en AsignacionColaborador} (RN-09)
-- -----------------------------------------------------------------------------
CREATE TABLE asignacion_colaborador (
    folio             VARCHAR(20) NOT NULL REFERENCES orden_servicio (folio) ON DELETE CASCADE,
    id_usuario        INTEGER     NOT NULL REFERENCES usuario (id_usuario),
    fecha_asignacion  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (folio, id_usuario)
);

-- -----------------------------------------------------------------------------
-- HistorialEstado (OrdenServicio ◆ 0..*; Usuario 0..1 —es responsable del cambio—)
-- {usuario nulo solo si el cambio lo origina la autorización del cliente}
-- {registro histórico: no se modifica ni se elimina} -> fn_registro_inmutable
-- -----------------------------------------------------------------------------
CREATE TABLE historial_estado (
    id_historial    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    folio           VARCHAR(20)  NOT NULL REFERENCES orden_servicio (folio),
    estado_anterior estado_orden,                       -- nulo en el registro de apertura
    estado_nuevo    estado_orden NOT NULL,
    fecha_hora      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    id_usuario      INTEGER      REFERENCES usuario (id_usuario),
    CONSTRAINT ck_historial_usuario CHECK (id_usuario IS NOT NULL OR estado_nuevo = 'Autorizada')
);

CREATE INDEX ix_historial_folio ON historial_estado (folio, fecha_hora);

-- -----------------------------------------------------------------------------
-- Entidades «OfflineSync» (RNF-06/RNF-08: persistencia local en IndexedDB y
-- sincronización posterior). uuid_local es el identificador que genera el
-- dispositivo sin conexión; su UNIQUE hace idempotente la sincronización y
-- evita duplicados (RNF-09).
-- -----------------------------------------------------------------------------

-- Diagnostico (OrdenServicio ◆ 0..*; Usuario —elabora— 0..*)
-- {registro histórico: no se modifica ni se elimina; un nuevo diagnóstico agrega otro registro}
CREATE TABLE diagnostico (
    id_diagnostico INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid_local     UUID        UNIQUE,
    folio          VARCHAR(20) NOT NULL REFERENCES orden_servicio (folio),
    id_usuario     INTEGER     NOT NULL REFERENCES usuario (id_usuario),
    fecha_hora     TIMESTAMPTZ NOT NULL,
    descripcion    TEXT        NOT NULL
);

CREATE INDEX ix_diagnostico_folio ON diagnostico (folio);

-- RecepcionVehicular (OrdenServicio ◆ 1; Cita 0..1 —se convierte en— 0..1)
-- {solo una Cita Confirmada se convierte en RecepcionVehicular, que abre la
--  OrdenServicio en estado Abierta} -> fn_validar_recepcion_cita
CREATE TABLE recepcion_vehicular (
    id_recepcion      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid_local        UUID              UNIQUE,
    folio             VARCHAR(20)       NOT NULL UNIQUE REFERENCES orden_servicio (folio) ON DELETE CASCADE,
    id_cita           INTEGER           UNIQUE REFERENCES cita (id_cita),
    fecha_hora        TIMESTAMPTZ       NOT NULL,
    kilometraje       INTEGER           NOT NULL CHECK (kilometraje >= 0),
    nivel_combustible nivel_combustible NOT NULL
);

-- ChecklistInspeccion (RecepcionVehicular ◆ 1)
CREATE TABLE checklist_inspeccion (
    id_checklist  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid_local    UUID    UNIQUE,
    id_recepcion  INTEGER NOT NULL UNIQUE REFERENCES recepcion_vehicular (id_recepcion) ON DELETE CASCADE,
    carroceria    TEXT,
    interiores    TEXT,
    observaciones TEXT,
    completo      BOOLEAN NOT NULL DEFAULT FALSE
);

-- Fotografia (RecepcionVehicular ◆ 4..*)
-- {mínimo 4: Frente, Trasera, Izquierda, Derecha} (RN-12): una foto por posición
-- obligatoria (índice parcial) y verificación del mínimo en v_recepcion_estado.
-- También se captura sin conexión, por eso lleva uuid_local.
CREATE TABLE fotografia (
    id_foto      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid_local   UUID          UNIQUE,
    id_recepcion INTEGER       NOT NULL REFERENCES recepcion_vehicular (id_recepcion) ON DELETE CASCADE,
    archivo      VARCHAR(255)  NOT NULL,             -- ruta del archivo en el almacenamiento
    posicion     posicion_foto NOT NULL,
    fecha_hora   TIMESTAMPTZ   NOT NULL
);

CREATE UNIQUE INDEX ux_fotografia_posicion
    ON fotografia (id_recepcion, posicion) WHERE posicion <> 'Otra';

-- -----------------------------------------------------------------------------
-- TokenAcceso (OrdenServicio ◆ 0..*; Cliente 1 —recibe— 0..*)
-- {fechaExpiracion = entrega y saldo del vehículo; el Cliente del token es
--  el propietario del Vehiculo de la orden} (RN-01) -> fn_validar_token_cliente
-- Se guarda el hash SHA-256 del token, nunca el token en claro (RNF-05).
-- -----------------------------------------------------------------------------
CREATE TABLE token_acceso (
    token_hash       CHAR(64)    PRIMARY KEY,
    folio            VARCHAR(20) NOT NULL REFERENCES orden_servicio (folio) ON DELETE CASCADE,
    id_cliente       INTEGER     NOT NULL REFERENCES cliente (id_cliente),
    canal            canal       NOT NULL DEFAULT 'Correo',
    fecha_emision    TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_expiracion TIMESTAMPTZ,                    -- se fija al entregar y saldar
    activo           BOOLEAN     NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_token_expiracion CHECK (fecha_expiracion IS NULL OR fecha_expiracion >= fecha_emision)
);

CREATE INDEX ix_token_folio ON token_acceso (folio);

-- -----------------------------------------------------------------------------
-- Cotizacion (OrdenServicio ◆ 0..*; Cotizacion 0..1 —reemplaza a— 0..1)
-- {vigencia 5 días naturales} (RN-11)
-- {si se genera una nueva versión por incremento mayor al 10 %, es obligatorio
--  crear un nuevo registro de Autorizacion} (RN-04)
-- /fechaVencimiento: columna generada; /total: vista v_cotizacion_total.
-- -----------------------------------------------------------------------------
CREATE TABLE cotizacion (
    id_cotizacion            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    folio                    VARCHAR(20)       NOT NULL REFERENCES orden_servicio (folio),
    version                  INTEGER           NOT NULL DEFAULT 1 CHECK (version >= 1),
    fecha_emision            DATE              NOT NULL DEFAULT CURRENT_DATE,
    vigencia_dias            INTEGER           NOT NULL DEFAULT 5 CHECK (vigencia_dias > 0),
    fecha_vencimiento        DATE              GENERATED ALWAYS AS (fecha_emision + vigencia_dias) STORED,
    estado                   estado_cotizacion NOT NULL DEFAULT 'Pendiente',
    id_cotizacion_reemplazada INTEGER          UNIQUE REFERENCES cotizacion (id_cotizacion),
    UNIQUE (folio, version),
    CONSTRAINT ck_cotizacion_no_autorreemplazo CHECK (id_cotizacion_reemplazada <> id_cotizacion)
);

-- DetalleCotizacion (Cotizacion ◆ 1..*)
CREATE TABLE detalle_cotizacion (
    id_detalle      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cotizacion   INTEGER       NOT NULL REFERENCES cotizacion (id_cotizacion) ON DELETE CASCADE,
    concepto        VARCHAR(200)  NOT NULL,
    tipo            tipo_concepto NOT NULL,
    cantidad        INTEGER       NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0),
    opcional        BOOLEAN       NOT NULL DEFAULT FALSE,
    seleccionado    BOOLEAN       NOT NULL DEFAULT TRUE,
    -- Solo los conceptos opcionales pueden deseleccionarse (RN-03).
    CONSTRAINT ck_detalle_seleccion CHECK (opcional OR seleccionado)
);

CREATE INDEX ix_detalle_cotizacion ON detalle_cotizacion (id_cotizacion);
-- Validación en la API: {1..*} — una cotización se envía al cliente solo si
-- tiene al menos un concepto.

-- -----------------------------------------------------------------------------
-- Autorizacion (Cotizacion 1 —requiere— 0..*; Autorizacion 0..* —se realiza
-- mediante— 0..1 TokenAcceso)
-- {registra fecha y hora, IP, monto aceptado y código de verificación} (RN-02, RNF-04)
-- Se guarda el hash del código 2FA, nunca el código en claro.
-- -----------------------------------------------------------------------------
CREATE TABLE autorizacion (
    id_autorizacion          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cotizacion            INTEGER             NOT NULL REFERENCES cotizacion (id_cotizacion),
    fecha_hora               TIMESTAMPTZ         NOT NULL DEFAULT now(),
    ip                       INET,
    medio                    medio_autorizacion  NOT NULL,
    tipo                     tipo_autorizacion   NOT NULL DEFAULT 'Inicial',
    monto_aceptado           NUMERIC(10,2)       NOT NULL CHECK (monto_aceptado >= 0),
    codigo_verificacion_hash VARCHAR(255)        NOT NULL,
    estado                   estado_autorizacion NOT NULL DEFAULT 'Pendiente',
    token_hash               CHAR(64)            REFERENCES token_acceso (token_hash),
    -- La autorización remota llega por el enlace del cliente y registra su IP.
    CONSTRAINT ck_autorizacion_remota CHECK (
        medio <> 'Remoto' OR (token_hash IS NOT NULL AND ip IS NOT NULL))
);

CREATE INDEX ix_autorizacion_cotizacion ON autorizacion (id_cotizacion);

-- -----------------------------------------------------------------------------
-- Pago (Cotizacion 1 —recibe— 0..*)
-- {el Pago se vincula a la Cotizacion Autorizada} -> fn_validar_pago
-- -----------------------------------------------------------------------------
CREATE TABLE pago (
    id_pago       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cotizacion INTEGER       NOT NULL REFERENCES cotizacion (id_cotizacion),
    monto         NUMERIC(10,2) NOT NULL CHECK (monto > 0),
    fecha_hora    TIMESTAMPTZ   NOT NULL DEFAULT now(),
    metodo        VARCHAR(30)   NOT NULL
);

CREATE INDEX ix_pago_cotizacion ON pago (id_cotizacion);

-- -----------------------------------------------------------------------------
-- Garantia (OrdenServicio ◆ 0..1)
-- {30 días desde la fechaEntrega de la orden; solo mano de obra} (RN-13)
-- -----------------------------------------------------------------------------
CREATE TABLE garantia (
    folio          VARCHAR(20)      PRIMARY KEY REFERENCES orden_servicio (folio) ON DELETE CASCADE,
    fecha_inicio   DATE             NOT NULL,
    duracion_dias  INTEGER          NOT NULL DEFAULT 30 CHECK (duracion_dias > 0),
    fecha_fin      DATE             GENERATED ALWAYS AS (fecha_inicio + duracion_dias) STORED,
    alcance        alcance_garantia NOT NULL DEFAULT 'ManoDeObra'
);

-- -----------------------------------------------------------------------------
-- Almacén: Proveedor, Refaccion, SolicitudRefaccion, Compra, DetalleCompra,
-- EntregaRefaccion
-- -----------------------------------------------------------------------------
CREATE TABLE proveedor (
    id_proveedor INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre       VARCHAR(160) NOT NULL,
    telefono     VARCHAR(20),
    correo       VARCHAR(160),
    CONSTRAINT ck_proveedor_contacto CHECK (telefono IS NOT NULL OR correo IS NOT NULL)
);

CREATE TABLE refaccion (
    id_refaccion INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre       VARCHAR(160) NOT NULL UNIQUE,
    existencia   INTEGER      NOT NULL DEFAULT 0 CHECK (existencia >= 0)
);

-- SolicitudRefaccion (OrdenServicio ◆ 0..*; Usuario 1 —solicita— 0..*;
-- Refaccion 1 —pide— 0..*)
CREATE TABLE solicitud_refaccion (
    id_solicitud     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    folio            VARCHAR(20)      NOT NULL REFERENCES orden_servicio (folio),
    id_usuario       INTEGER          NOT NULL REFERENCES usuario (id_usuario),
    id_refaccion     INTEGER          NOT NULL REFERENCES refaccion (id_refaccion),
    cantidad         INTEGER          NOT NULL CHECK (cantidad > 0),
    fecha_solicitud  TIMESTAMPTZ      NOT NULL DEFAULT now(),
    estado           estado_solicitud NOT NULL DEFAULT 'Solicitada'
);

CREATE INDEX ix_solicitud_folio ON solicitud_refaccion (folio);

-- Compra (Proveedor 1 —surte— 0..*; Usuario 1 —registra (almacén)— 0..*)
-- /total: vista v_compra_total.
CREATE TABLE compra (
    id_compra     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_proveedor  INTEGER     NOT NULL REFERENCES proveedor (id_proveedor),
    id_usuario    INTEGER     NOT NULL REFERENCES usuario (id_usuario),
    numero_ticket VARCHAR(40),
    fecha_compra  DATE        NOT NULL DEFAULT CURRENT_DATE
);

-- DetalleCompra (Compra ◆ 1..*; Refaccion 1 —incluye— 0..*;
-- SolicitudRefaccion 0..1 —se cubre en— 0..*)
-- /cantidadRecibida y /cantidadPendiente: vista v_detalle_compra_recepcion.
CREATE TABLE detalle_compra (
    id_detalle_compra INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_compra         INTEGER       NOT NULL REFERENCES compra (id_compra) ON DELETE CASCADE,
    id_refaccion      INTEGER       NOT NULL REFERENCES refaccion (id_refaccion),
    id_solicitud      INTEGER       REFERENCES solicitud_refaccion (id_solicitud),
    cantidad          INTEGER       NOT NULL CHECK (cantidad > 0),
    precio_unitario   NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0)
);

CREATE INDEX ix_detalle_compra_compra ON detalle_compra (id_compra);
-- Validación en la API: {1..*} — una compra se registra con al menos un detalle.

-- EntregaRefaccion (DetalleCompra ◆ 0..*)
-- {suma(cantidadRecibida) ≤ cantidad; entregas parciales permitidas}
-- -> fn_validar_entrega_refaccion
CREATE TABLE entrega_refaccion (
    id_entrega         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_detalle_compra  INTEGER NOT NULL REFERENCES detalle_compra (id_detalle_compra) ON DELETE CASCADE,
    fecha_entrega      DATE    NOT NULL DEFAULT CURRENT_DATE,
    cantidad_recibida  INTEGER NOT NULL CHECK (cantidad_recibida > 0)
);

-- =============================================================================
-- Vistas: atributos derivados y operaciones de consulta del diagrama
-- =============================================================================

-- Cotizacion./total, Cotizacion.estaVigente() y DetalleCotizacion.calcularSubtotal()
CREATE VIEW v_cotizacion_total AS
SELECT c.id_cotizacion,
       c.folio,
       c.version,
       c.estado,
       c.fecha_vencimiento,
       (CURRENT_DATE <= c.fecha_vencimiento)                                   AS esta_vigente,
       COALESCE(SUM(d.cantidad * d.precio_unitario) FILTER (WHERE d.seleccionado), 0)::NUMERIC(12,2) AS total
FROM cotizacion c
LEFT JOIN detalle_cotizacion d ON d.id_cotizacion = c.id_cotizacion
GROUP BY c.id_cotizacion;

-- OrdenServicio./totalAutorizado y /saldoPendiente
-- {/totalAutorizado = total de la Cotizacion en estado Autorizada}: si hubo
-- re-cotización, cuenta la versión autorizada más reciente.
-- {/saldoPendiente = Cotizacion Autorizada.total − suma(Pago.monto)}
CREATE VIEW v_orden_saldo AS
WITH autorizada AS (
    SELECT DISTINCT ON (folio) folio, id_cotizacion, total
    FROM v_cotizacion_total
    WHERE estado = 'Autorizada'
    ORDER BY folio, version DESC
)
SELECT o.folio,
       COALESCE(a.total, 0)::NUMERIC(12,2)                                      AS total_autorizado,
       COALESCE((SELECT SUM(p.monto) FROM pago p WHERE p.id_cotizacion = a.id_cotizacion), 0)::NUMERIC(12,2) AS total_pagado,
       (COALESCE(a.total, 0)
        - COALESCE((SELECT SUM(p.monto) FROM pago p WHERE p.id_cotizacion = a.id_cotizacion), 0))::NUMERIC(12,2) AS saldo_pendiente
FROM orden_servicio o
LEFT JOIN autorizada a ON a.folio = o.folio;

-- RecepcionVehicular.estaCompleta(): checklist completo y las 4 fotos obligatorias (RN-12)
CREATE VIEW v_recepcion_estado AS
SELECT r.id_recepcion,
       r.folio,
       COALESCE(ch.completo, FALSE)                                             AS checklist_completo,
       COUNT(DISTINCT f.posicion) FILTER (WHERE f.posicion <> 'Otra')            AS fotos_obligatorias,
       (COALESCE(ch.completo, FALSE)
        AND COUNT(DISTINCT f.posicion) FILTER (WHERE f.posicion <> 'Otra') = 4)  AS esta_completa
FROM recepcion_vehicular r
LEFT JOIN checklist_inspeccion ch ON ch.id_recepcion = r.id_recepcion
LEFT JOIN fotografia f            ON f.id_recepcion  = r.id_recepcion
GROUP BY r.id_recepcion, ch.completo;

-- Compra./total y Compra.calcularTotal()
CREATE VIEW v_compra_total AS
SELECT c.id_compra,
       COALESCE(SUM(d.cantidad * d.precio_unitario), 0)::NUMERIC(12,2) AS total
FROM compra c
LEFT JOIN detalle_compra d ON d.id_compra = c.id_compra
GROUP BY c.id_compra;

-- DetalleCompra./cantidadRecibida, /cantidadPendiente y calcularSubtotal()
CREATE VIEW v_detalle_compra_recepcion AS
SELECT d.id_detalle_compra,
       d.id_compra,
       d.id_refaccion,
       d.cantidad,
       (d.cantidad * d.precio_unitario)::NUMERIC(12,2)          AS subtotal,
       COALESCE(SUM(e.cantidad_recibida), 0)                    AS cantidad_recibida,
       d.cantidad - COALESCE(SUM(e.cantidad_recibida), 0)       AS cantidad_pendiente
FROM detalle_compra d
LEFT JOIN entrega_refaccion e ON e.id_detalle_compra = d.id_detalle_compra
GROUP BY d.id_detalle_compra;

-- Garantia.estaVigente()
CREATE VIEW v_garantia_vigencia AS
SELECT g.folio, g.fecha_inicio, g.fecha_fin,
       (CURRENT_DATE BETWEEN g.fecha_inicio AND g.fecha_fin) AS esta_vigente
FROM garantia g;

-- =============================================================================
-- Disparadores: restricciones del diagrama que no se expresan con CHECK
-- =============================================================================

-- {registro histórico: no se modifica ni se elimina} — HistorialEstado y Diagnostico
CREATE FUNCTION fn_registro_inmutable() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'La tabla % es un registro histórico: no se modifica ni se elimina', TG_TABLE_NAME;
END;
$$;

CREATE TRIGGER tg_historial_inmutable BEFORE UPDATE OR DELETE ON historial_estado
    FOR EACH ROW EXECUTE FUNCTION fn_registro_inmutable();
CREATE TRIGGER tg_diagnostico_inmutable BEFORE UPDATE OR DELETE ON diagnostico
    FOR EACH ROW EXECUTE FUNCTION fn_registro_inmutable();

-- {solo una Cita Confirmada se convierte en RecepcionVehicular}
CREATE FUNCTION fn_validar_recepcion_cita() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.id_cita IS NOT NULL AND
       (SELECT estado FROM cita WHERE id_cita = NEW.id_cita) <> 'Confirmada' THEN
        RAISE EXCEPTION 'Solo una cita Confirmada puede convertirse en recepción (cita %)', NEW.id_cita;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_recepcion_cita BEFORE INSERT OR UPDATE OF id_cita ON recepcion_vehicular
    FOR EACH ROW EXECUTE FUNCTION fn_validar_recepcion_cita();

-- {el Cliente del token es el propietario del Vehiculo de la orden}
CREATE FUNCTION fn_validar_token_cliente() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1
                   FROM orden_servicio o
                   JOIN vehiculo v ON v.id_vehiculo = o.id_vehiculo
                   WHERE o.folio = NEW.folio AND v.id_cliente = NEW.id_cliente) THEN
        RAISE EXCEPTION 'El cliente % no es el propietario del vehículo de la orden %', NEW.id_cliente, NEW.folio;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_token_cliente BEFORE INSERT OR UPDATE OF folio, id_cliente ON token_acceso
    FOR EACH ROW EXECUTE FUNCTION fn_validar_token_cliente();

-- {el Pago se vincula a la Cotizacion Autorizada}
CREATE FUNCTION fn_validar_pago() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF (SELECT estado FROM cotizacion WHERE id_cotizacion = NEW.id_cotizacion) <> 'Autorizada' THEN
        RAISE EXCEPTION 'Solo se registran pagos sobre una cotización Autorizada (cotización %)', NEW.id_cotizacion;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_pago_cotizacion BEFORE INSERT OR UPDATE OF id_cotizacion ON pago
    FOR EACH ROW EXECUTE FUNCTION fn_validar_pago();

-- {crédito solo si el propietario del vehículo es una Flotilla con
--  creditoHabilitado y lo autoriza un Usuario con rol Gerente} (RN-10)
CREATE FUNCTION fn_validar_credito() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.entrega_a_credito THEN
        IF NOT EXISTS (SELECT 1 FROM usuario
                       WHERE id_usuario = NEW.id_usuario_autoriza_credito
                         AND rol = 'Gerente' AND activo) THEN
            RAISE EXCEPTION 'La entrega a crédito de la orden % debe autorizarla un Gerente activo', NEW.folio;
        END IF;
        IF NOT EXISTS (SELECT 1
                       FROM vehiculo v
                       JOIN flotilla f ON f.id_cliente = v.id_cliente
                       WHERE v.id_vehiculo = NEW.id_vehiculo AND f.credito_habilitado) THEN
            RAISE EXCEPTION 'La orden % no pertenece a una flotilla con crédito habilitado', NEW.folio;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_orden_credito BEFORE INSERT OR UPDATE OF entrega_a_credito, id_usuario_autoriza_credito, id_vehiculo
    ON orden_servicio FOR EACH ROW EXECUTE FUNCTION fn_validar_credito();

-- RN-10: no se entrega un vehículo con saldo pendiente, salvo entrega a crédito autorizada.
CREATE FUNCTION fn_validar_entrega() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.fecha_entrega IS NOT NULL AND OLD.fecha_entrega IS NULL
       AND NOT NEW.entrega_a_credito
       AND (SELECT saldo_pendiente FROM v_orden_saldo WHERE folio = NEW.folio) > 0 THEN
        RAISE EXCEPTION 'La orden % tiene saldo pendiente: no puede entregarse sin autorización de crédito', NEW.folio;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_orden_entrega BEFORE UPDATE OF fecha_entrega ON orden_servicio
    FOR EACH ROW EXECUTE FUNCTION fn_validar_entrega();

-- {suma(cantidadRecibida) ≤ cantidad; entregas parciales permitidas}
CREATE FUNCTION fn_validar_entrega_refaccion() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_pedida   INTEGER;
    v_recibida INTEGER;
BEGIN
    SELECT cantidad INTO v_pedida
    FROM detalle_compra WHERE id_detalle_compra = NEW.id_detalle_compra
    FOR UPDATE;

    SELECT COALESCE(SUM(cantidad_recibida), 0) INTO v_recibida
    FROM entrega_refaccion
    WHERE id_detalle_compra = NEW.id_detalle_compra
      AND id_entrega IS DISTINCT FROM NEW.id_entrega;

    IF v_recibida + NEW.cantidad_recibida > v_pedida THEN
        RAISE EXCEPTION 'Se recibirían % piezas y solo se compraron % (detalle %)',
            v_recibida + NEW.cantidad_recibida, v_pedida, NEW.id_detalle_compra;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_entrega_refaccion BEFORE INSERT OR UPDATE ON entrega_refaccion
    FOR EACH ROW EXECUTE FUNCTION fn_validar_entrega_refaccion();

COMMIT;
