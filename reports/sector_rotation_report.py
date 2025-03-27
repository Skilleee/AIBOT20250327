import logging
from typing import Dict, Optional

# Konfigurera loggning
logging.basicConfig(filename="sector_rotation_report.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def generate_sector_rotation_report(sector_data: Dict[str, float]) -> Optional[str]:
    """
    Genererar en rapport över sektorer som presterat bäst och sämst.
    """
    try:
        best_sector = max(sector_data, key=sector_data.get)
        worst_sector = min(sector_data, key=sector_data.get)
        report = (
            f"🔄 Sektorrotation:\n"
            f"Bästa sektorn: {best_sector} ({sector_data[best_sector]}%)\n"
            f"Sämsta sektorn: {worst_sector} ({sector_data[worst_sector]}%)"
        )
        logger.info("✅ Sektorrotationsrapport genererad.")
        return report
    except Exception as e:
        logger.error(f"❌ Fel vid skapande av sektorrapport: {str(e)}")
        return None

if __name__ == "__main__":
    sector_data = {"Tech": 5.2, "Finance": 3.8, "Energy": 7.8, "Real Estate": -3.2}
    report = generate_sector_rotation_report(sector_data)
    print(report)
