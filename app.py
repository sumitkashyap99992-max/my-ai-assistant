from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return "🤖 My AI Assistant is running!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    if not client:
        return jsonify({"error": "OPENAI_API_KEY is not configured"}), 500

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=message
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
