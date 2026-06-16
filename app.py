import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

    if not os.getenv("GEMINI_API_KEY"):
        return jsonify({
            "ok": False,
            "answer": "Server error: GEMINI_API_KEY is not set. Add your Gemini API key in your hosting environment variables."
        }), 500

    try:
        prompt = SYSTEM_INSTRUCTIONS + "\n\nExplain this Python error/code for a beginner:\n\n" + user_text

        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            contents=prompt
        )

        return jsonify({
            "ok": True,
            "answer": response.text
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "answer": f"Something went wrong while asking the AI: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
