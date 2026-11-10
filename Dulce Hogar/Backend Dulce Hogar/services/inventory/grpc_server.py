import grpc
from concurrent import futures

from services.inventory.database import SessionLocal
from services.inventory.models import Producto
from services.inventory.proto import inventory_pb2, inventory_pb2_grpc


class InventoryServiceServicer(inventory_pb2_grpc.InventoryServiceServicer):
    def CheckStock(self, request, context):
        if request.product_id <= 0 or request.cantidad_solicitada <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "El ID del producto y la cantidad solicitada deben ser mayores que cero",
            )

        with SessionLocal() as db:
            producto = db.get(Producto, request.product_id)

            if producto is None:
                return inventory_pb2.StockResponse(
                    disponible=False,
                    mensaje=f"Producto con ID {request.product_id} no encontrado",
                    precio_unitario=0.0,
                )

            if not producto.disponible:
                return inventory_pb2.StockResponse(
                    disponible=False,
                    mensaje="El producto no se encuentra disponible actualmente",
                    precio_unitario=float(producto.precio),
                )

            # El modelo Producto actual no tiene un campo de unidades en stock.
            # Por eso solo podemos validar la disponibilidad general, no la
            # cantidad solicitada. No afirmar que existe stock suficiente.
            return inventory_pb2.StockResponse(
                disponible=True,
                mensaje="Producto habilitado para la venta; cantidad en stock no verificada",
                precio_unitario=float(producto.precio),
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(
        InventoryServiceServicer(), server
    )
    puerto = server.add_insecure_port("127.0.0.1:50051")
    if puerto == 0:
        raise RuntimeError("No se pudo abrir el puerto gRPC 50051")
    server.start()
    print("Servidor gRPC de Inventory disponible en 127.0.0.1:50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(grace=3)


if __name__ == "__main__":
    serve()
