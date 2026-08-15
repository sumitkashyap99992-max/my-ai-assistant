from flask import Flask, request, jsonify, render_template_string
import os
from openai import OpenAI

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My AI Assistant</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f7fb;
        }

        .header {
            background: #111827;
            color: white;
            padding: 18px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
        }

        .chat {
            max-width: 700px;
            margin: auto;
            padding: 20px;
            min-height: calc(100vh - 140px);
        }

        .welcome {
            text-align: center;
            margin-top: 80px;
            color: #374151;
        }

        .message {
            padding: 12px 15px;
            margin: 12px 0;
            border-radius: 15px;
            max-width: 85%;
            line-height: 1.5;
            white-space: pre-wrap;
        }

        .user {
            background: #2563eb;
            color: white;
            margin-left: auto;
        }

        .assistant {
            background: white;
            color: #111827;
            border: 1px solid #e5e7eb;
        }

        .input-area {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 12px;
            border-top: 1px solid #ddd;
        }

        .input-box {
            max-width: 700px;
            margin: auto;
            display: flex;
            gap: 8px;
        }

        input {
            flex: 1;
            padding: 14px;
            border: 1px solid #ccc;
            border-radius: 12px;
            font-size: 16px;
        }

        button {
            padding: 14px 18px;
            border: none;
            border-radius: 12px;
            background: #2563eb;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:disabled {
            background: #9ca3af;
        }
    </style>
</head>

<body>

<div class="header">
    🤖 My AI Assistant
</div>

<div class="chat" id="chat">
    <div class="welcome" id="welcome">
        <h
