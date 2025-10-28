import os
import json
from datetime import datetime
import requests
import sys

# ENV vars (setear en GitHub Secrets)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Rutas
VALUE_FILE = "value.json"

def load_value(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_value(path, payload):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("No TELEGRAM_TOKEN or TELEGRAM_CHAT_ID set — skipping Telegram notification.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        r = requests.post(url, data=data, timeout=10)
        r.raise_for_status()
        print("Telegram sent.")
    except Exception as e:
        print("Telegram error:", e)

def main():
    if not os.path.exists(VALUE_FILE):
        print(f"{VALUE_FILE} not found. Creating initial.")
        payload = {"date": datetime.utcnow().strftime("%Y-%m-%d"), "value": 0}
        save_value(VALUE_FILE, payload)
        return

    payload = load_value(VALUE_FILE)
    old_value = int(payload.get("value", 0))
    new_value = old_value + 1
    today = datetime.utcnow().strftime("%Y-%m-%d")

    new_payload = {
        "date": today,
        "value": new_value
    }

    save_value(VALUE_FILE, new_payload)

    msg = f"Incrementer Bot:\nFecha anterior: {payload.get('date')} -> {old_value}\nNuevo valor ({today}): {new_value}"
    print(msg)
    send_telegram(msg)

if __name__ == "__main__":
    main()
