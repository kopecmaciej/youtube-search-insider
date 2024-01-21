import whisper
import json

transcriptios_dir='transcriptions'

def transcribe_video(video_path):
    model = whisper.load_model("small")

    result = model.transcribe(video_path)

    result_json = json.dumps(result, ensure_ascii=False)

    video_path = video_path.split('/')[-1].split('.')[0]

    path = f"{transcriptios_dir}/{video_path}.json"

    with open(path, 'w') as f:
        f.write(result_json)


transcribe_video('videos/PairofSilkStockings.mp3')
