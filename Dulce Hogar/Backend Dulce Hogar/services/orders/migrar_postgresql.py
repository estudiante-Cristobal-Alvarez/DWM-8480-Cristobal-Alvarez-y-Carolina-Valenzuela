import sqlite3
from pathlib import Path

from sqlalchemy import text, select, func

from services.orders.database import engine, Base
from services.orders.models import Pedido, DetallePedido

SQLITE_PATH = Path(__file__).resolve().parent / "orders.db"


def migrar():
    if engine.dialect.name != "postgresql":
        raise RuntimeError("La conexion de destino no es PostgreSQL")

    if not SQLITE_PATH.is_file():
        raise FileNotFoundError("No se encontro orders.db")

    print("Iniciando migracion de SQLite a PostgreSQL")

    # Leer los datos originales sin modificarlos
    with sqlite3.connect(
        SQLITE_PATH.as_uri() + "?mode=ro",
        uri=True
    ) as origen:

        origen.row_factory = sqlite3.Row
        origen.execute("BEGIN")

        pedidos = [
            dict(fila)
            for fila in origen.execute("SELECT * FROM pedidos")
        ]

        detalles = [
            dict(fila)
            for fila in origen.execute("SELECT * FROM detalle_pedidos")
        ]

    print("Pedidos encontrados:", len(pedidos))
    print("Detalles encontrados:", len(detalles))

    # Crear las tablas en PostgreSQL
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conexion:

        # Evitar duplicar o sobrescribir datos existentes
        total_pedidos = conexion.scalar(
            select(func.count()).select_from(Pedido)
        )

        total_detalles = conexion.scalar(
            select(func.count()).select_from(DetallePedido)
        )

        if total_pedidos or total_detalles:
            raise RuntimeError(
                "PostgreSQL ya contiene datos. Migracion cancelada."
            )

        # Insertar primero los pedidos
        if pedidos:
            conexion.execute(
                Pedido.__table__.insert(),
                pedidos
            )

        # Insertar los detalles asociados
        if detalles:
            conexion.execute(
                DetallePedido.__table__.insert(),
                detalles
            )

        # Actualizar las secuencias de identificadores
        for tabla in ("pedidos", "detalle_pedidos"):
            conexion.execute(text(f"""
                SELECT setval(
                    pg_get_serial_sequence('{tabla}', 'id'),
                    COALESCE(MAX(id), 1),
                    COUNT(*) > 0
                )
                FROM {tabla}
            """))

        # Verificar las cantidades migradas
        pedidos_migrados = conexion.scalar(
            select(func.count()).select_from(Pedido)
        )

        detalles_migrados = conexion.scalar(
            select(func.count()).select_from(DetallePedido)
        )

        if pedidos_migrados != len(pedidos):
            raise RuntimeError("Cantidad de pedidos incorrecta")

        if detalles_migrados != len(detalles):
            raise RuntimeError("Cantidad de detalles incorrecta")

    print("Migracion completada correctamente")
    print("Pedidos migrados:", pedidos_migrados)
    print("Detalles migrados:", detalles_migrados)


if __name__ == "__main__":
    migrar()