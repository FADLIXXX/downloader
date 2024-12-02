from flask import Flask, request, jsonify, render_template
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# Helper function to fetch video/audio data using free API
def fetch_tiktok_data(url):
    try:
        # Using SnapTik as an example (replace with a valid free API if needed)
        api_url = f"https://api.snaptik.app/abc?url={url}"  # Replace with actual API endpoint
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "video_url": data.get("video_url"),
                "audio_url": data.get("audio_url"),
                "title": data.get("title", "TikTok Video")
            }
        else:
            return {"status": "error", "message": "Failed to fetch data from API."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    tiktok_url = request.form.get('url')

    if not tiktok_url:
        return jsonify({"status": "error", "message": "URL is required."})

    # Validate the URL
    parsed_url = urlparse(tiktok_url)
    if not parsed_url.netloc.endswith("tiktok.com"):
        return jsonify({"status": "error", "message": "Invalid TikTok URL."})

    # Fetch TikTok data
    result = fetch_tiktok_data(tiktok_url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
