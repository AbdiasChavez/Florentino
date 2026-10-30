"""Crea las tablas (solo SQLite) y las 4 bahías; con --demo agrega datos FICTICIOS.

    python -m app.semilla --demo

Las contraseñas de los usuarios de demostración salen de SEED_PASSWORD; si no
está definida se genera una al azar y se imprime una sola vez. Nunca se
guardan contraseñas en el repositorio.
"""
import os
import secrets
import sys

from sqlalchemy import select

from app import config, seguridad
from app.db import Base, SessionLocal, engine
from app.models import Bahia, Cliente, ClienteParticular, EstadoBahia, Flotilla, RolUsuario, TipoVehiculo, Usuario, Vehiculo


def preparar_base() -> None:
    if engine.url.get_backend_name() == "sqlite":
        Base.metadata.create_all(engine)  # en PostgreSQL se usa db/schema.sql
    with SessionLocal() as db:
        for n in range(1, config.BAHIAS + 1):
            if not db.get(Bahia, n):
                db.add(Bahia(numero=n, estado=EstadoBahia.Libre))
        db.commit()


def cargar_demo() -> None:
    preparar_base()
    contrasena = os.getenv("SEED_PASSWORD") or secrets.token_urlsafe(12)
    with SessionLocal() as db:
        if db.scalar(select(Usuario)):
            print("La base ya tiene datos; no se cargó la demostración.")
            return
        personal = [("Laura Gerente Demo", "gerente@taller.test", RolUsuario.Gerente),
                    ("Rosa Recepción Demo", "recepcion@taller.test", RolUsuario.Recepcionista),
                    ("Javier Jefe Demo", "jefe@taller.test", RolUsuario.JefeMecanicos),
                    ("Alma Almacén Demo", "almacen@taller.test", RolUsuario.EncargadoAlmacen)]
        for nombre, correo, rol in personal:
            db.add(Usuario(nombre=nombre, correo=correo, rol=rol, contrasena_hash=seguridad.hash_secreto(contrasena)))
        db.add(Usuario(nombre="Mario Mecánico Demo", correo="mecanico1@taller.test", rol=RolUsuario.Mecanico))
        particular = Cliente(tipo_cliente="Particular", telefono="9710000001", correo="cliente.demo@ejemplo.test")
        particular.particular = ClienteParticular(nombre="Cliente Ficticio Uno")
        particular.vehiculos.append(Vehiculo(placas="DEMO-001", marca="Nissan", modelo="Versa", anio=2019,
                                             tipo=TipoVehiculo.Automovil))
        flotilla = Cliente(tipo_cliente="Flotilla", telefono="9710000002", correo="flotilla.demo@ejemplo.test")
        flotilla.flotilla = Flotilla(razon_social="Transportes Ficticios S.A.", credito_habilitado=True)
        flotilla.vehiculos.append(Vehiculo(placas="FLT-100", marca="Ford", modelo="Ranger", anio=2021,
                                           tipo=TipoVehiculo.Camioneta))
        db.add_all([particular, flotilla])
        db.commit()
    if not os.getenv("SEED_PASSWORD"):
        print(f"Contraseña de los usuarios de demostración: {contrasena}")
    print("Datos ficticios cargados. Correos: gerente@, recepcion@, jefe@, almacen@taller.test")


if __name__ == "__main__":
    cargar_demo() if "--demo" in sys.argv else preparar_base()
