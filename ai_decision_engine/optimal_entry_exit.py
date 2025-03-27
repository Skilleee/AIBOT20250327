import sys, os
# Lägg till projektets rotmapp i sökvägen
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, Any, Optional

from notifications.telegram_bot import send_chart_to_telegram

# Konfigurera loggning
logging.basicConfig(filename="optimal_entry_exit.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def moving_average(prices: pd.Series, window: int = 20) -> Optional[pd.Series]:
    try:
        ma = prices.rolling(window=window).mean()
        logger.info(f"[{datetime.now()}] ✅ MA ({window} dagar) beräknad.")
        return ma
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ MA-fel: {str(e)}")
        return None

def bollinger_bands(prices: pd.Series, window: int = 20, num_std: int = 2) -> (Optional[pd.Series], Optional[pd.Series]):
    try:
        sma = moving_average(prices, window)
        std_dev = prices.rolling(window=window).std()
        upper_band = sma + (std_dev * num_std)
        lower_band = sma - (std_dev * num_std)
        logger.info(f"[{datetime.now()}] ✅ BB ({window}d, {num_std} std) klara.")
        return upper_band, lower_band
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ BB-fel: {str(e)}")
        return None, None

def optimal_entry_exit_strategy(signal_data: Dict[str, Any], window: int = 20, num_std: int = 2) -> Dict[str, Any]:
    try:
        prices = signal_data.get("prices")
        if prices is None or not isinstance(prices, pd.Series):
            raise ValueError("Ogiltig prisdata.")
        upper_band, lower_band = bollinger_bands(prices, window, num_std)
        if upper_band is None or lower_band is None:
            raise ValueError("Kunde inte beräkna Bollinger Bands.")
        last_price = prices.iloc[-1]
        entry = lower_band.iloc[-1]
        exit = upper_band.iloc[-1]
        if last_price < entry:
            signal = "BUY"
        elif last_price > exit:
            signal = "SELL"
        else:
            signal = "HOLD"
        result = {"entry": float(entry), "exit": float(exit), "signal": signal}
        logger.info(f"[{datetime.now()}] 📢 Signal: {signal}, Entry: {entry:.2f}, Exit: {exit:.2f}")
        return result
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel i strategi: {str(e)}")
        return {"entry": None, "exit": None, "signal": "HOLD"}

def generate_entry_exit_signals(prices: pd.Series, window: int = 20, num_std: int = 2) -> pd.Series:
    try:
        upper_band, lower_band = bollinger_bands(prices, window, num_std)
        signals = pd.Series(index=prices.index, dtype="object")
        signals[prices < lower_band] = "BUY"
        signals[prices > upper_band] = "SELL"
        signals.fillna("HOLD", inplace=True)
        logger.info(f"[{datetime.now()}] 📈 Signalserie genererad.")
        return signals
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel i signalgenerering: {str(e)}")
        return pd.Series(index=prices.index, data="HOLD")

def generate_entry_exit_dataframe(prices: pd.Series, window: int = 20, num_std: int = 2) -> pd.DataFrame:
    try:
        ma = moving_average(prices, window)
        upper_band, lower_band = bollinger_bands(prices, window, num_std)
        signals = generate_entry_exit_signals(prices, window, num_std)
        df = pd.DataFrame({
            "Price": prices,
            f"MA{window}": ma,
            "UpperBand": upper_band,
            "LowerBand": lower_band,
            "Signal": signals
        })
        logger.info(f"[{datetime.now()}] ✅ Entry/Exit DataFrame skapad.")
        return df
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel i DataFrame-generering: {str(e)}")
        return pd.DataFrame()

def plot_entry_exit_signals(df: pd.DataFrame, window: int = 20, save_png: bool = True) -> None:
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(df["Price"], label="Pris", linewidth=1.5)
        plt.plot(df[f"MA{window}"], label=f"MA{window}", linestyle="--")
        plt.plot(df["UpperBand"], label="Övre Band", color="green", alpha=0.5)
        plt.plot(df["LowerBand"], label="Nedre Band", color="red", alpha=0.5)

        buy_signals = df[df["Signal"] == "BUY"]
        sell_signals = df[df["Signal"] == "SELL"]
        plt.scatter(buy_signals.index, buy_signals["Price"], marker="^", color="green", label="BUY", s=80)
        plt.scatter(sell_signals.index, sell_signals["Price"], marker="v", color="red", label="SELL", s=80)

        plt.title("📉 Entry/Exit-signaler med Bollinger Bands")
        plt.xlabel("Datum")
        plt.ylabel("Pris")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if save_png:
            os.makedirs("charts", exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            file_path = f"charts/entry_exit_plot_{date_str}.png"
            plt.savefig(file_path)
            logger.info(f"[{datetime.now()}] 💾 Plot sparad till {file_path}")

            # Skicka till Telegram
            send_chart_to_telegram(file_path, caption=f"📊 Entry/Exit-signal ({date_str})")
        plt.show()
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid plotting: {str(e)}")

if __name__ == "__main__":
    np.random.seed(42)
    simulated_prices = pd.Series(np.cumsum(np.random.randn(100)) + 100)
    df = generate_entry_exit_dataframe(simulated_prices)
    print(f"\n🧾 Strategi DataFrame:\n{df.tail()}")
    strategy = optimal_entry_exit_strategy({"prices": simulated_prices})
    print(f"\n🎯 Optimal strategi-resultat:\n{strategy}")
    plot_entry_exit_signals(df)
