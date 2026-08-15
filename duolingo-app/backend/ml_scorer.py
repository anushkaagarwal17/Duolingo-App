"""
Lightweight ML-based answer scoring using TF-IDF vectorization + cosine similarity.

No API calls, no external model downloads, no API keys — pure scikit-learn.
Installs in seconds and deploys on any free-tier host (Render, Railway, etc.)
with zero added memory/build cost.

This replaces plain keyword-matching with vector-based similarity, so answers
that are phrased differently but mean the same thing still score as correct
(e.g. "the cat sleeps on the mat" vs "a cat is sleeping on the mat").
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def similarity_score(text_a: str, text_b: str) -> float:
    """Returns a 0.0-1.0 similarity score between two pieces of text."""
    if not text_a or not text_b:
        return 0.0
    try:
        vectorizer = TfidfVectorizer().fit([text_a, text_b])
        vectors = vectorizer.transform([text_a, text_b])
        return round(float(cosine_similarity(vectors[0], vectors[1])[0][0]), 3)
    except ValueError:
        # Happens if both strings are empty after stopword removal
        return 0.0


def grade_open_response(submitted: str, keywords: list, min_words: int = 10) -> dict:
    """
    Scores an open-ended answer (translation or image description) against
    a reference built from the expected keywords, using TF-IDF similarity
    instead of simple substring keyword matching.
    """
    reference_text = " ".join(keywords)
    score = similarity_score(submitted, reference_text)

    words = [w.strip(".,!?").lower() for w in submitted.split() if w.strip(".,!?")]
    word_count = len(words)

    matched = [kw for kw in keywords if kw.lower() in submitted.lower()]
    missed = [kw for kw in keywords if kw.lower() not in submitted.lower()]

    if score >= 0.35 and word_count >= min_words:
        verdict = "Great job! Your response captures the meaning well."
    elif score >= 0.15:
        verdict = "Good attempt — you got part of the idea, but some details are missing."
    else:
        verdict = "Keep practicing — try to include more of the key details below."

    return {
        "similarity_score": score,
        "word_count": word_count,
        "matched_keywords": matched,
        "missed_keywords": missed,
        "verdict": verdict,
    }
