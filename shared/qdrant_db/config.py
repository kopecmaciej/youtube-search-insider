import os


class QdrantConfig:
    def __init__(self):
        url = os.getenv("QDRANT_URL")
        if url is None:
            raise Exception("QDRANT_URL is not set")
        self.url = url
        api_key = os.getenv("QDRANT_API_KEY")
        if api_key is None:
            raise Exception("QDRANT_API_KEY is not set")
        self.api_key = api_key
        collection = os.getenv("QDRANT_COLLECTION_NAME")
        if collection is None:
            raise Exception("QDRANT_COLLECTION is not set")
        self.collection = collection

    def get_url(self):
        return self.url

    def get_api_key(self):
        return self.api_key

    def get_collection(self):
        return self.collection
