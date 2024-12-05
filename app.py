import os
from flask import Flask, request, render_template, send_file
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Ensure output folder exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "Error: No URL provided!", 400

        # Use yt-dlp to download the video
        try:
            options = {
                "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",  # Output filename format
                "format": "bestvideo+bestaudio/best",  # Download best quality
            }
            with YoutubeDL(options) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)

            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"Error downloading video: {str(e)}", 500

    # Render the upload form
    return render_template("form.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)