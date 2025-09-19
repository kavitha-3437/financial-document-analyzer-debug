import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from tasks import analyze_document_task
from models import init_db
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

# Initialize DB tables (safe noop if exist)
init_db()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/analyze", methods=["POST"])
def analyze():
    payload = request.get_json(force=True, silent=True) or {}
    document_b64 = payload.get("document_base64")
    metadata = payload.get("metadata", {})
    if not document_b64:
        return jsonify({"error": "document_base64 is required (base64-encoded PDF)"}), 400

    # Submit to Celery task queue
    task = analyze_document_task.delay(document_b64, metadata)
    return jsonify({"task_id": task.id, "status": "queued"}), 202

@app.route("/status/<task_id>", methods=["GET"])
def status(task_id):
    from celery.result import AsyncResult
    res = AsyncResult(task_id)
    return jsonify({"id": res.id, "state": res.state, "result": res.result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
 
