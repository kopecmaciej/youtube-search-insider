import os

class QdrantConfig:
    def __init__(self):
        host = os.getenv("QDRANT_HOST")
        if host is None:
            raise Exception("QDRANT_HOST is not set")
        self.host = host
        port = os.getenv("QDRANT_PORT")
        if port is None:
            raise Exception("QDRANT_PORT is not set")
        self.port = port
        collection = os.getenv("QDRANT_COLLECTION")
        if collection is None:
            raise Exception("QDRANT_COLLECTION is not set")
        self.collection = collection

    def get_host(self):
        return self.host

    def get_port(self):
        return int(self.port)
    
    def get_collection(self):
        return self.collection
