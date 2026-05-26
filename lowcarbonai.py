from flask import Flask, render_template, request
import random

app = Flask(__name__)

QUESTIONS = [
    {
        "id": "daily_prompts",
        "text": "How many AI prompts do you usually send per day?",
        "options": [
            ("0-5", 5),
            ("6-20", 20),
            ("21-50", 45),
            ("50+", 70)
        ],
        "tip": "Try batching questions into one clear prompt instead of sending lots of tiny prompts."
    },
    {
        "id": "image_generation",
        "text": "How often do you generate AI images?",
        "options": [
            ("Never", 0),
            ("Sometimes", 20),
            ("Often", 45),
            ("Every day", 70)
        ],
        "tip": "Use image generation only when needed and avoid repeatedly regenerating small changes."
    },
    {
        "id": "video_ai",
        "text": "Do you use AI video tools?",
        "options": [
            ("Never", 0),
            ("Rarely", 25),
            ("Weekly", 50),
            ("Daily", 80)
        ],
        "tip": "AI video can be resource-heavy. Plan your prompt carefully before generating."
    },
    {
        "id": "regeneration",
        "text": "How often do you regenerate AI answers?",
        "options": [
            ("Almost never", 0),
            ("Once or twice", 15),
            ("Several times", 40),
            ("Until it is perfect", 65)
        ],
        "tip": "Instead of regenerating, refine the answer by saying exactly what you want changed."
    },
    {
        "id": "model_choice",
        "text": "What kind of AI model do you usually choose?",
        "options": [
            ("Small/fast model", 10),
            ("Default model", 25),
            ("Advanced model", 50),
            ("Most powerful model every time", 70)
        ],
        "tip": "Use smaller or faster models for simple tasks like summaries, grammar, and planning."
    },
    {
        "id": "file_uploads",
        "text": "How often do you upload long documents, images, or PDFs to AI?",
        "options": [
            ("Never", 0),
            ("Rarely", 15),
            ("Often", 40),
            ("Very often", 60)
        ],
        "tip": "Upload only the pages or sections you need instead of entire large files."
    },
    {
        "id": "ai_for_school",
        "text": "How much do you use AI for school/work tasks?",
        "options": [
            ("Not much", 5),
            ("A few tasks", 20),
            ("Most tasks", 45),
            ("Almost everything", 65)
        ],
        "tip": "Use AI as a helper, not for every small task. Do quick tasks yourself when possible."
    },
    {
        "id": "prompt_length",
        "text": "How long are your prompts usually?",
        "options": [
            ("Very short", 10),
            ("Clear and medium length", 5),
            ("Long with lots of context", 35),
            ("Huge copy-paste blocks", 60)
        ],
        "tip": "Give focused context. Avoid pasting unnecessary text."
    },
    {
        "id": "chat_sessions",
        "text": "How many separate AI chats do you start in a day?",
        "options": [
            ("1", 5),
            ("2-4", 20),
            ("5-10", 40),
            ("10+", 65)
        ],
        "tip": "Keep related tasks in one chat so the AI does not need repeated context."
    },
    {
        "id": "awareness",
        "text": "Do you think about the environmental impact before using AI?",
        "options": [
            ("Yes, often", 0),
            ("Sometimes", 10),
            ("Rarely", 30),
            ("Never", 50)
        ],
        "tip": "Before using AI, ask: could I search, reuse, or solve this without generating?"
    }
]


def calculate_results(answers):

    total_score = 0
    max_score = 0
    tips = []

    for question in QUESTIONS:

        qid = question["id"]
        value = int(answers.get(qid, 0))

        total_score += value
        max_score += max(option[1] for option in question["options"])

        if value >= 35:
            tips.append(question["tip"])

    percentage = round((total_score / max_score) * 100)

    if percentage <= 10:
        category = "Extremely Low Impact 🌱"
        message = "Your AI usage is very environmentally conscious."

    elif percentage <= 20:
        category = "Low Impact ✅"
        message = "Your AI habits are relatively sustainable."

    elif percentage <= 40:
        category = "Low-Moderate Impact 🍃"
        message = "Your AI usage is moderate but could still improve."

    elif percentage <= 50:
        category = "Moderate Impact ⚡"
        message = "You use AI regularly. Small changes could reduce impact."

    elif percentage <= 60:
        category = "High-Moderate Impact 🌍"
        message = "Your AI habits may be using significant energy."

    elif percentage <= 70:
        category = "High Impact 🔥"
        message = "Your AI usage is environmentally heavy."

    elif percentage <= 80:
        category = "Very High Impact 🚨"
        message = "Your AI usage has a large estimated environmental impact."

    else:
        category = "Extremely High Impact ☠️"
        message = "Your AI usage is extremely resource intensive."

    if not tips:
        tips = [
            "Keep using AI mindfully.",
            "Use smaller models for simple tasks.",
            "Avoid unnecessary regenerations."
        ]

    estimated_energy = round(total_score * 0.002, 3)

    carbon_intensity = 0.4
    embodied_factor = 0.02

    sci_estimate = round(
        (estimated_energy * carbon_intensity) + embodied_factor,
        3
    )

    return {
        "percentage": percentage,
        "category": category,
        "message": message,
        "tips": tips[:5],
        "estimated_energy": estimated_energy,
        "sci_estimate": sci_estimate,
        "total_score": total_score
    }


@app.route("/")
def home():

    shuffled_questions = QUESTIONS.copy()
    random.shuffle(shuffled_questions)

    return render_template(
        "index.html",
        questions=shuffled_questions
    )


@app.route("/results", methods=["POST"])
def results():

    answers = request.form.to_dict()

    result = calculate_results(answers)

    return render_template(
        "results.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)