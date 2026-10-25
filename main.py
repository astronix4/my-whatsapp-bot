import os
import requests
from flask import Flask, request
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]
WA_TOKEN = os.environ["WA_TOKEN"]
PHONE_ID = os.environ["PHONE_ID"]


@app.route("/")
def home():
    return "Bot is running"


@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive():
    data = request.get_json()
    try:
        value = data["entry"][0]["changes"][0]["value"]
        if "messages" in value:
            msg = value["messages"][0]
            if msg.get("type") == "text":
                sender = msg["from"]
                text = msg["text"]["body"]
                prompt = f"You are a helpful assistant. Reply to this WhatsApp message shortly: {text}"
                reply = model.generate_content(prompt).text
                requests.post(
                    f"https://graph.facebook.com/v21.0/{PHONE_ID}/messages",
                    headers={"Authorization": f"Bearer {WA_TOKEN}"},
                    json={
                        "messaging_product": "whatsapp",
                        "to": sender,
                        "text": {"body": reply},
                    },
                    timeout=30,
                )
    except Exception as e:
        print(f"Error: {e}")
    return "ok", 200
