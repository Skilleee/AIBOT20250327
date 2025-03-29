import logging
from datetime import datetime
import json
import requests

from portfolio_management.portfolio_ai_analysis import (
    generate_ai_recommendations,
    suggest_new_investments,
)
from portfolio_management.portfolio_google_sheets import fetch_all_portfolios
from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(filename="telegram_notifications.log", level=logging.INFO)

def send_telegram_message(message, reply_markup=None):
    """
    Skickar ett meddelande via Telegram med valfri inline-knapp.
    """
    try:
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
      - AI-rekommendationer
      - Nya investeringsförslag
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

        # 3) Hämta AI-rekommendationer & nya investeringsförslag
        recommendations = generate_ai_recommendations()
        portfolios = fetch_all_portfolios()
        new_suggestions = suggest_new_investments(portfolios)

        # 4) Sammanfatta portföljvärden per konto + AI-rekommendationer
        portfolio_msg = "*Portföljöversikt & Rekommendationer*\n"
        for account, recs in recommendations.items():
            # Beräkna totalvärde
            total_konto = 0
            for r in recs:
                val = r.get("total_värde", 0)
                if isinstance(val, (int, float)):
                    total_konto += val

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

        # 5) Föreslagna nya investeringar
        invest_msg = "*Föreslagna nya investeringar:*\n"
        for account, forslag in new_suggestions.items():
            invest_msg += f"\n*{account}:*\n"
            if isinstance(forslag, list) and len(forslag) > 0:
                for kategori, namn in forslag:
                    invest_msg += f"• `{namn}` – {kategori}\n"
            else:
                invest_msg += "• (Inga förslag)\n"

        # 6) Makrohändelse
        macro_msg = f"\n*Makrohändelse:* {macro_event}\n"

        # 7) Slå ihop all text till ett meddelande
        full_message = (
            f"{market_summary}"
            f"{risk_msg}"
            f"{portfolio_msg}"
            f"{invest_msg}"
            f"{macro_msg}"
        )

        # 8) Lägg till inline-knapp (exempel: Dashboard)
        reply_markup = {
            "inline_keyboard": [
                [{"text": "Öppna Dashboard", "url": "https://example.com/dashboard"}]
            ]
        }

        send_telegram_message(full_message, reply_markup=reply_markup)
    except Exception as e:
        logging.error(f"❌ Fel vid skapande av full daily report: {str(e)}")

# Nedan är de gamla funktionerna om du fortfarande vill använda dem separat
def send_daily_market_report(market_data):
    ...
def send_risk_alert(risk_level):
    ...
def send_portfolio_update(portfolio_data):
    ...
def send_macro_event_alert(event):
    ...
def send_rl_backtest_summary(reward, final_value):
    ...

if __name__ == "__main__":
    # Exempeldata för testkörning
    market_data = {
        "sp500": 1.2,
        "nasdaq": 0.8,
        "tech_sector": 1.5,
        "sentiment": "Positiv",
    }
    risk_level = 0.06
    macro_event = "Fed höjde räntan med 0.25%."

    # Anropa vår nya funktion
    send_full_daily_report(market_data, risk_level, macro_event)

    # Skicka PDF om du vill
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"reports/daily_report_{today}.pdf"
    send_pdf_report_to_telegram(file_path)
