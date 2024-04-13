from langchain_core.documents import Document
import youtube_transcript_api

from langchain_community.document_loaders.youtube import YoutubeLoader
from shared.amqp.client import RabbitMQClient


class Transcriptor:

    def __init__(self, rabbitmq_client: RabbitMQClient):
        self.transcript_dir = "data/transcriptions"
        self.rabbitmq_client = rabbitmq_client

    async def transcript_video(
        self, video_id: str, languages: list[str]
    ) -> list[Document] | None:
        try:
            loader = YoutubeLoader(
                video_id=video_id, language=languages, add_video_info=True
            )
            video_doc = loader.load()
            print(f"Transcripting video {video_id} with languages {languages}")
            return video_doc
        except youtube_transcript_api.NoTranscriptFound:
            print(f"No transcript found for video {video_id}")
            self.rabbitmq_client.send_url_to_queue(video_id)
            return None
        except youtube_transcript_api.TranscriptsDisabled:
            print(f"Transcript disabled for video {video_id}")
            self.rabbitmq_client.send_url_to_queue(video_id)
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
