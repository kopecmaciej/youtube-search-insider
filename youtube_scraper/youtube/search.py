import re
import json
import pandas as pd
from shared.utils.file import write_json
from youtube_search import YoutubeSearch


class YoutubeSearcher:

    def __init__(self, search_phrase: str):
        self.raw_dir = "data/raw"
        self.search_phrase = search_phrase

    def get_url_ids(self):
        if self.search_phrase is None:
            raise ValueError("search_phrase must be set")

        print("Search phrase: {}".format(self.search_phrase))
        results = YoutubeSearch(self.search_phrase, max_results=20).to_json()
        videos = pd.DataFrame(json.loads(results)["videos"])

        videos["views"] = videos["views"].apply(self._get_views)
        videos["duration"] = videos["duration"].apply(self._duration_to_seconds)

        filtered_videos = videos[
            (videos["duration"] <= 90 * 60)
            & (videos["duration"] >= 5 * 60)
            & (videos["views"] >= 3000)
        ]

        if not isinstance(filtered_videos, pd.DataFrame):
            raise ValueError("videos must be a DataFrame")

        if filtered_videos.empty:
            return None

        for _, test in filtered_videos.iterrows():
            write_json(json.dumps(test.to_dict()), f"{self.raw_dir}/{test['id']}.json")

        return filtered_videos[["title", "id"]].values.tolist()

    def _duration_to_seconds(self, duration):
        if duration is None or type(duration) != str:
            return 0
        ## duration is in the format 'H:MM:SS' or 'MM:SS'
        if len(duration.split(":")) == 2:
            duration = "0:" + duration
        return sum(x * int(t) for x, t in zip([3600, 60, 1], duration.split(":")))

    def _get_views(self, x):
        x_str = str(x) if pd.notna(x) else ""
        return int(re.sub(r"\D", "", x_str)) if re.search(r"\d", x_str) else 0
