import re
import uuid
from youtube_search import YoutubeSearch
import json
import pandas as pd

class YoutubeSearcher:

    def __init__(self, search_phrase: str):
        self.raw_dir = 'data/raw'
        self.search_phrase = search_phrase

    def get_url_ids(self):
        if self.search_phrase is None:
            raise ValueError("search_phrase must be set")

        print("Search phrase: {}".format(self.search_phrase))
        results = YoutubeSearch(self.search_phrase, max_results=20).to_json()
        videos = pd.DataFrame(json.loads(results)['videos'])
        
        videos['views'] = videos['views'].apply(self._process_views)
        videos['duration'] = videos['duration'].apply(self._duration_to_minutes)

        filtered_videos = videos[(videos['duration'] <= 90) & (videos['duration'] >= 5) & (videos['views'] >= 3000)]

        if not isinstance(filtered_videos, pd.DataFrame):
            raise ValueError("videos must be a DataFrame")
        
        if filtered_videos.empty:
            return None

        filtered_videos.loc[:, 'video_id'] = videos['url_suffix'].apply(self._extract_video_id)
        filtered_videos = filtered_videos.dropna(subset=['video_id'])

        for video in filtered_videos.iterrows():
            id = uuid.uuid4().hex
            open(f'{self.raw_dir}/{id}.json', 'w').write(json.dumps(video[1].to_dict()))

        return filtered_videos[['title', 'video_id']].values.tolist()

    def _duration_to_minutes(self, duration):
        parts = list(map(int, duration.split(':')))
        if len(parts) == 3:
            return parts[0] * 60 + parts[1] + parts[2] / 60
        elif len(parts) == 2:
            return parts[0] + parts[1] / 60
        elif len(parts) == 1:
            return parts[0] / 60

    def _extract_video_id(self, url):
        match = re.search(r'(?<=v=)[^&]+', url)
        return match.group(0) if match else None

    def _process_views(self,x):
        x_str = str(x) if pd.notna(x) else ''
        return int(re.sub(r'\D', '', x_str)) if re.search(r'\d', x_str) else 0
