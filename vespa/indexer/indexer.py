import base64

import grpc
import embedding_pb2_grpc, embedding_pb2
import numpy as np
import pandas as pd
import tqdm
import glob
from PIL import Image
from collections import defaultdict
import logging
from vespa.application import Vespa

if __name__ == '__main__':
    # open a gRPC channel
    channel = grpc.insecure_channel('127.0.0.1:5005')
    vespa_endpoint = Vespa(url="http://localhost", port=8080, )
    i = 1
    to_index = defaultdict(list)
    for file in tqdm.tqdm(list(glob.glob("Images/*/*"))[:500]):
        stub = embedding_pb2_grpc.ImageProcedureStub(channel)
        with Image.open(file) as img:
            frame = img.resize(size=(224, 224))
            data = base64.b64encode(np.array(frame))
            image_req = embedding_pb2.B64Image(b64image=data, width=224, height=224)
            try:
                response = stub.ImageToEmbedding(image_req)
                to_index["id"].append(f"indoor.tiktok.{i}")
                to_index["filename"].append(file)
                to_index["embedding"].append(list(response.embedding))
            except:
                logging.error(f"Error with image {file}")
        if i % 10 == 0:
            logging.warning("*" * 100)
            logging.warning("INDEXATION")
            logging.warning("*" * 100)
            dataframe_to_index = pd.DataFrame(to_index)
            vespa_endpoint.feed_batch(dataframe_to_index.to_json(lines=True,orient="records"), schema="images")
            to_index = defaultdict(list)
        i += 1
    if len(to_index) > 0:
        logging.warning("*" * 100)
        logging.warning("INDEXATION")
        logging.warning("*" * 100)
        dataframe_to_index = pd.DataFrame(to_index)
        vespa_endpoint.feed_df(dataframe_to_index)
        to_index = defaultdict(list)
