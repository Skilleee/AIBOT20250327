import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="portfolio_risk_management.log", level=logging.INFO)


def assess_portfolio_risk(portfolio_data):
    """
    Analyserar risknivån i portföljen och identifierar potentiella faror.
    """
    try:
        portfolio_data["volatility"] = (
            portfolio_data["returns"].rolling(window=20).std()
        )
        portfolio_data["risk_level"] = np.where(
            portfolio_data["volatility"] > portfolio_data["volatility"].median(),
            "HIGH RISK",
            "LOW RISK",
        )

        logging.info("✅ Portföljriskanalys genomförd.")
        return portfolio_data[["symbol", "volatility", "risk_level"]]
    except Exception as e:
        logging.error(f"❌ Fel vid riskanalys: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT"],
            "returns": np.random.randn(4) / 100,
        }
    )

    risk_analysis = assess_portfolio_risk(df)
    print("📢 Portföljriskanalys:")
    print(risk_analysis)
