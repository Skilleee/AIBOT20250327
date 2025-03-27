import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="dynamic_allocation.log", level=logging.INFO)


def dynamic_allocation(portfolio, market_trends):
    """
    Justerar portföljens allokering dynamiskt baserat på marknadstrender.
    """
    try:
        portfolio["adjustment"] = portfolio["sector"].apply(
            lambda x: 0.05 if x in market_trends else -0.05
        )
        portfolio["new_allocation"] = np.clip(
            portfolio["allocation"] + portfolio["adjustment"], 0, 1
        )
        logging.info("✅ Dynamisk allokering uppdaterad.")
        return portfolio
    except Exception as e:
        logging.error(f"❌ Fel vid dynamisk allokering: {str(e)}")
        return portfolio


# Exempelanrop
if __name__ == "__main__":
    portfolio = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "GOOGL", "JPM", "XOM"],
            "sector": ["Tech", "Tech", "Tech", "Finance", "Energy"],
            "allocation": [0.25, 0.20, 0.15, 0.25, 0.15],
        }
    )

    market_trends = ["Tech", "Finance"]
    updated_portfolio = dynamic_allocation(portfolio, market_trends)

    print("📊 Uppdaterad portfölj:")
    print(updated_portfolio)
