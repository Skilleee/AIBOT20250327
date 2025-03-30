
import shutil
import os
import requests

def backup_file(filepath: str):
    backup_path = filepath + ".bak"
    shutil.copy(filepath, backup_path)

def send_telegram_message(message: str, token: str, chat_id: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Telegram-meddelande misslyckades: {e}")
