import cell_pb2_grpc
import grpc

from cell_pb2 import GetResponse, PutResponse
from concurrent import futures


class Cell:
    data = []

    @classmethod
    def store(cls, data):
        cls.data.append(data)

    @classmethod
    def get(cls):
        return cls.data[-1]

    @classmethod
    def get_all(cls):
        return cls.data.copy()


class CellService(cell_pb2_grpc.CellServicer):
    def Get(self, request, context):
        return GetResponse(data=Cell.get())

    def Put(self, request, context):
        Cell.store(request.data)
        return PutResponse(status=True)

    def GetAll(self, request, context):
        data = Cell.get_all()
        for item in data:
            yield GetResponse(data=item)


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    cell_pb2_grpc.add_CellServicer_to_server(CellService(), server)
    server.add_insecure_port('localhost:9999')
    server.start()
    server.wait_for_termination(timeout=None)
