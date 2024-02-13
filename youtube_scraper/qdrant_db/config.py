import os


class QdrantConfig:
    def __init__(self):
        url = os.getenv("QDRANT_URL")
        if url is None:
            raise Exception("QDRANT_URL is not set")
        self.url = url
        collection = os.getenv("QDRANT_COLLECTION")
        if collection is None:
            raise Exception("QDRANT_COLLECTION is not set")
        self.collection = collection

    def get_url(self):
        return self.url

    def get_collection(self):
        return self.collection
