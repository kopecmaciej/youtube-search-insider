import re
import uuid
from youtube_search import YoutubeSearch
import json
import pandas as pd

raw_dir = 'raw'

def get_youtube_ids(search_phrase):
    results = YoutubeSearch(search_phrase, max_results=10).to_json()
    videos = pd.DataFrame(json.loads(results)['videos'])
    
    videos['views'] = videos['views'].apply(lambda x: int(re.sub(r'\D', '', x)))

    def duration_to_minutes(duration):
        parts = list(map(int, duration.split(':')))
        if len(parts) == 3:
            return parts[0] * 60 + parts[1] + parts[2] / 60
        elif len(parts) == 2:
            return parts[0] + parts[1] / 60
        elif len(parts) == 1:
            return parts[0] / 60

    videos['duration'] = videos['duration'].apply(duration_to_minutes)

    validated_videos = pd.DataFrame()

    if ((videos['duration'] <= 90) & (videos['duration'] >= 5) & (videos['views'] >= 3000)).any():
        def extract_video_id(url):
            match = re.search(r'(?<=v=)[^&]+', url)
            return match.group(0) if match else None

        videos['video_id'] = videos['url_suffix'].apply(extract_video_id)
        filtered_videos = videos.dropna(subset=['video_id'])
        validated_videos = filtered_videos

    for video in validated_videos:
        id = uuid.uuid4().hex
        open(f'{raw_dir}/{id}.json', 'w').write(json.dumps(video))

    return validated_videos[['title', 'video_id']].values.tolist()


