import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="crypto_risk.log", level=logging.INFO)


def calculate_volatility(price_series, window=30):
    """
    Beräknar volatiliteten för en kryptovaluta över ett angivet fönster.
    """
    try:
        volatility = price_series.pct_change().rolling(window=window).std()
        logging.info(f"✅ Volatilitet beräknad över {window} dagar.")
        return volatility
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av volatilitet: {str(e)}")
        return None


def calculate_max_drawdown(price_series):
    """
    Beräknar den maximala drawdownen för att mäta risken för stora nedgångar.
    """
    try:
        cumulative_returns = (1 + price_series.pct_change()).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        logging.info(f"✅ Max Drawdown beräknad: {max_drawdown:.2%}")
        return max_drawdown
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av max drawdown: {str(e)}")
        return None


def risk_score(price_series, window=30):
    """
    Kombinerar volatilitet och max drawdown för att generera en riskpoäng.
    """
    try:
        vol = calculate_volatility(price_series, window)
        drawdown = calculate_max_drawdown(price_series)

        if vol is not None and drawdown is not None:
            risk_score = (vol.mean() + abs(drawdown)) / 2  # Enkel riskmodell
            logging.info(f"✅ Riskpoäng beräknad: {risk_score:.2f}")
            return risk_score
        else:
            return None
    except Exception as e:
        logging.error(f"❌ Fel vid riskpoängsberäkning: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad kryptoprisdata
    np.random.seed(42)
    simulated_prices = pd.Series(np.cumsum(np.random.randn(100)) + 50000)

    volatility = calculate_volatility(simulated_prices)
    print(f"📊 Volatilitet: {volatility.tail()}")

    max_dd = calculate_max_drawdown(simulated_prices)
    print(f"📉 Max Drawdown: {max_dd:.2%}")

    risk = risk_score(simulated_prices)
    print(f"⚠️ Riskpoäng: {risk:.2f}")
