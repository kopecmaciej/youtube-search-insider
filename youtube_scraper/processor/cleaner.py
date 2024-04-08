import os
import re
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

    def clean_transcripts(
        self, transcriptions: list[str], video_ids: list[str]
    ) -> list[str]:
        all_cleaned = []
        for i, transcription in enumerate(transcriptions):
            cleaned = self._clean_and_tokenize_text(transcription)
            all_cleaned.append(cleaned)

            procPath = os.path.join(self.processed_dir, video_ids[i])
            procPath = procPath.replace(".json", ".txt")
            mode = "w" if os.path.exists(procPath) else "x"
            with open_or_create(procPath, mode) as f:
                f.write(cleaned)
                f.close()

        return all_cleaned

    def _clean_and_tokenize_text(self, text):
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
