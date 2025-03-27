import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="feature_engineering.log", level=logging.INFO)


def calculate_technical_indicators(data):
    """
    Beräknar tekniska indikatorer såsom RSI, glidande medelvärde och volatilitet.
    """
    try:
        data["SMA_20"] = data["close"].rolling(window=20).mean()
        data["SMA_50"] = data["close"].rolling(window=50).mean()

        delta = data["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data["RSI"] = 100 - (100 / (1 + rs))

        data["volatility"] = data["close"].rolling(window=20).std()

        logging.info("✅ Teknisk analysindikatorer beräknade.")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av tekniska indikatorer: {str(e)}")
        return None


def generate_feature_matrix(data):
    """
    Skapar en feature-matris för maskininlärning baserat på tekniska och fundamentala faktorer.
    """
    try:
        data = calculate_technical_indicators(data)
        data.dropna(inplace=True)

        feature_columns = ["SMA_20", "SMA_50", "RSI", "volatility", "volume"]
        feature_matrix = data[feature_columns]

        logging.info("✅ Feature-matris skapad för maskininlärning.")
        return feature_matrix
    except Exception as e:
        logging.error(f"❌ Fel vid skapande av feature-matris: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad marknadsdata
    np.random.seed(42)
    data = pd.DataFrame(
        {
            "close": np.cumsum(np.random.randn(1000) * 2 + 100),
            "volume": np.random.randint(100, 1000, size=1000),
        }
    )

    feature_matrix = generate_feature_matrix(data)
    print(f"📊 Feature-matris för AI-modellen:")
    print(feature_matrix.head())
