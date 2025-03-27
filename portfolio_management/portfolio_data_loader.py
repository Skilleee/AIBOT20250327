import os
import gspread
import json
import base64
import logging
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Konfigurera loggning
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ladda .env och verifiera att den finns
dotenv_path = Path.home() / "ai_trading_bot" / ".env"
if not dotenv_path.exists():
    raise FileNotFoundError(f"❌ .env-filen hittades inte på: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)
logger.info("✅ .env-filen laddad.")

# Ladda credentials från fil eller Base64
try:
    credentials_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    base64_str = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")

    if credentials_path and os.path.exists(credentials_path):
        with open(credentials_path, "r") as f:
            credentials_dict = json.load(f)
        logger.info(f"✅ Credentials laddade från fil: {credentials_path}")
    elif base64_str:
        credentials_json = base64.b64decode(base64_str).decode("utf-8")
        credentials_dict = json.loads(credentials_json)
        logger.info("✅ Credentials laddade från Base64.")
    else:
        raise ValueError("❌ Varken GOOGLE_SERVICE_ACCOUNT_JSON eller GOOGLE_SHEETS_CREDENTIALS_JSON är definierade i .env")
except Exception as e:
    logger.error(f"❌ Fel vid laddning av Google Sheets credentials: {e}")
    raise

# Autentisera med Google Sheets API
try:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    gc = gspread.authorize(creds)
    logger.info("✅ Autentisering mot Google Sheets lyckades.")
except Exception as e:
    logger.error(f"❌ Kunde inte autentisera mot Google Sheets: {e}")
    raise

# Hämta kalkylarket med Sheet ID från .env
try:
    SHEET_ID = os.getenv("SHEET_ID")
    if not SHEET_ID:
        raise ValueError("❌ SHEET_ID saknas i .env-filen")
    sheet = gc.open_by_key(SHEET_ID)
    logger.info("✅ Kalkylarket öppnades med Sheet ID.")
except Exception as e:
    logger.error(f"❌ Kunde inte öppna kalkylarket: {e}")
    raise

def fetch_all_portfolios() -> Dict[str, pd.DataFrame]:
    """
    Hämtar portföljdata för angivna konton och returnerar en dictionary
    där varje värde är ett DataFrame.
    """
    portfolios: Dict[str, pd.DataFrame] = {}
    konton = ["Alice", "Valter", "Pension", "Investeringskonto"]

    for konto in konton:
        try:
            worksheet = sheet.worksheet(konto)
            rows = worksheet.get_all_records()
            if rows:
                portfolios[konto] = pd.DataFrame(rows)
            else:
                portfolios[konto] = pd.DataFrame()
            logger.info(f"✅ Portföljdata hämtad för {konto}.")
        except Exception as e:
            portfolios[konto] = pd.DataFrame()
            logger.warning(f"⚠️ Kunde inte hämta data för {konto}: {e}")

    return portfolios

if __name__ == "__main__":
    data = fetch_all_portfolios()
    for konto, innehav in data.items():
        print(f"\n📁 {konto}:")
        print(innehav)
