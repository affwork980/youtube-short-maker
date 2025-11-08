from flask import Flask, request, send_file, jsonify
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os, uuid

app = Flask(__name__)

@app.route("/short", methods=["POST"])
def make_short():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "Missing YouTube URL"}), 400

        os.makedirs("temp", exist_ok=True)

        file_id = str(uuid.uuid4())
        file_path = f"temp/{file_id}.mp4"
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
        stream.download(filename=file_path)

        clip = VideoFileClip(file_path).subclip(0, 60)
        short_path = f"temp/{file_id}_short.mp4"
        clip.write_videofile(short_path, codec="libx264")

        return send_file(short_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
