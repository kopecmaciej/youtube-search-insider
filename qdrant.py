import os
from qdrant_client import QdrantClient


def get_client():
    host = os.getenv("QDRANT_HOST")
    port = os.getenv("QDRANT_PORT")

    if not host or not port:
        raise Exception("QDRANT_HOST and QDRANT_PORT environment variables should be set")

    client = QdrantClient(host=host, port=int(port))
    return client
