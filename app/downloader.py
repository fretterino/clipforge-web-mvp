from pathlib import Path
import yt_dlp

def download_video(url: str, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    opts = {
        "outtmpl": str(output),
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])