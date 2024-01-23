from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from typing import Iterable

from qdrant_db.config import QdrantConfig

class Qdrant:

    def __init__(self):
        config = QdrantConfig()
        host, port = config.get_host(), config.get_port()
        self.client = QdrantClient(host=host, port=port)
        self.collection = config.get_collection()

    def get_client(self):
        return self.client

    def get_collection_name(self):
        return self.collection

    def get_collection(self):
        return self.client.get_collection(collection_name=self.collection)
    
    def create_collection(self, vector_size):
        print(f"Creating collection {self.collection} with vector size {vector_size}")
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            ),
        )

    def delete_collection(self):
        print(f"Deleting collection {self.collection}")
        self.client.delete_collection(collection_name=self.collection)

    def upload_points(self, points: Iterable[PointStruct]):
        print(f"Uploading {points.__sizeof__} points to collection {self.collection}")
        self.client.upload_points(
            collection_name=self.collection,
            points=points
        )


