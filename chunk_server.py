from flask import Flask, request, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

SERVER_NAME = os.environ.get("SERVER_NAME", "server1")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE = os.path.join(BASE_DIR, "chunks", SERVER_NAME)

os.makedirs(STORAGE, exist_ok=True)

@app.route("/store/<chunk_id>", methods=["POST"])
def store(chunk_id):
    with open(os.path.join(STORAGE, chunk_id), "wb") as f:
        f.write(request.data)
    return "Stored"

@app.route("/read/<chunk_id>")
def read(chunk_id):
    path = os.path.join(STORAGE, chunk_id)
    if not os.path.exists(path):
        return "Missing", 404
    return send_file(path)

if __name__ == "__main__":
    port = 5001 if SERVER_NAME == "server1" else 5002
    app.run(port=port, debug=True)
