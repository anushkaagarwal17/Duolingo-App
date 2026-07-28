import os
from flask import Flask, jsonify, request
from flask_cors import CORS

import data

app = Flask(__name__)

# Allow requests from any origin (Vercel, Localhost, Mobile, etc.)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def health_check():
    return jsonify({"status": "healthy", "message": "Duolingo Backend API is running"}), 200


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

# Simple health-check route for root URL
@app.route("/")
def home():
    return jsonify({"status": "healthy", "message": "Duolingo Backend API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
