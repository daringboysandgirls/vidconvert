from yt_dlp import YoutubeDL

options = {
    "outtmpl": "%(title)s.%(ext)s",
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
}

url = "https://www.youtube.com/watch?v=82g-SWgQNZY"
with YoutubeDL(options) as ydl:
    ydl.download([url])