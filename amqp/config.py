from utils.env import get_env

class RabbitMQConfig:

    def __init__(self):
        self.host = get_env("RABBITMQ_HOST", "localhost")
        self.port = get_env("RABBITMQ_PORT", "5672")
        self.username = get_env("RABBITMQ_USERNAME", "guest")
        self.password = get_env("RABBITMQ_PASSWORD", "guest")
        self.queue = get_env("RABBITMQ_QUEUE", "youtube_videos")

    def get_url(self):
        return f"amqp://{self.username}:{self.password}@{self.host}"

    def get_main_queue(self):
        return self.queue

