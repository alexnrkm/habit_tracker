from fastapi import FastAPI, Request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api = FastAPI()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def get_webhook_update(update: dict) -> dict | None:
    return update


def get_ngrok_url():
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    data = response.json()

    for tunnel in data["tunnels"]:
        public_url = tunnel["public_url"]
        if public_url.startswith("https://"):
            return public_url

    return None


@api.post("/webhook")
async def telegram_webhook(request: Request):
    update = await request.json()
    print(update)
    get_webhook_update(update)
    return {"ok": True}


def setup_webhook ():
    info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(info_url)
    LIVE_WEBHOOK_URL = f"{get_ngrok_url()}/webhook"
    LAST_WEBHOOK_URL = response.json().get("result", {}).get("url")

    if not LAST_WEBHOOK_URL:
        print("Webhook is empty")
        setup_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        response = requests.post(setup_url, json={"url": LIVE_WEBHOOK_URL})
        if response.json().get("result") == True:
            print(f"The webhook is active {LIVE_WEBHOOK_URL}")

    elif LAST_WEBHOOK_URL != LIVE_WEBHOOK_URL:
        delete_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
        response = requests.post(delete_url)
        if response.json().get("result") == True:
            print("Webhook was timed out and deleted")

        setup_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        response = requests.post(setup_url, json={"url": LIVE_WEBHOOK_URL})
        if response.json().get("result") == True:
            print(f"The webhook is active {LIVE_WEBHOOK_URL}")
    
    elif LAST_WEBHOOK_URL == LIVE_WEBHOOK_URL:
        print(f"The webhook is active {LIVE_WEBHOOK_URL}")
    



setup_webhook()