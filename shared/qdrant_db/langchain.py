from langchain_community.vectorstores.qdrant import Qdrant
from shared.qdrant_db.client import Qdrant as QdrantClient
from langchain_core.embeddings import Embeddings


def get_langchain_qdrant(embeddings: Embeddings) -> Qdrant:
    client = QdrantClient()
    return Qdrant(
        client=client.get_client(),
        embeddings=embeddings,
        collection_name=client.get_collection_name(),
    )
