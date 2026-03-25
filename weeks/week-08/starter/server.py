import grpc
from concurrent import futures
import time
# Импортируйте сгенерированные модули
import service_pb2
import service_pb2_grpc

class ShipmentService(service_pb2_grpc.ShipmentsServiceServicer):
    def CreateShipment(self, request, context):
        # Реализуем логику создания отправления
        return service_pb2.CreateShipmentResponse(
            id=1, 
            tracking=request.tracking
        )
    
    def TrackShipment(self, request, context):
        # Реализуем streaming метод
        statuses = ["created", "shipped", "in_transit", "delivered"]
        locations = ["Warehouse", "Moscow", "Transit", "Customer"]
        
        for i, (status, location) in enumerate(zip(statuses, locations)):
            yield service_pb2.ShipmentUpdate(
                id=request.id,
                status=status,
                location=location,
                sequence=i
            )
            time.sleep(0.5)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Добавляем наш сервис
    service_pb2_grpc.add_ShipmentsServiceServicer_to_server(
        ShipmentService(), server
    )
    server.add_insecure_port('[::]:8290')
    print("Server started on port 8290")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
