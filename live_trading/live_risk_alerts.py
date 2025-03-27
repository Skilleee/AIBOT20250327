import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="live_risk_alerts.log", level=logging.INFO)


def detect_risk_alerts(data, volatility_threshold=0.05):
    """
    Identifierar riskfyllda marknadsförhållanden och genererar varningar.
    """
    try:
        data["volatility"] = data["close"].pct_change().rolling(window=20).std()
        data["risk_alert"] = np.where(
            data["volatility"] > volatility_threshold, "HIGH RISK", "NORMAL"
        )

        logging.info("✅ Riskvarningar genererade.")
        return data[["date", "close", "volatility", "risk_alert"]]
    except Exception as e:
        logging.error(f"❌ Fel vid generering av riskvarningar: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=300),
            "close": np.cumsum(np.random.randn(300) * 2 + 100),
        }
    )

    risk_alerts = detect_risk_alerts(df)
    print("📢 Riskvarningar:")
    print(risk_alerts.tail())
