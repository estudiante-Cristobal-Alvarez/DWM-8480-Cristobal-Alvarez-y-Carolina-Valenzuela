import os
import grpc

from services.orders.proto import inventory_pb2
from services.orders.proto import inventory_pb2_grpc


# Dirección del servidor gRPC de Inventory
GRPC_INVENTORY_URL = os.getenv(
    "GRPC_INVENTORY_URL",
    "127.0.0.1:50051"
)


def consultar_stock_con_grpc(product_id: int, cantidad: int):
    """
    Consulta la disponibilidad de un producto mediante gRPC.
    """

    # Validar los parámetros antes de consultar
    if product_id <= 0 or cantidad <= 0:
        return {
            "disponible": False,
            "mensaje": "El producto y la cantidad deben ser mayores que cero",
            "precio_unitario": 0.0
        }

    # Crear la solicitud gRPC
    request = inventory_pb2.StockRequest(
        product_id=product_id,
        cantidad_solicitada=cantidad
    )

    try:
        # Conexión local con Inventory
        with grpc.insecure_channel(GRPC_INVENTORY_URL) as channel:
            stub = inventory_pb2_grpc.InventoryServiceStub(channel)

            response = stub.CheckStock(
                request,
                timeout=3.0
            )

            return {
                "disponible": response.disponible,
                "mensaje": response.mensaje,
                "precio_unitario": response.precio_unitario
            }

    except grpc.RpcError as error:
        print(
            f"Error de comunicación gRPC: "
            f"{error.code().name} - {error.details()}"
        )

        return {
            "disponible": False,
            "mensaje": "Servicio de inventario no disponible temporalmente",
            "precio_unitario": 0.0
        }
