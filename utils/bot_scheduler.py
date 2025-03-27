import logging
import schedule
import threading
import time
from datetime import datetime

from reports.generate_report import generate_and_send_daily_pdf_report
from notifications.telegram_bot import send_ai_recommendations, send_telegram_notification
from data_collection.macro_data import fetch_macro_data
from risk_management.risk_warning import detect_risk_level

from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(filename="scheduler_manager.log", level=logging.INFO)


def schedule_all_tasks():
    """
    Schemalägg alla uppgifter som AI-boten ska utföra automatiskt.
    """
    logging.info("🕒 Initierar schemalagda uppgifter...")

    # Daglig PDF-rapport med AI-data
    schedule.every().day.at("18:00").do(generate_and_send_daily_pdf_report)

    # AI-rekommendationer & nya investeringar
    schedule.every().day.at("17:00").do(send_ai_recommendations)

    # Makrohändelsekoll varje timme
    schedule.every().hour.at(":05").do(check_macro_events)

    # Riskvarning varje timme
    schedule.every().hour.at(":10").do(send_risk_alert_if_needed)

    # Starta schemaläggning i bakgrundstråd
    thread = threading.Thread(target=_run_scheduler_loop, daemon=True)
    thread.start()


def check_macro_events():
    try:
        macro_data = fetch_macro_data()
        today = datetime.today().date()

        for key, value in macro_data.items():
            if isinstance(value, dict):
                timestamp = value.get("date")
                if timestamp:
                    event_date = datetime.strptime(timestamp, "%Y-%m-%d").date()
                    if event_date == today:
                        message = f"📢 Makrohändelse: {key} släpptes idag – {value.get('value', '')}"
                        send_telegram_notification(message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
                        logging.info(f"Makrohändelse skickad: {key}")
    except Exception as e:
        logging.error(f"❌ Fel vid makrohändelsekontroll: {str(e)}")


def send_risk_alert_if_needed():
    try:
        risk_level = detect_risk_level()
        if risk_level > 0.05:
            message = f"⚠️ Hög volatilitet upptäckt! Risknivå: {risk_level:.2%}. Överväg att minska exponering."
            send_telegram_notification(message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
            logging.info("🚨 Riskvarning skickad")
    except Exception as e:
        logging.error(f"❌ Fel vid riskvarning: {str(e)}")


def _run_scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)
