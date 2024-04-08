import uuid
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from qdrant_db.client import Qdrant


class Tokenizer:

    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
        self.processed_dir = "data/processed"

    def tokenize(
        self,
        client: Qdrant,
        names: list[str],
        transcriptions: list[str],
        chunk_size: int = 1000,
    ):

        objects: list[dict[str, str]] = []

        for iter, transcription in enumerate(transcriptions):
            name = names[iter]
            for i in range(0, len(transcription), chunk_size):
                chunk = transcription[i : i + chunk_size]
                obj = {"name": name, "text": chunk}
                objects.append(obj)

        print("Loaded texts {}".format(len(transcriptions)))

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
                    vector=self.encoder.encode(obj["text"]),  # type: ignore
                    payload={"name": obj["name"], "text": obj["text"]},
                    id=str(uuid.uuid4()),
                )
                for _, obj in enumerate(objects)
            ],
        )
