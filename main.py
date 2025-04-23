from flask import Flask, request
import requests
import os

app = Flask(__name__)

INSTANCE_ID = os.environ.get("INSTANCE_ID")
TOKEN = os.environ.get("TOKEN")
ONESTREAM_API_KEY = os.environ.get("ONESTREAM_API_KEY")

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'messages' in data:
        for message in data['messages']:
            if 'text' in message:
                video_url = message['text']['body']
                start_live_stream(video_url)

    return 'OK', 200

def start_live_stream(video_url):
    url = "https://api.onestream.live/api/v2/stream"

    headers = {
        "Authorization": f"Bearer {ONESTREAM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "streamUrl": video_url,
        "title": "Live from WhatsApp Bot",
        "platforms": ["facebook"]
    }

    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
