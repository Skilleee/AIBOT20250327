import logging
from datetime import datetime

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="live_signal_generator.log", level=logging.INFO)


def generate_trading_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    Genererar köp- och säljsignaler baserat på tekniska indikatorer (SMA-50/200).
    Returnerar en DataFrame med signaler och SMA-kurvor.

    Signalregler:
    - SMA_50 > SMA_200 → BUY
    - SMA_50 < SMA_200 → SELL
    - Annars → HOLD
    """
    try:
        df = data.copy()
        df["SMA_50"] = df["close"].rolling(window=50).mean()
        df["SMA_200"] = df["close"].rolling(window=200).mean()

        df["signal"] = "HOLD"
        df.loc[df["SMA_50"] > df["SMA_200"], "signal"] = "BUY"
        df.loc[df["SMA_50"] < df["SMA_200"], "signal"] = "SELL"

        logging.info(f"[{datetime.now()}] ✅ Signaler genererade för {len(df)} rader.")
        return df[["date", "close", "SMA_50", "SMA_200", "signal"]]
    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Fel vid signalgenerering: {str(e)}")
        return pd.DataFrame()


def summarize_latest_signal(signal_df: pd.DataFrame) -> dict:
    """
    Sammanfattar den senaste signalen (BUY / SELL / HOLD).
    Returnerar en dict med signal och pris.
    """
    try:
        last_row = signal_df.dropna().iloc[-1]
        return {
            "signal": last_row["signal"],
            "close": float(last_row["close"]),
            "sma_50": float(last_row["SMA_50"]),
            "sma_200": float(last_row["SMA_200"]),
            "date": last_row["date"].strftime("%Y-%m-%d")
        }
    except Exception as e:
        logging.warning(f"[{datetime.now()}] ⚠️ Kunde inte sammanfatta senaste signal: {str(e)}")
        return {
            "signal": "HOLD",
            "close": None,
            "sma_50": None,
            "sma_200": None,
            "date": None
        }


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame({
        "date": pd.date_range(start="2023-01-01", periods=300),
        "close": np.cumsum(np.random.randn(300) * 2 + 100)
    })

    signals = generate_trading_signals(df)
    summary = summarize_latest_signal(signals)

    print("📢 Signaler (senaste 5):")
    print(signals.tail())
    print("\n📊 Sammanfattning av senaste signal:")
    print(summary)
