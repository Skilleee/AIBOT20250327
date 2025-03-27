import sys, os
# Lägg till projektets rotmapp i sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import logging
from fpdf import FPDF
from datetime import datetime
import os
from typing import Optional
from notifications.telegram_bot import send_pdf_report_to_telegram

logging.basicConfig(filename="monthly_performance_report.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def generate_monthly_performance_pdf(report_data: dict, output_path: str = "reports/monthly_report.pdf") -> Optional[str]:
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        # Använd inbyggt typsnitt (Helvetica) för att undvika problem med externa fontfiler
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Månadsrapport - AI Trading Bot", ln=True)
        pdf.ln(10)

        pdf.set_font("Helvetica", "", 12)
        for konto, data in report_data.items():
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, f"{konto}", ln=True)
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(0, 10, f"Avkastning: {data['portfolio_return']}%", ln=True)
            pdf.cell(0, 10, f"S&P 500: {data['sp500']}%", ln=True)
            pdf.cell(0, 10, f"Bästa innehav: {data['best_performer']} ({data['best_return']}%)", ln=True)
            pdf.cell(0, 10, f"Sämsta innehav: {data['worst_performer']} ({data['worst_return']}%)", ln=True)
            pdf.ln(5)

        pdf.output(output_path)
        logger.info("✅ Månadsrapport PDF genererad.")
        return output_path
    except Exception as e:
        logger.error(f"❌ Fel vid skapande av PDF: {str(e)}")
        return None

def send_monthly_report(report_data: dict) -> None:
    pdf_path = generate_monthly_performance_pdf(report_data)
    if pdf_path and os.path.exists(pdf_path):
        success = send_pdf_report_to_telegram(pdf_path)
        if success:
            logger.info("✅ Månadsrapport skickad till Telegram.")
        else:
            logger.warning("⚠️ Kunde inte skicka månadsrapport till Telegram.")
    else:
        logger.warning("⚠️ Inget PDF-dokument genererat för månadsrapport.")

if __name__ == "__main__":
    example_data = {
        "Investeringskonto": {
            "portfolio_return": 5.2,
            "sp500": 4.3,
            "best_performer": "AAPL",
            "best_return": 8.1,
            "worst_performer": "TSLA",
            "worst_return": -2.3,
        },
        "Pension": {
            "portfolio_return": 3.1,
            "sp500": 4.3,
            "best_performer": "MSFT",
            "best_return": 6.5,
            "worst_performer": "XACT Norden",
            "worst_return": -1.4,
        }
    }
    send_monthly_report(example_data)
