import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()

SYSTEM_INSTRUCTIONS = """
You are an AI Python Error Explainer for beginner students.
Explain Python errors in very simple English.
Use this structure:
1. What the error means
2. Why it happened
3. How to fix it
4. Corrected code example if possible
Keep it friendly and not too long.
Never make fun of the user.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return "OK", 200

@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json(silent=True) or {}
    user_text = (data.get("error") or "").strip()

    if not user_text:
        return jsonify({
            "ok": False,
            "answer": "Please paste a Python error or code first."
        }), 400

    if not os.getenv("OPENAI_API_KEY"):
        return jsonify({
            "ok": False,
            "answer": "Server error: OPENAI_API_KEY is not set. Add your API key in your hosting environment variables."
        }), 500

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5.5-mini"),
            instructions=SYSTEM_INSTRUCTIONS,
            input=f"Explain this Python error/code for a beginner:\n\n{user_text}"
        )

        return jsonify({
            "ok": True,
            "answer": response.output_text
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "answer": f"Something went wrong while asking the AI: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
