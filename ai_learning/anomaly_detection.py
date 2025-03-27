import logging

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Konfigurera loggning
logging.basicConfig(filename="anomaly_detection.log", level=logging.INFO)


def detect_anomalies(data, contamination=0.01):
    """
    Upptäcker anomalier i marknadsdata med hjälp av Isolation Forest.
    """
    try:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)

        model = IsolationForest(contamination=contamination, random_state=42)
        data["anomaly_score"] = model.fit_predict(scaled_data)

        anomalies = data[data["anomaly_score"] == -1]
        logging.info(f"✅ {len(anomalies)} anomalier upptäckta i marknadsdatan.")
        return anomalies
    except Exception as e:
        logging.error(f"❌ Fel vid upptäckt av anomalier: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad marknadsdata
    np.random.seed(42)
    simulated_data = pd.DataFrame(
        {
            "price_change": np.random.randn(1000),
            "volume_change": np.random.randn(1000),
            "volatility": np.random.rand(1000),
        }
    )

    anomalies = detect_anomalies(simulated_data)
    print("📢 Upptäckta anomalier:")
    print(anomalies)
