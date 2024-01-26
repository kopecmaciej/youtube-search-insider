from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from typing import Iterable

from qdrant_db.config import QdrantConfig

class Qdrant:

    def __init__(self):
        config = QdrantConfig()
        host, port = config.get_host(), config.get_port()
        try:
            self.client = QdrantClient(host=host, port=port)
            self.collection = config.get_collection()
        except Exception as e:
            print(f"Error connecting to Qdrant: {e}")
            raise e

    def get_client(self):
        return self.client

    def get_collection_name(self):
        return self.collection

    def get_collection(self):
        return self.client.get_collection(collection_name=self.collection)
    
    def create_collection(self, vector_size):
        print(f"Creating collection {self.collection} with vector size {vector_size}")
        try:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                ),
            )
        except Exception as e:
            print(f"Error creating collection: {e}")
            pass

    def delete_collection(self):
        print(f"Deleting collection {self.collection}")
        self.client.delete_collection(collection_name=self.collection)

    def upload_points(self, points: Iterable[PointStruct]):
        print(f"Uploading points to collection {self.collection}")
        self.client.upload_points(
            collection_name=self.collection,
            points=points
        )


