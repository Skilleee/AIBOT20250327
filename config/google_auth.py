import os
import json
import base64
import gspread
from config.config import GOOGLE_SHEETS_CREDENTIALS

def get_gspread_client():
    """
    Returnerar gspread-klient:
    - Prioritet 1: Base64-sträng från .env (GOOGLE_SHEETS_CREDENTIALS_JSON)
    - Prioritet 2: Lokalt JSON-path från .env (GOOGLE_SHEETS_JSON_PATH)
    - Prioritet 3: Default till 'config/service_account.json'
    """
    try:
        if GOOGLE_SHEETS_CREDENTIALS:
            creds_json = base64.b64decode(GOOGLE_SHEETS_CREDENTIALS).decode()
            creds_dict = json.loads(creds_json)
            return gspread.service_account_from_dict(creds_dict)

        # Annars, försök läsa från lokal fil
        path = os.getenv("GOOGLE_SHEETS_JSON_PATH", "config/service_account.json")
        return gspread.service_account(filename=path)

    except Exception as e:
        raise RuntimeError(f"❌ Misslyckades att autentisera med Google Sheets: {e}")
