from flask import Flask, render_template, jsonify
import requests
import random

app = Flask(__name__)

IMGFLIP_URL = "https://api.imgflip.com/get_memes"

def get_memes():
    response = requests.get(IMGFLIP_URL, timeout=10)
    data = response.json()
    return data["data"]["memes"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/meme")
def random_meme():
    memes = get_memes()
    meme = random.choice(memes)
    return jsonify({
        "name" : meme["name"],
        "url"  : meme["url"]
    })

@app.route("/health")
def health():
    return jsonify({
        "status" : "200 ok",
        "messagge" : "Service is Healhty"
    }), 200

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host=host, port=port, debug=debug)
