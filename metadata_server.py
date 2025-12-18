from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

metadata = {}

CHUNK_SERVERS = [
    "http://localhost:5001",
    "http://localhost:5002"
]

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.read()  # consume data

    chunk_id = str(uuid.uuid4())
    metadata[file.filename] = {
        "chunk_id": chunk_id,
        "servers": CHUNK_SERVERS
    }
    return jsonify(metadata[file.filename])

@app.route("/download/<filename>")
def download(filename):
    if filename not in metadata:
        return jsonify({"error": "File not found"}), 404
    return jsonify(metadata[filename])

@app.route("/files")
def files():
    return jsonify(list(metadata.keys()))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
