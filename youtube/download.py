import yt_dlp as youtube_dl

video_dir = "data/videos"

def download_youtube_audio(video_id):
    print(f"Downloading audio for video {video_id}")

    yotube_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'outtmpl': f"{video_dir}/{video_id}",
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yotube_url])
    except Exception as e:
        print(f"An error occurred: {e}")
        return

