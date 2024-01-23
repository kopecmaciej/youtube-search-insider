import aio_pika
import asyncio

from amqp.config import RabbitMQConfig

class RabbitMQClient:

    def __init__(self):
        self.config = RabbitMQConfig()
        self.url = self.config.get_url()

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        ## declare queue
        ## declare exchange
        ## bind queue to exchange
        await self.channel.declare_queue(self.config.get_main_queue())
        self.exchange = await self.channel.declare_exchange(self.config.get_main_queue(), aio_pika.ExchangeType.FANOUT)

    async def send_url_to_queue(self, url: str) -> None:
        message_body = url.encode()
        message = aio_pika.Message(body=message_body)
        await self.exchange.publish(message, routing_key='')

        print(f"Sent URL to 'transcription_processing' queue: {url}")

    async def consume(self, callback) -> None:

        print("Consuming from {}".format(self.config.get_main_queue()))

        queue = await self.channel.declare_queue(self.config.get_main_queue())

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    callback(message.body.decode())

if __name__ == '__main__':
    rabbitmq_client = RabbitMQClient()
    asyncio.run(rabbitmq_client.connect())
    asyncio.run(rabbitmq_client.consume(print))
