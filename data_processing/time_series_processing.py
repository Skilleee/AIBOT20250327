import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="time_series_processing.log", level=logging.INFO)


def generate_moving_average(data, column, window=20):
    """
    Beräknar glidande medelvärde för en tidsserie.
    """
    try:
        data[f"SMA_{window}"] = data[column].rolling(window=window).mean()
        logging.info(f"✅ {window}-dagars glidande medelvärde beräknat.")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av glidande medelvärde: {str(e)}")
        return None


def calculate_trend_indicator(data, column):
    """
    Beräknar en enkel trendindikator baserad på derivatan av priset.
    """
    try:
        data[f"trend_{column}"] = np.gradient(data[column])
        logging.info("✅ Trendindikator beräknad.")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid trendanalys: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=100),
            "price": np.cumsum(np.random.randn(100) * 2 + 100),
        }
    )

    df = generate_moving_average(df, "price")
    df = calculate_trend_indicator(df, "price")
    print("📢 Bearbetad tidsseriedata:")
    print(df.tail())
