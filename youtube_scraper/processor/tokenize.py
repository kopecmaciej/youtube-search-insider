from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document
from youtube_scraper.qdrant_db.config import QdrantConfig
from youtube_scraper.qdrant_db.langchain import get_langchain_qdrant


class Tokenizer:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 40):
        self.embeddings = SentenceTransformerEmbeddings()
        self.qdrant: Qdrant = get_langchain_qdrant(self.embeddings)
        self.qdrant_config = QdrantConfig()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def tokenize(
        self,
        transcriptions: list[Document],
    ):
        documents = self.split_transcriptions(transcriptions)
        try:
            self.qdrant.from_documents(
                documents=documents,
                embedding=self.embeddings,
                ## Todo: check why this method needs api_key, url and collection_name
                ## while others don't
                api_key=self.qdrant_config.get_api_key(),
                url=self.qdrant_config.get_url(),
                collection_name=self.qdrant_config.get_collection(),
            )
        except Exception as e:
            print(f"Error saving to Qdrant: {e}")
            exit(1)

    def split_transcriptions(self, transcriptions: list[Document]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(transcriptions)
