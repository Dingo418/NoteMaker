import yt_dlp
from pathlib import Path
URL = 'https://www.youtube.com/watch?v=rrB13utjYV4'

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{  
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
    'outtmpl': str(Path("./data/temp_audio"))
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URL)