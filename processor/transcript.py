from youtube_search import json
import youtube_transcript_api

class Transcriptor:

    def __init__(self):
        self.transcript_dir = 'data/transcriptions'

    def transcript_video(self, name, video_id):
        transcript_list = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            transcript_list = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['en'])
        except youtube_transcript_api.NoTranscriptFound:
            print(f"No English transcript found for video {video_id}")
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

    def _file_name(self, name):
        return f"{self.transcript_dir}/{name}.json"

