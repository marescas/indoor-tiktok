import base64

import numpy as np
from PIL import Image
from vespa.application import Vespa
import streamlit as st
import grpc
from protos import embedding_pb2_grpc, embedding_pb2

if __name__ == '__main__':
    channel = grpc.insecure_channel('127.0.0.1:5005')
    vespa_endpoint = Vespa(url="http://localhost", port=8080)
    stub = embedding_pb2_grpc.ImageProcedureStub(channel)
    uploaded_file = st.file_uploader("Choose a file", type="jpg")
    # open upload file
    if uploaded_file is not None:
        with Image.open(uploaded_file) as img:
            st.write("Query image:")
            # resize image
            frame = img.resize(size=(224, 224))
            st.image(frame)
            st.write("*" * 100)
            # encode
            data = base64.b64encode(np.array(frame))
            image_req = embedding_pb2.B64Image(b64image=data, width=224, height=224)
            try:
                # get embedding
                response = stub.ImageToEmbedding(image_req)
                # get similar images with ANN on Vespa
                recommendations = vespa_endpoint.query(body={
                    'yql': (
                        'select filename from images where ({targetHits:100,approximate:true}nearestNeighbor(embedding,query_embedding)) ;'),
                    'hits': 10,
                    'input.query(query_embedding)': list(response.embedding),
                    'ranking.profile': 'semantic-similarity'
                })
                rec = recommendations.get_json()
                for recommendation in rec["root"]["children"]:
                    st.write(
                        f"Recommendation: {recommendation['fields']['filename']} with relevance: {recommendation['relevance']} ")
                    st.image(Image.open(recommendation['fields']['filename']))
            except Exception as e:
                print(f"Error {str(e)}")
