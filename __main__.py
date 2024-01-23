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
    search_phrase = OpenAIClient().generate_youtube_topic()
    if search_phrase is None:
        print("No search phrase generated")
        exit(1)

    whisper_client = WhisperClient()

    videos = YoutubeSearcher(search_phrase).get_url_ids()
    if videos is None:
        print("No videos found")
        exit(1)

    transcriptor = Transcriptor(rabbitmq_client)
    for video in videos:
      await transcriptor.transcript_video(video[0], video[1])

    TextCleaner().clean_files()

    Tokenizer().tokenize(Qdrant())

    await rabbitmq_client.consume(whisper_client.transcribe_video)

if __name__ == '__main__':
    asyncio.run(main(RabbitMQClient()))
