import logging
from typing import Dict, Any, Optional

# Konfigurera loggning
logging.basicConfig(filename="macro_event_impact.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def generate_macro_event_impact_report(event_data: Dict[str, Any]) -> Optional[str]:
    """
    Analyserar hur en makrohändelse påverkat marknaden.
    Förväntar sig att event_data innehåller nycklarna:
      - 'event': Händelsen
      - 'sp500': S&P 500-siffran (t.ex. 2.1)
    Övriga värden (t.ex. 'bond_market' och 'usd_movement') hanteras med standardvärde 'N/A' om de saknas.
    """
    try:
        event = event_data.get('event', 'Ingen händelse angiven')
        sp500 = event_data.get('sp500', 'N/A')
        bond_market = event_data.get('bond_market', 'N/A')
        usd_movement = event_data.get('usd_movement', 'N/A')
        report = (
            f"📢 Makrohändelsepåverkan:\n"
            f"Händelse: {event}\n"
            f"S&P 500: {sp500}%\n"
            f"Obligationsmarknadens respons: {bond_market}\n"
            f"USD-rörelse: {usd_movement}%"
        )
        logger.info("✅ Makrohändelserapport genererad.")
        return report
    except Exception as e:
        logger.error(f"❌ Fel vid skapande av makrohändelserapport: {str(e)}")
        return None

if __name__ == "__main__":
    dummy_event_data = {
        "event": "Fed höjde räntan med 0.25%",
        "sp500": 2.1,
        # Om du inte har information om obligationsmarknad och USD-rörelse, används standardvärdet 'N/A'
    }
    report = generate_macro_event_impact_report(dummy_event_data)
    print(report)
