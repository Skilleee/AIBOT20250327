import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="sector_rotation_signals.log", level=logging.INFO)


def detect_sector_rotation(data):
    """
    Identifierar sektorrotation genom att jämföra sektorer baserat på momentum.
    """
    try:
        data["momentum"] = data.groupby("sector")["return"].transform(
            lambda x: x.rolling(20).mean()
        )
        best_sector = data.groupby("sector")["momentum"].last().idxmax()
        worst_sector = data.groupby("sector")["momentum"].last().idxmin()

        logging.info(f"✅ Bästa sektorn: {best_sector}, Sämsta sektorn: {worst_sector}")
        return best_sector, worst_sector
    except Exception as e:
        logging.error(f"❌ Fel vid sektorrotation-analys: {str(e)}")
        return None, None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=300),
            "sector": np.random.choice(
                ["Tech", "Finance", "Energy", "Healthcare"], 300
            ),
            "return": np.random.randn(300) / 100,
        }
    )

    best, worst = detect_sector_rotation(df)
    print(f"📢 Bästa sektorn: {best}, Sämsta sektorn: {worst}")
