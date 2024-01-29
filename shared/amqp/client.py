import aio_pika
import asyncio

from shared.amqp.config import RabbitMQConfig

class RabbitMQClient:

    def __init__(self):
        self.config = RabbitMQConfig()
        self.url = self.config.get_url()
        self.routing_key = 'processing'

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.config.get_main_queue())
        self.exchange = await self.channel.declare_exchange(self.config.get_main_exchange(), aio_pika.ExchangeType.FANOUT)
        await self.queue.bind(self.exchange)

    def send_url_to_queue(self, url: str) -> None:
        message_body = url.encode()
        message = aio_pika.Message(body=message_body)
        print(f"Sending message to queue: {message_body}")
        asyncio.create_task(self.exchange.publish(message, routing_key=self.routing_key))


    async def consume(self, callback) -> None:
        print("Consuming from {}".format(self.queue.name))
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    callback(message.body.decode())
                    print(f"Message processed, body: {message.body.decode()}")

if __name__ == '__main__':
    rabbitmq_client = RabbitMQClient()
    asyncio.run(rabbitmq_client.connect())
    asyncio.run(rabbitmq_client.consume(print))
