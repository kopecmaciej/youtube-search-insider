import __init__
import asyncio

from shared.utils.env import get_env
from qdrant_db.client import Qdrant
from ai.open_ai import OpenAIClient
from youtube.search import YoutubeSearcher
from processor.transcript import Transcriptor
from processor.cleaner import TextCleaner
from processor.tokenize import Tokenizer
from shared.amqp.client import RabbitMQClient
from shell.flags import Flags


async def main(rabbitmq_client: RabbitMQClient):
    flags = Flags().parse_args()

    try:
        await rabbitmq_client.connect()
    except Exception as e:
        print(f"Error while connecting to RabbitMQ, err: {e}")
        exit(1)

    transcriptor = Transcriptor(rabbitmq_client)
    text_cleaner = TextCleaner()
    tokenizer = Tokenizer()

    while True:
        search_phrase = flags.search_phrase
        if flags.search_phrases is not None:
            search_phrase = ",".join(flags.search_phrases)

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

        cleaned_transcript = []
        for video in founded_videos_ids:
            try:
                transcript = await transcriptor.transcript_video(
                    video[1], flags.languages
                )
                if transcript is not None:
                    cleaned = text_cleaner.clean_transcript(transcript)
                    cleaned_transcript.extend(cleaned)

            except Exception as e:
                print(f"An error occurred: {e}")
                continue

        try:
            qdrant = Qdrant()
        except Exception as e:
            print(f"Error connecting to Qdrant: {e}")
            exit(1)

        tokenizer.tokenize(cleaned_transcript)

        ## add delay between scraping
        delay = get_env("SCRAPING_DELAY", 15)

        await asyncio.sleep(int(delay))


if __name__ == "__main__":
    rabbitmq_client = RabbitMQClient()
    asyncio.run(main(rabbitmq_client))
