import json
import youtube_transcript_api

from shared.amqp.client import RabbitMQClient
from shared.utils.file import write_json


class Transcriptor:

    def __init__(self, rabbitmq_client: RabbitMQClient):
        self.transcript_dir = "data/transcriptions"
        self.rabbitmq_client = rabbitmq_client

    async def transcript_video(self, video_id: str, languages: list[str]) -> str:
        print(f"Transcripting video {video_id} with languages {languages}")
        try:
            transcript_list = (
                youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(video_id)
            )
            transcript = transcript_list.find_transcript(languages)
        except youtube_transcript_api.NoTranscriptFound:
            print(f"No transcript found for video {video_id}")
            self.rabbitmq_client.send_url_to_queue(video_id)
            return ""
        except youtube_transcript_api.TranscriptsDisabled:
            print(f"Transcript disabled for video {video_id}")
            self.rabbitmq_client.send_url_to_queue(video_id)
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

        transcript_text = transcript.fetch()

        text = ""

        for entry in transcript_text:
            entry["text"] = entry["text"].replace("\n", " ")
            text += entry["text"] + " "

        json_data = json.dumps({"text": text}, ensure_ascii=False)

        write_json(json_data, self._file_name(video_id))

        return text

    def _file_name(self, name: str):
        return f"{self.transcript_dir}/{name}.json"
