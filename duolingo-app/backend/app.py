import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import data

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

app = Flask(__name__, static_folder=FRONTEND_DIST, static_url_path="")

# Configure CORS origins via environment variable `ALLOWED_ORIGINS`.
# Format: comma-separated origins, e.g. https://frontend.vercel.app,https://backend.onrender.com
allowed = os.environ.get("ALLOWED_ORIGINS")
if allowed:
    origins = [o.strip() for o in allowed.split(",") if o.strip()]
else:
    # sensible defaults for local dev (Vite default port)
    origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

CORS(app, origins=origins)


# ---------------------------------------------------------------------------
# Grammar & Fun
# ---------------------------------------------------------------------------

@app.route("/api/grammar/question", methods=["GET"])
def grammar_question():
    q = data.get_random_grammar_question()
    # Don't leak the answer/explanation to the client before they submit.
    safe = {k: v for k, v in q.items() if k not in ("answer", "explanation", "accepted")}
    return jsonify(safe)


@app.route("/api/grammar/check", methods=["POST"])
def grammar_check():
    body = request.get_json(force=True) or {}
    result = data.check_grammar_answer(body.get("question_id"), body.get("answer"))
    if result is None:
        return jsonify({"error": "Unknown question_id"}), 400
    return jsonify(result)


# ---------------------------------------------------------------------------
# Reading & Translation
# ---------------------------------------------------------------------------

@app.route("/api/translation/sentence", methods=["GET"])
def translation_sentence():
    s = data.get_random_translation_sentence()
    return jsonify({"id": s["id"], "hindi": s["hindi"]})


@app.route("/api/translation/check", methods=["POST"])
def translation_check():
    body = request.get_json(force=True) or {}
    result = data.check_translation(body.get("sentence_id"), body.get("translation", ""))
    if result is None:
        return jsonify({"error": "Unknown sentence_id"}), 400
    return jsonify(result)


# ---------------------------------------------------------------------------
# Image Comprehension
# ---------------------------------------------------------------------------

@app.route("/api/image/prompt", methods=["GET"])
def image_prompt():
    p = data.get_random_image_prompt()
    return jsonify({"id": p["id"], "image_url": p["image_url"]})


@app.route("/api/image/check", methods=["POST"])
def image_check():
    body = request.get_json(force=True) or {}
    result = data.check_image_description(body.get("image_id"), body.get("description", ""))
    if result is None:
        return jsonify({"error": "Unknown image_id"}), 400
    return jsonify(result)


# ---------------------------------------------------------------------------
# Serve the built React frontend for every non-API route
# ---------------------------------------------------------------------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    # If the frontend `dist` directory isn't present (we're deploying frontend separately),
    # don't attempt to serve static files from here.
    index_path = os.path.join(app.static_folder, "index.html")
    if not os.path.isdir(app.static_folder) or not os.path.exists(index_path):
        return jsonify({"error": "Frontend not served from backend"}), 404

    full_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
