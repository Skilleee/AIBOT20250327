import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="dynamic_sector_exposure.log", level=logging.INFO)


def calculate_sector_performance(sector_data):
    """
    Beräknar sektorns genomsnittliga avkastning över en viss period.
    """
    try:
        performance = sector_data.mean()
        logging.info(f"✅ Sektorprestanda beräknad: {performance}")
        return performance
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av sektorprestanda: {str(e)}")
        return None


def adjust_sector_exposure(portfolio, sector_performance, threshold=0.02):
    """
    Justerar exponeringen mot olika sektorer baserat på deras prestanda.
    """
    try:
        adjusted_exposure = portfolio.copy()
        for sector, performance in sector_performance.items():
            if performance > threshold:
                adjusted_exposure[sector] *= 1.1  # Öka exponering
            elif performance < -threshold:
                adjusted_exposure[sector] *= 0.9  # Minska exponering
        logging.info(f"✅ Sektorallokering justerad: {adjusted_exposure}")
        return adjusted_exposure
    except Exception as e:
        logging.error(f"❌ Fel vid justering av sektorallokering: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad data
    sectors = ["Tech", "Finance", "Healthcare", "Energy"]
    sector_data = pd.DataFrame(
        np.random.randn(100, len(sectors)) / 100, columns=sectors
    )

    sector_performance = calculate_sector_performance(sector_data)
    print(f"📊 Sektorprestanda: {sector_performance}")

    portfolio_allocation = {
        "Tech": 0.25,
        "Finance": 0.25,
        "Healthcare": 0.25,
        "Energy": 0.25,
    }
    adjusted_allocation = adjust_sector_exposure(
        portfolio_allocation, sector_performance
    )
    print(f"📈 Justerad sektorallokering: {adjusted_allocation}")
