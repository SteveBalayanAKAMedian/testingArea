import cell_pb2_grpc
import grpc

from cell_pb2 import PutRequest
from google.protobuf.empty_pb2 import Empty


if __name__ == '__main__':
    with grpc.insecure_channel('localhost:9999') as channel:
        stub = cell_pb2_grpc.CellStub(channel)
        response = stub.Put(PutRequest(data=b'hello'))
        assert response.status
        response = stub.Get(Empty())
        print(response.data)
        response = stub.Put(PutRequest(data=b'another hello'))
        assert response.status
        for response in stub.GetAll(Empty()):
            print(response.data)
