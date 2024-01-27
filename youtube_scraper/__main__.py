import asyncio
import __init__

from utils.env import get_env
from qdrant_db.client import Qdrant
from ai.open_ai import OpenAIClient
from youtube.search import YoutubeSearcher
from processor.transcript import Transcriptor
from processor.cleaner import TextCleaner
from processor.tokenize import Tokenizer
from amqp.client import RabbitMQClient

async def main(rabbitmq_client: RabbitMQClient):
    try:
        await rabbitmq_client.connect()
    except Exception as e:
        print(f"Error while connecting to RabbitMQ, err: {e}")
        exit(1)

    transcriptor = Transcriptor(rabbitmq_client)
    text_cleaner = TextCleaner()
    tokenizer = Tokenizer()

    while True:
        search_phrase = OpenAIClient().generate_youtube_topic()
        if search_phrase is None:
            print("No search phrase generated")
            exit(1)

        videos = YoutubeSearcher(search_phrase).get_url_ids()
        if videos is None:
            print("No videos found")
            continue

        for video in videos:
            try:
                await transcriptor.transcript_video(video[0], video[1])
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

        text_cleaner.clean_files()
        try:
            qdrant = Qdrant()
        except Exception as e:
            print(f"Error connecting to Qdrant: {e}")
            exit(1)
        
        tokenizer.tokenize(qdrant)

        ## add delay between scraping
        delay = get_env('SCRAPING_DELAY', 15)

        await asyncio.sleep(int(delay))

if __name__ == '__main__':
    rabbitmq_client = RabbitMQClient()
    asyncio.run(main(rabbitmq_client))

