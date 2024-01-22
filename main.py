from sentence_transformers.SentenceTransformer import os
from dotenv import load_dotenv

from qdrant_db.client import Qdrant
from ai.open_ai import OpenAIClient
from youtube.search import YoutubeSearcher
from processor.transcript import transcript_video
from processor.cleaner import TextCleaner
from processor.tokenize import Tokenizer

load_dotenv()

def main():
    search_phrase = OpenAIClient().generate_youtube_topic()

    collection = os.getenv("QDRANT_COLLECTION")
    if collection is None:
        print("QDRANT_COLLECTION is not set")
        exit(1)

    videos = YoutubeSearcher(search_phrase).get_url_ids()
    if videos is None:
        print("No videos found")
        exit(1)

    for video in videos:
        transcript_video(video[0], video[1])

    TextCleaner().clean_files()

    Tokenizer().tokenize(Qdrant())


if __name__ == '__main__':
    main()
