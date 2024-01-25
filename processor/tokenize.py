import os
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from qdrant_db.client import Qdrant

class Tokenizer:

    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2', device="cuda")
        self.processed_dir = "data/processed"

    def tokenize(self, client: Qdrant, chunk_size: int = 1000):
        texts = []

        for file in os.listdir(self.processed_dir):
            with open(f"{self.processed_dir}/{file}", "r") as f:
                text = f.read()
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i+chunk_size]
                    obj = {'name': file, 'text': chunk}
                    texts.append(obj)

        print("Loaded texts {}".format(len(texts)))

        try:
            coll = client.get_collection()
            if coll is None:
                print("Collection does not exist")
                raise Exception()
        except:
            print("Creating collection")
            client.create_collection(self.encoder.get_sentence_embedding_dimension())

        client.upload_points(
            points=[
                PointStruct(
                    vector=self.encoder.encode(obj['text']), #type: ignore
                    payload={"name": self._remove_extension(obj['name'])},
                    id=i,
                )
                for i, obj in enumerate(texts)
            ],
        )


    def _remove_extension(self, name):
        return name.split(".")[0]
