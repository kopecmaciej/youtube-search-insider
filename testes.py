import qdrant
from sentence_transformers import SentenceTransformer

client = qdrant.get_client()

collection = "processed_transcripts"

encoder = SentenceTransformer('all-MiniLM-L6-v2', device="cuda")

hits = client.search(
    collection_name=collection,
    query_vector=encoder.encode("What is large language models?").tolist(), #type: ignore
    limit=1,
)

print(hits)


