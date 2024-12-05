import os
from flask import Flask, request, render_template, send_file
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Ensure output folder exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Proxy configuration for Ireland, Netherlands, and US
PROXY_MAP = {
    "Ireland": "http://20.13.148.109:8080",  # Ireland Proxy
    "Netherlands": "http://103.204.129.42:3128",  # Netherlands Proxy
    "US": "http://107.148.42.218:1234",  # US Proxy
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        selected_region = request.form.get("region")  # User-selected region

        if not url:
            return "Error: No URL provided!", 400

        # Determine the proxy based on selected region
        proxy = PROXY_MAP.get(selected_region, PROXY_MAP["Ireland"])  # Default to Ireland

        # Configure yt-dlp with the selected proxy
        options = {
            "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",  # Output filename format
            "format": "bestvideo+bestaudio/best",  # Download best quality
            "proxy": proxy,  # Set proxy for yt-dlp
            "merge_output_format": "mp4",  # Ensure final format is MP4
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",  # Convert to MP4 if necessary
                }
            ],
        }

        try:
            # Download video using yt-dlp
            with YoutubeDL(options) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)

            # Return downloaded file
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"Error downloading video: {str(e)}", 500

    # Render the upload form
    return render_template("form.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)