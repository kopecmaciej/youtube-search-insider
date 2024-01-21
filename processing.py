import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
 
nltk.download('punkt')
nltk.download('stopwords')

stop_word = set(stopwords.words('english'))

trDir = 'transcriptions'
procDir = 'processed'

def get_all_transcriptions():
    return os.listdir(trDir)

def clean_and_tokenize_text(text):
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split()).lower()
    tokens = word_tokenize(text)
    print(tokens)
    tokens = [word for word in tokens if word not in stop_word]
    filtered = []
    for word in tokens:
        if word not in stop_word:
            filtered.append(word)
    return ' '.join(filtered)


## Clean files
def clean_files():
    for transcription in get_all_transcriptions():
        trPath = os.path.join(trDir, transcription)

        with open(trPath, 'r') as f:
            data = json.load(f)
            text = data['text']
            cleaned = clean_and_tokenize_text(text)
            f.close()

        procPath = os.path.join(procDir, transcription)
        procPath = procPath.replace('.json', '.txt')
        mode = 'w' if os.path.exists(procPath) else 'x'
        with open(procPath, mode) as f:
            f.write(cleaned)
            f.close()

