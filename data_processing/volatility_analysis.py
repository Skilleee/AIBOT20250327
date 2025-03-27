import logging
from datetime import datetime
import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="volatility_analysis.log", level=logging.INFO)


def calculate_daily_volatility(price_series):
    """
    Beräknar daglig volatilitet baserat på standardavvikelse av loggade avkastningar.
    Returnerar en float eller dict med mer info.
    """
    try:
        if not isinstance(price_series, (pd.Series, np.ndarray)) or len(price_series) < 2:
            raise ValueError("Ogiltig prisserie")

        log_returns = np.log(price_series / np.roll(price_series, 1))[1:]
        daily_volatility = np.std(log_returns)

        logging.info(
            f"[{datetime.now()}] ✅ Daglig volatilitet beräknad: {daily_volatility:.6f}"
        )
        return float(daily_volatility)
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid beräkning av daglig volatilitet: {str(e)}"
        )
        return None


def calculate_annual_volatility(price_series):
    """
    Beräknar årlig volatilitet genom att skala upp daglig volatilitet med roten ur 252.
    """
    try:
        daily_vol = calculate_daily_volatility(price_series)
        annual_volatility = daily_vol * np.sqrt(252) if daily_vol is not None else None
        if annual_volatility is not None:
            logging.info(
                f"[{datetime.now()}] ✅ Årlig volatilitet beräknad: {annual_volatility:.6f}"
            )
        return annual_volatility
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid beräkning av årlig volatilitet: {str(e)}"
        )
        return None


def analyze_historical_volatility(price_series, window=30):
    """
    Beräknar rullande volatilitet över en viss tidsperiod (t.ex. 30 dagar).
    """
    try:
        if not isinstance(price_series, (pd.Series, np.ndarray)) or len(price_series) < window:
            raise ValueError("Ogiltig prisserie eller för kort för vald tidsperiod")

        rolling_volatility = pd.Series(price_series).pct_change().rolling(window=window).std()
        logging.info(
            f"[{datetime.now()}] ✅ Historisk volatilitet analyserad över {window} dagar."
        )
        return rolling_volatility
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid analys av historisk volatilitet: {str(e)}"
        )
        return None


def fetch_vix_index():
    """
    Hämtar och returnerar det senaste värdet av VIX-index, som mäter marknadens förväntade volatilitet.
    """
    try:
        vix_value = np.random.uniform(15, 35)  # Simulerad data, ersätt med API-anrop
        logging.info(f"[{datetime.now()}] ✅ VIX-index: {vix_value:.2f}")
        return float(vix_value)
    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Fel vid hämtning av VIX-index: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    simulated_prices = pd.Series(np.random.normal(100, 5, 100))

    daily_vol = calculate_daily_volatility(simulated_prices)
    if daily_vol is not None:
        print(f"📉 Daglig volatilitet: {daily_vol:.6f}")

    annual_vol = calculate_annual_volatility(simulated_prices)
    if annual_vol is not None:
        print(f"📈 Årlig volatilitet: {annual_vol:.6f}")

    historical_vol = analyze_historical_volatility(simulated_prices)
    if historical_vol is not None:
        print(f"📊 Historisk volatilitet (30 dagar): {historical_vol.tail()}")

    vix_index = fetch_vix_index()
    if vix_index is not None:
        print(f"🌎 VIX-index: {vix_index:.2f}")
