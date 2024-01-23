import asyncio

from qdrant_db.client import Qdrant
from ai.open_ai import OpenAIClient
from youtube.search import YoutubeSearcher
from processor.transcript import Transcriptor
from processor.cleaner import TextCleaner
from processor.tokenize import Tokenizer
from amqp.client import RabbitMQClient
from ai.whisper import WhisperClient

async def main(rabbitmq_client: RabbitMQClient):
    await rabbitmq_client.connect()

    whisper_client = WhisperClient()
    transcriptor = Transcriptor(rabbitmq_client)
    text_cleaner = TextCleaner()
    tokenizer = Tokenizer()

    run = False
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
        tokenizer.tokenize(Qdrant())

        if not run:
            asyncio.create_task(rabbitmq_client.consume(whisper_client.transcribe_video))
            run = True

        await asyncio.sleep(15)  # Wait 15 seconds before next iteration

if __name__ == '__main__':
    asyncio.run(main(RabbitMQClient()))
