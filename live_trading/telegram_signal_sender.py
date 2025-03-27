import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="telegram_signal_sender.log", level=logging.INFO)


def send_telegram_signal(message, bot_token, chat_id):
    """
    Skickar en köp-/sälj-rekommendation till Telegram.
    """
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=data)
        logging.info("✅ Signal skickad till Telegram.")
        return response.json()
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av Telegram-signal: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    bot_token = "DIN_TELEGRAM_BOT_TOKEN"
    chat_id = "DIN_CHAT_ID"
    message = "📢 Köp-signal: Tesla har brutit 200-dagars medelvärde och har positivt momentum."

    send_telegram_signal(message, bot_token, chat_id)
