import os
import whisper
import json

import youtube.download as download

class WhisperClient:

    def __init__(self):
        self.model = whisper.load_model("small")
        self.transcriptios_dir = 'transcriptions'

    def transcribe_video(self, video_path):
        print(f"Transcribing video {video_path}")

        file = os.path.isfile(video_path)
        if not file:
            print(f"File {video_path} does not exist")
            download.download_youtube_audio(video_path)

        result = self.model.transcribe(video_path)

        result_json = json.dumps(result, ensure_ascii=False)

        video_path = video_path.split('/')[-1].split('.')[0]

        path = f"{self.transcriptios_dir}/{video_path}.json"

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
