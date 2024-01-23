import asyncio

from youtube_search import json
import youtube_transcript_api

from amqp.client import RabbitMQClient

class Transcriptor:

    def __init__(self, rabbitmq_client: RabbitMQClient):
        self.transcript_dir = 'data/transcriptions'
        self.rabbitmq_client = rabbitmq_client

    async def transcript_video(self, name: str, video_id: str):
        transcript_list = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            transcript_list = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['en'])
        except youtube_transcript_api.NoTranscriptFound:
            print(f"No English transcript found for video {video_id}")
            await self.rabbitmq_client.send_url_to_queue(video_id)
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return

        transcript_text = transcript.fetch()

        text = ''

        for entry in transcript_text:
            entry['text'] = entry['text'].replace('\n', ' ')
            text += entry['text'] + ' '

        json_data = json.dumps({'text': text}, ensure_ascii=False)

        with open(self._file_name(name), 'w') as file:
            file.write(json_data)

    def _file_name(self, name: str):
        return f"{self.transcript_dir}/{name}.json"

