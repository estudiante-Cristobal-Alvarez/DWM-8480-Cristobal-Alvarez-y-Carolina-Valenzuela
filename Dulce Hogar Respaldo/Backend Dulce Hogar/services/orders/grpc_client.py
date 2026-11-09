import grpc
from services.orders.proto import inventory_pb2
from services.orders.proto import inventory_pb2_grpc

def consultar_stock_con_grpc(product_id: int, cantidad: int):
    """
    Se conecta al servidor gRPC de Inventory en el puerto 50051 
    para validar la disponibilidad de stock de forma ultrarrápida.
    """
    # Nos conectamos al canal inseguro de gRPC en localhost:50051
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        
        # Creamos la petición tipada definida en el contrato .proto
        request = inventory_pb2.StockRequest(
            product_id=product_id,
            cantidad_solicitada=cantidad
        )
        
        try:
            # Ejecutamos la llamada remota con un tiempo límite (timeout) de 3 segundos
            response = stub.CheckStock(request, timeout=3.0)
            return {
                "disponible": response.disponible,
                "mensaje": response.mensaje,
                "precio_unitario": response.precio_unitario
            }
        except grpc.RpcError as e:
            print(f"Error de comunicación gRPC: {e.code().name} - {e.details()}")
            return {
                "disponible": False,
                "mensaje": "Servicio de inventario no disponible temporalmente",
                "precio_unitario": 0.0
            }