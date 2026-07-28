"""
All app content lives in memory as plain Python data structures.
No database, no external API calls — everything here is static,
hand-written content that ships with the code.
"""

import random

# ---------------------------------------------------------------------------
# Grammar & Fun — fill-in-the-blank and multiple-choice questions
# ---------------------------------------------------------------------------

GRAMMAR_QUESTIONS = [
    {
        "id": "g1",
        "type": "fill_blank",
        "prompt": "She ___ to the market every Sunday morning.",
        "answer": "goes",
        "accepted": ["goes"],
        "explanation": "Use the third-person singular present tense (goes) with 'she'.",
    },
    {
        "id": "g2",
        "type": "mcq",
        "prompt": "Choose the correct sentence:",
        "options": [
            "He don't like coffee.",
            "He doesn't likes coffee.",
            "He doesn't like coffee.",
            "He not like coffee.",
        ],
        "answer": 2,
        "explanation": "With third-person singular subjects, use 'doesn't' + the base verb form: 'doesn't like'.",
    },
    {
        "id": "g3",
        "type": "fill_blank",
        "prompt": "I have ___ my homework already.",
        "answer": "done",
        "accepted": ["done"],
        "explanation": "'Have' pairs with the past participle 'done' to form the present perfect tense.",
    },
    {
        "id": "g4",
        "type": "mcq",
        "prompt": "Which word correctly completes: 'This is the book ___ I told you about'?",
        "options": ["who", "which", "whom", "whose"],
        "answer": 1,
        "explanation": "'Which' refers to things (the book), not people.",
    },
    {
        "id": "g5",
        "type": "fill_blank",
        "prompt": "They ___ been living here since 2019.",
        "answer": "have",
        "accepted": ["have", "have,", "have."],
        "explanation": "'Since 2019' signals the present perfect tense, which needs 'have/has' + past participle.",
    },
    {
        "id": "g6",
        "type": "mcq",
        "prompt": "Pick the correctly punctuated sentence:",
        "options": [
            "Its a beautiful day.",
            "It's a beautiful day.",
            "Its' a beautiful day.",
            "It is' a beautiful day.",
        ],
        "answer": 1,
        "explanation": "\"It's\" is the contraction of 'it is'. 'Its' (no apostrophe) shows possession.",
    },
    {
        "id": "g7",
        "type": "fill_blank",
        "prompt": "If I ___ more time, I would learn another language.",
        "answer": "had",
        "accepted": ["had"],
        "explanation": "The second conditional uses the past simple ('had') in the if-clause for hypothetical situations.",
    },
    {
        "id": "g8",
        "type": "mcq",
        "prompt": "Choose the correct comparative form:",
        "options": [
            "This road is more longer than that one.",
            "This road is longer than that one.",
            "This road is more long than that one.",
            "This road is longest than that one.",
        ],
        "answer": 1,
        "explanation": "Short adjectives like 'long' take the '-er' suffix: 'longer', not 'more longer'.",
    },
]


def get_random_grammar_question():
    return random.choice(GRAMMAR_QUESTIONS)


def check_grammar_answer(question_id: str, submitted):
    question = next((q for q in GRAMMAR_QUESTIONS if q["id"] == question_id), None)
    if not question:
        return None

    if question["type"] == "mcq":
        is_correct = int(submitted) == question["answer"]
    else:
        normalized = str(submitted).strip().lower()
        is_correct = normalized in [a.lower() for a in question["accepted"]]

    return {
        "correct": is_correct,
        "explanation": question["explanation"],
        "correct_answer": (
            question["options"][question["answer"]]
            if question["type"] == "mcq"
            else question["answer"]
        ),
        "correct_answer_index": question["answer"] if question["type"] == "mcq" else None,
    }


# ---------------------------------------------------------------------------
# Reading & Translation — Hindi sentences with reference English translations
# ---------------------------------------------------------------------------

TRANSLATION_SENTENCES = [
    {
        "id": "t1",
        "hindi": "आज सुबह बारिश हो रही थी, इसलिए मैं टहलने नहीं गया।",
        "reference": "It was raining this morning, so I did not go for a walk.",
        "keywords": ["rain", "morning", "walk", "go", "did not", "so"],
    },
    {
        "id": "t2",
        "hindi": "मेरी दादी हर शाम बगीचे में फूलों को पानी देती हैं।",
        "reference": "My grandmother waters the flowers in the garden every evening.",
        "keywords": ["grandmother", "water", "flowers", "garden", "evening"],
    },
    {
        "id": "t3",
        "hindi": "वह परीक्षा की तैयारी के लिए हर दिन पुस्तकालय जाता है।",
        "reference": "He goes to the library every day to prepare for the exam.",
        "keywords": ["library", "every day", "prepare", "exam", "goes"],
    },
    {
        "id": "t4",
        "hindi": "हमने पिछले सप्ताह एक नई फिल्म देखी जो बहुत दिलचस्प थी।",
        "reference": "We watched a new movie last week that was very interesting.",
        "keywords": ["watched", "movie", "last week", "interesting", "new"],
    },
    {
        "id": "t5",
        "hindi": "कृपया मुझे बताएं कि अगली बैठक कब और कहाँ होगी।",
        "reference": "Please tell me when and where the next meeting will be.",
        "keywords": ["tell", "next meeting", "when", "where", "please"],
    },
]


def get_random_translation_sentence():
    return random.choice(TRANSLATION_SENTENCES)


def check_translation(sentence_id: str, submitted: str):
    sentence = next((s for s in TRANSLATION_SENTENCES if s["id"] == sentence_id), None)
    if not sentence:
        return None

    submitted_lower = submitted.lower()
    matched = [kw for kw in sentence["keywords"] if kw.lower() in submitted_lower]
    missed = [kw for kw in sentence["keywords"] if kw.lower() not in submitted_lower]
    coverage = len(matched) / len(sentence["keywords"])

    if coverage >= 0.8:
        verdict = "Great job! Your translation captures the meaning well."
    elif coverage >= 0.5:
        verdict = "Good attempt — you got the main idea, but a few details are missing."
    else:
        verdict = "Keep practicing — try to include more of the key details below."

    return {
        "verdict": verdict,
        "coverage_percent": round(coverage * 100),
        "matched_keywords": matched,
        "missed_keywords": missed,
        "reference": sentence["reference"],
    }


# ---------------------------------------------------------------------------
# Image Comprehension — stable images with hand-written reference descriptions
# ---------------------------------------------------------------------------

IMAGE_PROMPTS = [
    {
        "id": "i1",
        "image_url": "https://picsum.photos/id/1015/960/640",
        "reference_description": (
            "A wide river winds through a valley surrounded by tall green mountains. "
            "The water reflects the cloudy sky, and the landscape feels calm and remote."
        ),
        "keywords": ["river", "mountain", "valley", "water", "sky", "green"],
    },
    {
        "id": "i2",
        "image_url": "https://picsum.photos/id/1043/960/640",
        "reference_description": (
            "A field of purple lavender stretches across the frame under a bright blue sky. "
            "The rows are neat and evenly spaced, suggesting a cultivated farm."
        ),
        "keywords": ["field", "flowers", "purple", "sky", "farm", "rows"],
    },
    {
        "id": "i3",
        "image_url": "https://picsum.photos/id/1074/960/640",
        "reference_description": (
            "A dog stands alone on a dirt path in a dry, grassy landscape. "
            "The mood feels quiet and a little lonely, with warm, muted colors."
        ),
        "keywords": ["dog", "path", "grass", "alone", "landscape"],
    },
    {
        "id": "i4",
        "image_url": "https://picsum.photos/id/1062/960/640",
        "reference_description": (
            "Close-up of a small plant sprouting from cracked, dry soil. "
            "The image highlights texture and contrast between new growth and a harsh environment."
        ),
        "keywords": ["plant", "soil", "grow", "dry", "texture", "close-up"],
    },
]


def get_random_image_prompt():
    return random.choice(IMAGE_PROMPTS)


def check_image_description(image_id: str, submitted: str):
    prompt = next((p for p in IMAGE_PROMPTS if p["id"] == image_id), None)
    if not prompt:
        return None

    words = [w.strip(".,!?").lower() for w in submitted.split() if w.strip(".,!?")]
    word_count = len(words)
    unique_ratio = round(len(set(words)) / word_count, 2) if word_count else 0

    submitted_lower = submitted.lower()
    matched = [kw for kw in prompt["keywords"] if kw.lower() in submitted_lower]
    missed = [kw for kw in prompt["keywords"] if kw.lower() not in submitted_lower]

    feedback = []
    if word_count < 15:
        feedback.append("Try writing a longer description (aim for at least 15-20 words).")
    else:
        feedback.append("Good length — you gave a solidly detailed description.")

    if unique_ratio < 0.6 and word_count > 5:
        feedback.append("Try varying your vocabulary — you're repeating several words.")
    else:
        feedback.append("Nice vocabulary variety.")

    if missed:
        feedback.append(
            "Consider mentioning: " + ", ".join(missed) + "."
        )

    return {
        "word_count": word_count,
        "unique_word_ratio": unique_ratio,
        "matched_keywords": matched,
        "missed_keywords": missed,
        "feedback": feedback,
        "reference_description": prompt["reference_description"],
    }
