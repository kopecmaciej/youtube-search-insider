import asyncio
import __init__

from shared.amqp.client import RabbitMQClient
from processor.whisper import WhisperClient

async def main(rabbitmq_client: RabbitMQClient):
    try:
        await rabbitmq_client.connect()
    except Exception as e:
        print(f"Error while connecting to RabbitMQ, err: {e}")
        exit(1)

    whisper = WhisperClient()

    await rabbitmq_client.consume(whisper.transcribe_video)


if __name__ == '__main__':
    rabbitmq_client = RabbitMQClient()
    asyncio.run(main(rabbitmq_client))

