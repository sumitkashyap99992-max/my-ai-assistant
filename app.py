from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My AI Assistant</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
                padding: 0;
            }

            .header {
                background: #111827;
                color: white;
                padding: 20px;
                text-align: center;
                font-size: 24px;
            }

            .container {
                max-width: 700px;
                margin: auto;
                padding: 20px;
            }

            #chat {
                background: white;
                min-height: 400px;
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 15px;
                overflow-y: auto;
            }

            .message {
                padding: 12px;
                margin: 10px 0;
                border-radius: 10px;
                white-space: pre-wrap;
            }

            .user {
                background: #2563eb;
                color: white;
                text-align: right;
            }

            .ai {
                background: #e5e7eb;
                color: #111827;
            }

            .input-area {
                display: flex;
                gap: 8px;
            }

            input {
                flex: 1;
                padding: 14px;
                border: 1px solid #ccc;
                border-radius: 10px;
                font-size: 16px;
            }

            button {
                padding: 14px 20px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
            }
        </style>
    </head>

    <body>

        <div class="header">
            🤖 My AI Assistant
        </div>

        <div class="container">

            <div id="chat">
                <div class="message ai">
                    Hello! 👋 I am your AI Assistant. Ask me anything.
                </div>
            </div>

            <div class="input-area">
                <input
                    id="message"
                    type="text"
                    placeholder="Type your message..."
                    onkeydown="if(event.key === 'Enter') sendMessage()"
                >

                <button onclick="sendMessage()">
                    Send
                </button>
            </div>

        </div>

        <script>
            async function sendMessage() {

                const input = document.getElementById("message");
                const chat = document.getElementById("chat");

                const message = input.value.trim();

                if (!message) {
                    return;
                }

                const userMessage = document.createElement("div");
                userMessage.className = "message user";
                userMessage.innerText = message;
                chat.appendChild(userMessage);

                input.value = "";

                const aiMessage = document.createElement("div");
                aiMessage.className = "message ai";
                aiMessage.innerText = "Thinking...";
                chat.appendChild(aiMessage);

                try {

                    const response = await fetch("/chat", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    });

                    const data = await response.json();

                    if (data.reply) {
                        aiMessage.innerText = data.reply;
                    } else {
                        aiMessage.innerText = "Error: " + (data.error || "Unknown error");
                    }

                } catch (error) {

                    aiMessage.innerText =
                        "Could not connect to the AI server.";

                }

                chat.scrollTop = chat.scrollHeight;
            }
        </script>

    </body>
    </html>
    """


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json() or {}

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Message is required"
        }), 400

    if not client:
        return jsonify({
            "error": "OPENAI_API_KEY is not configured"
        }), 500

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
