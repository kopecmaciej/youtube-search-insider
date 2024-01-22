import whisper
import json

class WhisperClient:

    def __init__(self):
        self.model = whisper.load_model("small")
        self.transcriptios_dir = 'transcriptions'

    def transcribe_video(self, video_path):
        result = self.model.transcribe(video_path)

        result_json = json.dumps(result, ensure_ascii=False)

        video_path = video_path.split('/')[-1].split('.')[0]

        path = f"{self.transcriptios_dir}/{video_path}.json"

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
