from concurrent import futures

import grpc

from proto import likes_pb2, likes_pb2_grpc

from db import SessionLocal
from models import Like


class LikeServiceServicer(

    likes_pb2_grpc.LikeServiceServicer
):

    def GetLikesCount(
        self,
        request,
        context
    ):

        db = SessionLocal()

        count = db.query(Like).filter(
            Like.post_id == request.post_id
        ).count()

        return likes_pb2.LikeResponse(
            count=count
        )


def start_grpc_server():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    likes_pb2_grpc.add_LikeServiceServicer_to_server(
        LikeServiceServicer(),
        server
    )

    server.add_insecure_port("[::]:50051")

    server.start()

    print("gRPC server started on 50051")

    server.wait_for_termination()

