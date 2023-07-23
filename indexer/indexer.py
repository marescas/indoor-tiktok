import base64
import random
from typing import List

import grpc
from protos import embedding_pb2_grpc, embedding_pb2
import numpy as np
import tqdm
import glob
from PIL import Image
from vespa.application import Vespa


def create_vespa_doc(idx: int, filename: str, embedding: List[float]):
    vespa_doc = {
        "put": f"id:images:images::{idx}",
        "fields": {
            "id": idx,
            "filename": filename,
            "embedding": {
                "values": embedding
            }
        }
    }
    return vespa_doc


if __name__ == '__main__':
    # open a gRPC channel
    channel = grpc.insecure_channel('127.0.0.1:5005')
    vespa_endpoint = Vespa(url="http://localhost", port=8080, )
    i = 1
    files = list(glob.glob("Images/*/*"))
    random.shuffle(files)
    for file in tqdm.tqdm(files[:3000]):
        stub = embedding_pb2_grpc.ImageProcedureStub(channel)
        with Image.open(file) as img:
            frame = img.resize(size=(224, 224))
            data = base64.b64encode(np.array(frame))
            image_req = embedding_pb2.B64Image(b64image=data, width=224, height=224)
            try:
                response = stub.ImageToEmbedding(image_req)
                vespa_doc = create_vespa_doc(idx=i, filename=file, embedding=list(response.embedding))
                vespa_endpoint.feed_data_point(schema="images", data_id=i, fields=vespa_doc["fields"])
            except Exception as e:
                print(f"Error in {file} with error {str(e)}")

        i += 1
