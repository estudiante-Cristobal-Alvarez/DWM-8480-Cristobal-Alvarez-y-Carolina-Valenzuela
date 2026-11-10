
import grpc

from services.inventory.proto import inventory_pb2
from services.inventory.proto import inventory_pb2_grpc


# Conexión con Inventory mediante gRPC
with grpc.insecure_channel("127.0.0.1:50051") as canal:

    cliente = inventory_pb2_grpc.InventoryServiceStub(canal)

    # Consultar el producto con ID 1
    solicitud = inventory_pb2.StockRequest(
        product_id=1,
        cantidad_solicitada=1
    )

    respuesta = cliente.CheckStock(solicitud, timeout=5)

    print("Disponible:", respuesta.disponible)
    print("Mensaje:", respuesta.mensaje)
    print("Precio unitario:", respuesta.precio_unitario)
