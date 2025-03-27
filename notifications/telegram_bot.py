import logging
from datetime import datetime
import requests

from portfolio_management.portfolio_ai_analysis import generate_ai_recommendations, suggest_new_investments
from portfolio_management.portfolio_google_sheets import fetch_all_portfolios
from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# 📄 Loggning
logging.basicConfig(filename="telegram_notifications.log", level=logging.INFO)

# 🟢 Grundläggande funktion för att skicka text
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, data=data)
        logging.info("✅ Telegram-meddelande skickat.")
        return response.json()
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av Telegram-meddelande: {str(e)}")
        return None

# 📊 Daglig AI-analys + nya förslag
def send_ai_recommendations():
    try:
        recommendations = generate_ai_recommendations()
        new_suggestions = suggest_new_investments(fetch_all_portfolios())

        message = "🤖 *AI Rekommendationer per konto:*\n"
        for konto, innehav in recommendations.items():
            message += f"\n📁 *{konto}*\n"
            for post in innehav:
                namn = post["namn"]
                kategori = post["kategori"]
                värde = post["värde"]
                rek = post["rekommendation"]
                message += f"• `{namn}` ({kategori}, {värde} kr): *{rek}*\n"

        message += "\n🆕 *Föreslagna nya investeringar:*\n"
        for konto, förslag in new_suggestions.items():
            message += f"\n📁 *{konto}*\n"
            for kategori, namn in förslag:
                message += f"• `{namn}` – {kategori}\n"

        send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid AI-rekommendationer: {str(e)}")

# 📎 Skicka PDF-rapport som bilaga
def send_pdf_report_to_telegram(file_path):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, "rb") as pdf_file:
            files = {"document": pdf_file}
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": f"📄 Daglig AI-rapport – {datetime.today().date()}"
            }
            response = requests.post(url, data=data, files=files)
            logging.info("✅ PDF-rapport skickad till Telegram.")
            return response.ok
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av PDF-rapport: {str(e)}")
        return False

# 🖼️ Skicka diagram till Telegram
def send_chart_to_telegram(image_path, caption="📈 Entry/Exit-graf"):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as img:
            files = {"photo": img}
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption
            }
            response = requests.post(url, data=data, files=files)
            logging.info("✅ Diagram skickat till Telegram.")
            return response.ok
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av diagram till Telegram: {str(e)}")
        return False

# 📈 Marknadsrapport
def send_daily_market_report(market_data):
    try:
        summary = (
            f"📊 *Daglig marknadsrapport:*\n"
            f"S&P 500: {market_data['sp500']}%\n"
            f"Nasdaq: {market_data['nasdaq']}%\n"
            f"Tech-sektorn: {market_data['tech_sector']}%\n"
            f"Sentiment: {market_data['sentiment']}"
        )
        send_telegram_message(summary)
    except Exception as e:
        logging.error(f"❌ Fel vid marknadsrapport: {str(e)}")

# ⚠️ Riskvarning
def send_risk_alert(risk_level):
    try:
        if risk_level > 0.05:
            message = f"⚠️ *Hög volatilitet upptäckt!* Risknivå: *{risk_level:.2%}*. Överväg att minska exponering."
            send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid riskvarning: {str(e)}")

# 📢 Portföljuppdatering
def send_portfolio_update(portfolio_data):
    try:
        message = "📢 *Portföljuppdatering:*\n"
        for stock, change in portfolio_data.items():
            message += f"{stock}: {change:.2%}\n"
        send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid portföljnotis: {str(e)}")

# 🌐 Makrohändelser
def send_macro_event_alert(event):
    try:
        message = f"📢 *Makrohändelse:* {event}"
        send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid makronotis: {str(e)}")

# 🔍 Sammanfattning efter RL-backtest
def send_rl_backtest_summary(reward, final_value):
    try:
        message = (
            f"🤖 *RL-agentens backtest:*\n"
            f"• Total reward: {reward:.2f}\n"
            f"• Slutligt portföljvärde: {final_value:,.2f} SEK"
        )
        send_telegram_message(message)
    except Exception as e:
        logging.error(f"❌ Fel vid skickning av RL-backtestresultat: {str(e)}")

# 🔁 Test
if __name__ == "__main__":
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
    send_pdf_report_to_telegram("reports/daily_report.pdf")
