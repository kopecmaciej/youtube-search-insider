import os
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from qdrant_db.client import Qdrant

class Tokenizer:

    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2', device="cuda")
        self.processed_dir = "data/processed"

    def tokenize(self, client: Qdrant):
        texts = []

        for file in os.listdir(self.processed_dir):
            with open(f"{self.processed_dir}/{file}", "r") as f:
                text = f.read()
                obj = {}
                obj['name'] = file
                obj['text'] = text
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
                    payload={"name": obj['name']},
                    id=i,
                )
                for i, obj in enumerate(texts)
            ],
        )

