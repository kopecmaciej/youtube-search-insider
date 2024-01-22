import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

class TextCleaner:

    def __init__(self):
        self.trasactions_dir = 'data/transcriptions'
        self.processed_dir = 'data/processed'

        nltk.download('punkt')
        nltk.download('stopwords')

        self.stop_word = set(stopwords.words('english'))

    def clean_files(self):
        for transcription in self._get_all_transcriptions():
            trPath = os.path.join(self.trasactions_dir, transcription)

            with open(trPath, 'r') as f:
                data = json.load(f)
                text = data['text']
                cleaned = self._clean_and_tokenize_text(text)
                f.close()

            procPath = os.path.join(self.processed_dir, transcription)
            procPath = procPath.replace('.json', '.txt')
            mode = 'w' if os.path.exists(procPath) else 'x'
            with open(procPath, mode) as f:
                f.write(cleaned)
                f.close()


    def _clean_and_tokenize_text(self, text):
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = ' '.join(text.split()).lower()
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_word]
        filtered = []
        for word in tokens:
            if word not in self.stop_word:
                filtered.append(word)
        return ' '.join(filtered)

    def _get_all_transcriptions(self):
        return os.listdir(self.trasactions_dir)

