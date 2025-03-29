import logging
from datetime import datetime
import json
import requests

from portfolio_management.portfolio_ai_analysis import generate_ai_recommendations, suggest_new_investments
from portfolio_management.portfolio_google_sheets import fetch_all_portfolios
from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Konfigurera loggning
logging.basicConfig(filename="telegram_notifications.log", level=logging.INFO)

# Grundläggande funktion för att skicka meddelanden via Telegram med stöd för reply_markup
def send_telegram_message(message, reply_markup=None):
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

# Funktion för att skicka AI-rekommendationer med utökad information och inline-knapp för dashboard
def send_ai_recommendations():
    try:
        recommendations = generate_ai_recommendations()
        new_suggestions = suggest_new_investments(fetch_all_portfolios())
        message = " *AI Rekommendationer per konto:*\n"
        
        for konto, innehav in recommendations.items():
            message += f"\n *{konto}*\n"
            for post in innehav:
                # Säkerställ att vi arbetar med en dictionary
                if isinstance(post, dict):
                    namn = post.get("namn", "Okänt")
                    kategori = post.get("kategori", "Okänt")
                    värde = post.get("värde", "N/A")
                    rek = post.get("rekommendation", "")
                    motivering = post.get("motivering", "")
                    riktkurs_3m = post.get("riktkurs_3m", "N/A")
                    riktkurs_6m = post.get("riktkurs_6m", "N/A")
                    riktkurs_12m = post.get("riktkurs_12m", "N/A")
                    pe_ratio = post.get("pe_ratio", "N/A")
                    rsi = post.get("rsi", "N/A")
                    riskbedomning = post.get("riskbedomning", "N/A")
                    historisk_prestanda = post.get("historisk_prestanda", "N/A")
                    
                    message += f"• `{namn}` ({kategori}, {värde} kr): *{rek}*"
                    if motivering:
                        message += f" – {motivering}"
                    message += f"\n  Riktkurser: 3 mån: {riktkurs_3m}, 6 mån: {riktkurs_6m}, 12 mån: {riktkurs_12m}\n"
                    message += f"  PE-tal: {pe_ratio}, RSI: {rsi}, Riskbedömning: {riskbedomning}\n"
                    message += f"  Historisk Prestanda: {historisk_prestanda}\n"
                    message += f"  Länkar: [Visa historik](https://example.com/historik/{namn}), [Mer info](https://example.com/info/{namn})\n\n"
                else:
                    # Om post inte är en dictionary läggs den bara till som text
                    message += f"• {post}\n"
        
        message += "\n *Föreslagna nya investeringar:*\n"
        for konto, förslag in new_suggestions.items():
            message += f"\n *{konto}*\n"
            for kategori, namn in förslag:
                message += f"• `{namn}` – {kategori}\n"
        
        # Exempel på inline-knapp som öppnar en dashboard
        reply_markup = {
            "inline_keyboard": [
                [{"text": "Öppna Dashboard", "url": "https://example.com/dashboard"}]
            ]
        }
        
        send_telegram_message(message, reply_markup=reply_markup)
    except Exception as e:
        logging.error(f"❌ Fel vid AI-rekommendationer: {str(e)}")

# Funktion för att skicka en PDF-rapport som bilaga
def send_pdf_report_to_telegram(file_path):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, "rb") as pdf_file:
            files = {"document": pdf_file}
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": f" Daglig AI-rapport – {datetime.today().date()}"
            }
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            logging.info("✅ PDF-rapport skickad till Telegram.")
            return response.ok
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av PDF-rapport: {str(e)}")
        return False

# Funktion för att skicka ett diagram som bild
def send_chart_to_telegram(image_path, caption="Entry/Exit-graf"):
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
        logging.error(f"❌ Fel vid skickning av diagram till Telegram: {str(e)}")
        return False

# Funktion för att skicka en daglig marknadsrapport
def send_daily_market_report(market_data):
    try:
        summary = (
            f" *Daglig marknadsrapport:*\n"
            f"S&P 500: {market_data['sp500']}%\n"
            f"Nasdaq: {market_data['nasdaq']}%\n"
            f"Tech-sektorn: {market_data['tech_sector']}%\n"
            f"Sentiment: {market_data['sentiment']}"
        )
        send_telegram_message(summary)
    except Exception as e:
        logging.error(f"❌ Fel vid marknadsrapport: {str(e)}")

# Funktion för att skicka en riskvarning vid hög volatilitet
def send_risk_alert(risk_level):
    try:
        if risk_level > 0.05:
            message = f"⚠️ *Hög volatilitet upptäckt!* Risknivå: *{risk_level:.2%}*. Överväg att minska exponering."
            send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid riskvarning: {str(e)}")

# Funktion för att skicka portföljuppdatering
def send_portfolio_update(portfolio_data):
    try:
        message = " *Portföljuppdatering:*\n"
        for stock, change in portfolio_data.items():
            message += f"{stock}: {change:.2%}\n"
        send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid portföljnotis: {str(e)}")

# Funktion för att skicka makrohändelser
def send_macro_event_alert(event):
    try:
        message = f" *Makrohändelse:* {event}"
        send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid makronotis: {str(e)}")

# Funktion för att skicka en sammanfattning efter RL-backtest
def send_rl_backtest_summary(reward, final_value):
    try:
        message = (
            f" *RL-agentens backtest:*\n"
            f"• Total reward: {reward:.2f}\n"
            f"• Slutligt portföljvärde: {final_value:,.2f} SEK"
        )
        send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av RL-backtestresultat: {str(e)}")

if __name__ == "__main__":
    # Exempeldata för testkörning
    market_data = {
        "sp500": 1.2,
        "nasdaq": 0.8,
        "tech_sector": 1.5,
        "sentiment": "Positiv",
    }
    risk_level = 0.06
    portfolio_data = {"Tesla": -0.05, "Apple": 0.02, "Amazon": 0.03}
    macro_event = "Fed höjde räntan med 0.25%."
    
    send_daily_market_report(market_data)
    send_risk_alert(risk_level)
    send_portfolio_update(portfolio_data)
    send_macro_event_alert(macro_event)
    send_ai_recommendations()
    send_rl_backtest_summary(12543.21, 108769.56)
    
    # Bygg ett dynamiskt filnamn baserat på dagens datum
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"reports/daily_report_{today}.pdf"
    send_pdf_report_to_telegram(file_path)
