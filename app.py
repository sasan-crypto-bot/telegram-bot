
import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SECRET = os.environ["WEBHOOK_SECRET"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


@app.get("/")
def home():
    return "Telegram bot is running!"


@app.post("/webhook")
def webhook():
    if request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    ) != SECRET:
        abort(403)

    data = request.get_json(silent=True) or {}
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id:
        return "OK", 200

    if text == "/start":
        reply = "سلام! ربات فعال است. هر پیامی بفرستی، برمی‌گردانم."
    elif text.startswith("/"):
        reply = "این دستور را هنوز نمی‌شناسم."
    else:
        reply = text or "لطفاً یک پیام متنی بفرست."

    response = requests.post(
        f"{BASE_URL}/sendMessage",
        json={"chat_id": chat_id, "text": reply},
        timeout=10,
    )
    response.raise_for_status()

    return "OK", 200


def setup_webhook():
    url = os.environ.get("RENDER_EXTERNAL_URL")
    if not url:
        raise RuntimeError("Render URL is missing")

    response = requests.post(
        f"{BASE_URL}/setWebhook",
        json={
            "url": f"{url}/webhook",
            "secret_token": SECRET,
        },
        timeout=20,
    )
    response.raise_for_status()
    print("Webhook configured")


setup_webhook()
