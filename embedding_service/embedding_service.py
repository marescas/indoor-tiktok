import base64

import grpc
import protos.embedding_pb2 as embedding_pb2
from protos import embedding_pb2_grpc
from concurrent import futures
import time
import tensorflow as tf
import numpy as np


class ImageProcedureServicer(embedding_pb2_grpc.ImageProcedureServicer):
    def __init__(self):
        self.model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, pooling="avg")

    def ImageToEmbedding(self, request, context):
        b64decoded = base64.b64decode(request.b64image)
        imgarr = np.frombuffer(b64decoded, dtype=np.uint8).reshape(1, request.width, request.height, -1)
        hyp = self.model.predict(imgarr)
        return embedding_pb2.Embedding(embedding=list(tf.math.l2_normalize(hyp[0])))


if __name__ == '__main__':
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))
    embedding_pb2_grpc.add_ImageProcedureServicer_to_server(
        ImageProcedureServicer(), server)
    print('Starting server. Listening on port 5005.')
    server.add_insecure_port('[::]:5005')
    server.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)
