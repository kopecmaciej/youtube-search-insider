import os
import qdrant
from qdrant_client.conversions.common_types import Record
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, qdrant_client
from qdrant_client.models import VectorParams, Distance

def tokenize(client: QdrantClient, collection: str):
    processed_dir = "processed"
    texts = []

    for file in os.listdir(processed_dir):
        with open(f"{processed_dir}/{file}", "r") as f:
            text = f.read()
            obj = {}
            obj['name'] = file
            obj['text'] = text
            texts.append(obj)

    print("Loaded texts {}".format(len(texts)))


    encoder = SentenceTransformer('all-MiniLM-L6-v2', device="cuda")

    try:
        coll = client.get_collection(collection_name=collection)
        if coll is None:
            client.delete_collection(collection_name=collection)
            print("Collection does not exist")
            raise Exception()
    except:
        print("Creating collection")
        client.create_collection(
            collection_name=collection, 
            vectors_config=VectorParams(
                size=encoder.get_sentence_embedding_dimension(), #type: ignore
                distance=Distance.COSINE
            ),
        )

    client.upload_points(
        collection_name=collection,
        points=[
            PointStruct(
                vector=encoder.encode(obj['text']), #type: ignore
                payload={"name": obj['name']},
                id=i,
            )
            for i, obj in enumerate(texts)
        ],
    )

