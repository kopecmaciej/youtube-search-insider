import __init__
import asyncio
import argparse

from shared.utils.env import get_env
from qdrant_db.client import Qdrant
from ai.open_ai import OpenAIClient
from youtube.search import YoutubeSearcher
from processor.transcript import Transcriptor
from processor.cleaner import TextCleaner
from processor.tokenize import Tokenizer
from shared.amqp.client import RabbitMQClient


async def main(rabbitmq_client: RabbitMQClient):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search_phrase", type=str, required=False)
    args = parser.parse_args()

    search_phrase = args.search_phrase

    try:
        await rabbitmq_client.connect()
    except Exception as e:
        print(f"Error while connecting to RabbitMQ, err: {e}")
        exit(1)

    transcriptor = Transcriptor(rabbitmq_client)
    text_cleaner = TextCleaner()
    tokenizer = Tokenizer()

    while True:
        if search_phrase is None:
            search_phrase = OpenAIClient().generate_youtube_topic()
            if search_phrase is None:
                print("No search phrase generated")
                exit(1)

        search_phrases = search_phrase.split(",")

        founded_videos_ids = []
        for search_phrase in search_phrases:
            videos_ids = YoutubeSearcher(search_phrase).get_url_ids()
            if videos_ids is None or len(videos_ids) == 0:
                print("No videos found for search phrase: {}".format(search_phrase))
                continue
            founded_videos_ids.extend(videos_ids)

        for video in founded_videos_ids:
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
        delay = get_env("SCRAPING_DELAY", 15)

        await asyncio.sleep(int(delay))


if __name__ == "__main__":
    rabbitmq_client = RabbitMQClient()
    asyncio.run(main(rabbitmq_client))
