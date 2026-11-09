import grpc
from concurrent import futures

from services.inventory.proto import inventory_pb2
from services.inventory.proto import inventory_pb2_grpc
from database import SessionLocal
from models import Producto

class InventoryServiceServicer(inventory_pb2_grpc.InventoryServiceServicer):
    
    def CheckStock(self, request, context):
        db = SessionLocal()
        try:
            # Buscamos el producto por su ID
            producto = db.query(Producto).filter(Producto.id == request.product_id).first()
            
            if not producto:
                return inventory_pb2.StockResponse(
                    disponible=False,
                    mensaje=f"Producto con ID {request.product_id} no encontrado",
                    precio_unitario=0.0
                )
            
            # Verificamos si el producto está disponible según tu modelo
            if producto.disponible:
                return inventory_pb2.StockResponse(
                    disponible=True,
                    mensaje="Producto disponible",
                    precio_unitario=float(producto.precio)
                )
            else:
                return inventory_pb2.StockResponse(
                    disponible=False,
                    mensaje="El producto no se encuentra disponible actualmente",
                    precio_unitario=float(producto.precio)
                )
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🚀 Servidor gRPC de Inventory corriendo en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()