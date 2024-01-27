import os
import whisper
import json

import processor.download as download

class WhisperClient:

    def __init__(self):
        self.transcriptios_dir = 'data/transcriptions'
        self.video_dir = 'data/videos'

    def transcribe_video(self, video_id):
        print(f"Transcribing video {video_id}")

        video_path = f"{self.video_dir}/{video_id}.mp3"

        file = os.path.isfile(video_path)
        if not file:
            print(f"File {video_path} not found, downloading audio")
            download.download_youtube_audio(video_id)

        self.model = whisper.load_model("small")
        result = self.model.transcribe(f"{self.video_dir}/{video_id}.mp3")

        result_json = json.dumps(result, ensure_ascii=False)

        video_id = video_id.split('/')[-1].split('.')[0]

        path = f"{self.transcriptios_dir}/{video_id}.json"

        print(f"Saving transcription to {path}")

        with open(path, 'w') as f:
            f.write(result_json)


if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) != 2:
        print("Usage: python3 whisper.py <video_path>")
        exit(1)

    client = WhisperClient()
    client.transcribe_video(args[1])
