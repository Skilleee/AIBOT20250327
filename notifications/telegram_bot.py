# notifications/telegram_bot.py

import logging
from datetime import datetime
import json
import os
import requests

# Behåll AI-importerna om du fortfarande vill använda dem
from portfolio_management.portfolio_ai_analysis import (
    generate_ai_recommendations,
    suggest_new_investments,
)

# === VIKTIG ÄNDRING: importera från "scripts.fetch_data" istället för "portfolio_google_sheets"
from scripts.fetch_data import fetch_all_portfolios

# Om du vill läsa in tokens/ID från .env:
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # Se till att denna finns
JSON_KEYFILE_PATH = "/home/rlundkvist87/secrets/service_account.json"

logging.basicConfig(filename="telegram_notifications.log", level=logging.INFO)

def send_telegram_message(message, reply_markup=None):
    """
    Skickar ett meddelande via Telegram med valfri inline-knapp.
    """
    try:
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logging.error("Saknar TELEGRAM_BOT_TOKEN eller TELEGRAM_CHAT_ID i miljövariabler.")
            return None

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        response = requests.post(url, data=data)
        response.raise_for_status()
        logging.info("✅ Telegram-meddelande skickat.")
        return response.json()
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av Telegram-meddelande: {str(e)}")
        return None

def send_pdf_report_to_telegram(file_path):
    """
    Skickar en PDF-rapport som bilaga via Telegram.
    """
    try:
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logging.error("Saknar TELEGRAM_BOT_TOKEN eller TELEGRAM_CHAT_ID i miljövariabler.")
            return False

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, "rb") as pdf_file:
            files = {"document": pdf_file}
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": f"Daglig AI-rapport – {datetime.today().date()}"
            }
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            logging.info("✅ PDF-rapport skickad till Telegram.")
            return response.ok
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av PDF-rapport: {str(e)}")
        return False

def send_chart_to_telegram(image_path, caption="Entry/Exit-graf"):
    """
    Skickar ett diagram som bild via Telegram.
    """
    try:
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logging.error("Saknar TELEGRAM_BOT_TOKEN eller TELEGRAM_CHAT_ID i miljövariabler.")
            return False

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as img:
            files = {"photo": img}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            logging.info("✅ Diagram skickat till Telegram.")
            return response.ok
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av diagram: {str(e)}")
        return False

def send_full_daily_report(market_data, risk_level, macro_event):
    """
    Skickar ett samlat dagligt meddelande med:
      - Marknadsrapport
      - Riskvarning
      - Portföljöversikt (per konto)
      - AI-rekommendationer (om du vill)
      - Nya investeringsförslag (om du vill)
      - Makrohändelse
    """
    try:
        # 1) Daglig marknadsrapport
        market_summary = (
            "*Daglig marknadsrapport:*\n"
            f"- S&P 500: {market_data.get('sp500', 'N/A')}%\n"
            f"- Nasdaq: {market_data.get('nasdaq', 'N/A')}%\n"
            f"- Tech-sektorn: {market_data.get('tech_sector', 'N/A')}%\n"
            f"- Sentiment: {market_data.get('sentiment', 'N/A')}\n"
        )

        # 2) Riskvarning
        risk_msg = ""
        if risk_level > 0.05:
            risk_msg = (
                f"\n⚠️ *Hög volatilitet upptäckt!* "
                f"Risknivå: *{risk_level:.2%}*. Överväg att minska exponering.\n"
            )

        # 3) Hämta AI-rekommendationer (om du vill behålla AI-delen)
        recommendations = generate_ai_recommendations()

        # 4) Hämta portföljerna (från nya fetch_data.py)
        #    - Samma rad som förr, men nu från scripts.fetch_data
        if not GOOGLE_SHEET_ID:
            logging.error("Saknar 'GOOGLE_SHEET_ID' i miljövariabler/.env")
            return
        portfolios = fetch_all_portfolios(JSON_KEYFILE_PATH, GOOGLE_SHEET_ID)

        # 5) Få nya investeringsförslag (om du vill behålla AI-delen)
        new_suggestions = suggest_new_investments(portfolios)

        # 6) Sammanfatta portföljvärden + AI-rekommendationer
        portfolio_msg = "*Portföljöversikt & Rekommendationer*\n"
        for account, recs in recommendations.items():
            # Beräkna totalvärde från recs eller från portfolios
            # (Beroende på hur du vill göra. Nedan ett enkelt exempel:)
            total_konto = 0.0
            for r in recs:
                val = r.get("total_värde", 0)
                if isinstance(val, (int, float)):
                    total_konto += val

            # Skriv ut info
            portfolio_msg += f"\n*{account}*\n"
            portfolio_msg += f"Totalt värde (estimerat): {total_konto:,.2f} SEK\n"
            for r in recs:
                namn = r.get("namn", "Okänt")
                antal = r.get("antal", 0)
                pris = r.get("pris", "N/A")
                valuta = r.get("valuta", "")
                total_värde = r.get("total_värde", 0)
                rek = r.get("rekommendation", "")
                motiv = r.get("motivering", "")
                portfolio_msg += (
                    f"• `{namn}`: {antal} st à {pris} {valuta} "
                    f"(~{total_värde:,.2f} {valuta})\n"
                    f"   Rek: *{rek}* – _{motiv}_\n"
                )
            portfolio_msg += "\n"

        # 7) Föreslagna nya investeringar
        invest_msg = "*Föreslagna nya investeringar:*\n"
        for account, forslag in new_suggestions.items():
            invest_msg += f"\n*{account}:*\n"
            if isinstance(forslag, list) and len(forslag) > 0:
                for kategori, namn in forslag:
                    invest_msg += f"• `{namn}` – {kategori}\n"
            else:
                invest_msg += "• (Inga förslag)\n"

        # 8) Makrohändelse
        macro_msg = f"\n*Makrohändelse:* {macro_event}\n"

        # 9) Slå ihop all text
        full_message = (
            f"{market_summary}"
            f"{risk_msg}"
            f"{portfolio_msg}"
            f"{invest_msg}"
            f"{macro_msg}"
        )

        # 10) Inline-knapp (exempel)
        reply_markup = {
            "inline_keyboard": [
                [{"text": "Öppna Dashboard", "url": "https://example.com/dashboard"}]
            ]
        }

        # 11) Skicka meddelande
        send_telegram_message(full_message, reply_markup=reply_markup)

    except Exception as e:
        logging.error(f"❌ Fel vid skapande av full daily report: {str(e)}")

def main():
    # Exempeldata för manuell testkörning
    market_data = {
        "sp500": 1.2,
        "nasdaq": 0.8,
        "tech_sector": 1.5,
        "sentiment": "Positiv",
    }
    risk_level = 0.06
    macro_event = "Fed höjde räntan med 0.25%."

    send_full_daily_report(market_data, risk_level, macro_event)

    # Om du vill skicka PDF därefter
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"reports/daily_report_{today}.pdf"
    send_pdf_report_to_telegram(file_path)

if __name__ == "__main__":
    main()
