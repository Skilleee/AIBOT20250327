import logging
from typing import Dict, Any, Optional

# Konfigurera loggning
logging.basicConfig(filename="weekly_market_report.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def generate_weekly_market_report(market_data: Dict[str, Any]) -> Optional[str]:
    """
    Genererar en veckorapport över marknadens utveckling.
    """
    try:
        report = (
            f"📊 Veckorapport:\n"
            f"S&P 500: {market_data['sp500']}%\n"
            f"Nasdaq: {market_data['nasdaq']}%\n"
            f"Tech-sektorn: {market_data['tech_sector']}%\n"
            f"Sentiment: {market_data['sentiment']}"
        )
        logger.info("✅ Veckorapport genererad.")
        return report
    except Exception as e:
        logger.error(f"❌ Fel vid skapande av veckorapport: {str(e)}")
        return None

if __name__ == "__main__":
    market_data = {
        "sp500": 2.1,
        "nasdaq": 1.8,
        "tech_sector": 2.5,
        "sentiment": "Positiv",
    }
    report = generate_weekly_market_report(market_data)
    print(report)
