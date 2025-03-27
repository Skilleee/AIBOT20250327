import os
from dotenv import load_dotenv

# Ladda .env-filen automatiskt
load_dotenv()

# === Telegram ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === Google Sheets (Base64 JSON-sträng om du kör så) ===
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")

# === Alpha Vantage ===
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# === OpenAI (valfritt) ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Validering av obligatoriska variabler ===
required_keys = {
    "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
    "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
    "ALPHA_VANTAGE_API_KEY": ALPHA_VANTAGE_API_KEY,
}

missing = [key for key, value in required_keys.items() if not value]
if missing:
    raise ValueError(f"❌ Saknade miljövariabler i .env: {', '.join(missing)}")
