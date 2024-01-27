from shared.utils.env import get_env

class RabbitMQConfig:

    def __init__(self):
        self.host = get_env("RABBITMQ_HOST", "localhost")
        self.port = get_env("RABBITMQ_PORT", "5672")
        self.user = get_env("RABBITMQ_USER", "guest")
        self.password = get_env("RABBITMQ_PASSWORD", "guest")
        self.queue = get_env("RABBITMQ_QUEUE", "youtube_videos_queue")
        self.exchange = get_env("RABBITMQ_EXCHANGE", "youtube_videos_exchange")

    def get_url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}"

    def get_main_queue(self):
        return self.queue

    def get_main_exchange(self):
        return self.exchange

