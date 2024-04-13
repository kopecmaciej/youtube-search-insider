from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from sentence_transformers.SentenceTransformer import os


class Tokenizer:
    collection_name = "processed_transcriptions"

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 40):
        self.embeddings = SentenceTransformerEmbeddings()
        self.processed_dir = "data/processed"
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def tokenize(
        self,
        transcriptions: list[Document],
    ):

        documents = self.split_transcriptions(transcriptions)
        try:
            self.qdrant = Qdrant.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                api_key=self.qdrant_api_key,
                url=self.qdrant_url,
            )
        except Exception as e:
            print(f"Error saving to Qdrant: {e}")
            exit(1)

    def split_transcriptions(self, transcriptions: list[Document]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(transcriptions)
