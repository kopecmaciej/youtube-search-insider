from fetcher import get_youtube_ids
from transcriptor import transcript_video
import tokenizer
import qdrant
import processing
import topic_generator
from dotenv import load_dotenv

load_dotenv()

search_phrase = topic_generator.generate_youtube_topic()

def main():
    client = qdrant.get_client()
    collection = "processed_transcripts"

    videos = get_youtube_ids(search_phrase)
    for video in videos:
        transcript_video(video[0], video[1])

    processing.clean_files()

    tokenizer.tokenize(client, collection)


if __name__ == '__main__':
    main()
