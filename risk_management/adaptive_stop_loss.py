import logging
from datetime import datetime
import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="adaptive_stop_loss.log", level=logging.INFO)


def adaptive_stop_loss(signal_data):
    """
    Returnerar en enkel adaptiv stop-loss baserat på AI-signal (buy/sell).

    Args:
        signal_data (dict): Exempelvis {"signal": "buy"}

    Returns:
        dict: {"stop_loss": 0.03}
    """
    try:
        signal = signal_data.get("signal", "buy").lower()

        if signal == "buy":
            stop = 0.03  # 3 % nedåt
        elif signal == "sell":
            stop = 0.05  # 5 % uppåt
        else:
            stop = 0.04  # neutral fallback

        result = {"stop_loss": stop}
        logging.info(f"[{datetime.now()}] ✅ AI-baserad stop-loss för '{signal}': {stop}")
        return result

    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Fel i adaptive_stop_loss: {str(e)}")
        return {"stop_loss": 0.05}


def atr_based_stop_loss(price_data, atr_multiplier=3, window=14):
    """
    Beräknar en adaptiv stop-loss baserad på marknadsvolatilitet (ATR).

    Args:
        price_data (pd.DataFrame): Innehåller kolumnerna 'High', 'Low', 'Close'
        atr_multiplier (int): Multiplikator för att justera känslighet
        window (int): Antal perioder för ATR-beräkning

    Returns:
        pd.Series: Stop-loss-nivåer
    """
    try:
        high_low = price_data["High"] - price_data["Low"]
        high_close = np.abs(price_data["High"] - price_data["Close"].shift(1))
        low_close = np.abs(price_data["Low"] - price_data["Close"].shift(1))

        true_range = pd.DataFrame({
            "TR1": high_low,
            "TR2": high_close,
            "TR3": low_close
        }).max(axis=1)

        atr = true_range.rolling(window=window).mean()
        stop_loss = price_data["Close"] - (atr_multiplier * atr)

        logging.info(f"[{datetime.now()}] 📊 ATR-baserad stop-loss beräknad med multiplier={atr_multiplier}, window={window}")
        return stop_loss

    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Fel i atr_based_stop_loss: {str(e)}")
        return pd.Series([np.nan] * len(price_data), index=price_data.index)


# Exempelanrop
if __name__ == "__main__":
    # Simulerad prisdata för demonstration
    np.random.seed(42)
    price_data = pd.DataFrame({
        "High": np.random.uniform(100, 110, 100),
        "Low": np.random.uniform(90, 100, 100),
        "Close": np.random.uniform(95, 105, 100),
    })

    # ATR-baserad stop-loss
    atr_stop = atr_based_stop_loss(price_data)
    print("📉 ATR-baserad Stop-Loss (senaste 5):")
    print(atr_stop.tail())

    # Enkel AI-signalbaserad stop-loss
    signal_result = adaptive_stop_loss({"signal": "buy"})
    print("🤖 AI-baserad Stop-Loss:")
    print(signal_result)
