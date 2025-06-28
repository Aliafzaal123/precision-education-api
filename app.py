
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    essay = data.get("essay", "")
    learning_style = data.get("style", "")

    prompt = f"""
    A student wrote this essay:\n"{essay}"\n
    and said their learning style is: "{learning_style}".

    Based on this, suggest a personalized curriculum focusing on:
    1. Language skill development (grammar, writing, reading)
    2. Learning techniques suited to their style
    3. Daily study plan

    Reply in structured JSON:
    {
      "language_focus": "...",
      "learning_techniques": "...",
      "daily_plan": "..."
    }
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    try:
        return jsonify(eval(content))
    except Exception:
        return jsonify({"error": "AI response parsing failed", "raw": content}), 400

if __name__ == "__main__":
    app.run()
