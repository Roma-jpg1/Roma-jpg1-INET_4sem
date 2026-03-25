import time
import requests
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import service_pb2
import service_pb2_grpc

def run_rest_bench():
    """REST бенчмарк"""
    print("REST benchmark...")
    start = time.time()
    
    for i in range(1000):
        requests.post(
            "http://localhost:5000/api/shipments",
            json={'tracking': f'TRK{i}'}
        )
    
    total = time.time() - start
    print(f"REST: {total:.2f}s, avg: {total/1000*1000:.2f}ms")
    return total

def run_grpc_bench():
    """gRPC бенчмарк"""
    print("gRPC benchmark...")
    start = time.time()
    
    channel = grpc.insecure_channel('localhost:8290')
    stub = service_pb2_grpc.ShipmentsServiceStub(channel)
    
    for i in range(1000):
        stub.CreateShipment(service_pb2.CreateShipmentRequest(tracking=f'TRK{i}'))
    
    channel.close()
    total = time.time() - start
    print(f"gRPC: {total:.2f}s, avg: {total/1000*1000:.2f}ms")
    return total

def test_streaming():
    """Тест streaming метода"""
    print("\nStreaming test...")
    
    channel = grpc.insecure_channel('localhost:8290')
    stub = service_pb2_grpc.ShipmentsServiceStub(channel)
    
    # Создаем отправление
    resp = stub.CreateShipment(service_pb2.CreateShipmentRequest(tracking='TEST001'))
    print(f"Created: id={resp.id}")
    
    # Получаем поток обновлений
    request = service_pb2.TrackShipmentRequest(id=resp.id, tracking='TEST001')
    
    print("Updates:")
    for update in stub.TrackShipment(request):
        print(f"  {update.sequence}: {update.status} @ {update.location}")
        if update.sequence == 3:
            break
    
    channel.close()

def main():
    print("=== Benchmark ===\n")
    
    rest_time = run_rest_bench()
    grpc_time = run_grpc_bench()
    
    # Сохраняем результаты
    with open('/home/adduser/stud_roma/INET_2sem/distrib_systems_tasks/weeks/week-08/bench/results.md', 'w') as f:
        f.write("# Benchmark Results\n\n")
        f.write(f"**REST**: {rest_time:.2f}s ({rest_time/1000*1000:.2f}ms avg)\n\n")
        f.write(f"**gRPC**: {grpc_time:.2f}s ({grpc_time/1000*1000:.2f}ms avg)\n\n")
        
        if grpc_time < rest_time:
            f.write(f"**gRPC is {(rest_time - grpc_time)/rest_time*100:.1f}% faster**\n")
        else:
            f.write(f"**REST is {(grpc_time - rest_time)/grpc_time*100:.1f}% faster**\n")
    
    test_streaming()

if __name__ == "__main__":
    main()