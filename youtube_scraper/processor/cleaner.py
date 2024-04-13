import os
import re
from langchain_core.documents import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from shared.utils.file import open_or_create


class TextCleaner:

    def __init__(self):
        self.trasactions_dir = "data/transcriptions"
        self.processed_dir = "data/processed"

        nltk.download("punkt")
        nltk.download("stopwords")

        self.stop_word = set(stopwords.words("english"))

    def clean_transcript(self, video_docs: list[Document]) -> list[Document]:
        cleaned_docs: list[Document] = []
        for _, video_doc in enumerate(video_docs):
            text = video_doc.page_content
            video_doc.page_content = self._clean_and_tokenize_text(text)
            cleaned_docs.append(video_doc)

        return cleaned_docs

    def _clean_and_tokenize_text(self, text: str) -> str:
        text = re.sub(r"\d+", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = " ".join(text.split()).lower()
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_word]
        filtered = []
        for word in tokens:
            if word not in self.stop_word:
                filtered.append(word)
        return " ".join(filtered)
