import re
import youtube_transcript_api
from youtube_search import YoutubeSearch
import json

search_phrase = 'Introduction to large language models, LLM'
video_id = 'zjkBMFhNj_g'
filename = 'transcription.txt'

def get_youtube_ids():
    validated_videos = []
    results = YoutubeSearch(search_phrase, max_results=1000).to_json()
    videos = json.loads(results)
    for video in videos['videos']:
        title, url_suffix = video['title'], video['url_suffix']
        views = int(''.join(filter(str.isdigit, video['views'])))
        duration = video['duration'].split(':')
        mapped = list(map(int, duration))
        total_minutes = 0
        if len(duration) == 3:
            total_minutes += mapped[0] * 60 + mapped[1] + mapped[2] / 60
        elif len(duration) == 2:
            total_minutes += mapped[0] + mapped[1] / 60
        elif len(duration) == 1:
            total_minutes += mapped[0] / 60

        if total_minutes <= 90 and total_minutes >= 5 and views >= 3000:
            video_id = re.search(r'(?<=v=)[^&]+', url_suffix)
            if video_id:
                validated_videos.append([title, video_id.group(0)])

    return validated_videos


def transcript_video(name, video_id):
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

    filename = f"./transcriptions/{name}.txt"
    with open(filename, 'w') as file:
        for entry in transcript_text:
            file.write(f"{entry['text']}\n")



def transcript_examin_video():
    transcript_list = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(video_id)

    transcript = transcript_list.find_transcript(['en'])
    transcript_text = transcript.fetch()

    with open(filename, 'w') as file:
        for entry in transcript_text:
            file.write(f"{entry['text']}\n")

def main():
    videos = get_youtube_ids()
    for video in videos:
        transcript_video(video[0], video[1])

if __name__ == '__main__':
    main()
