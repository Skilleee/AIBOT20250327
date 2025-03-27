import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="drawdown_protection.log", level=logging.INFO)


def calculate_max_drawdown(price_series):
    """
    Beräknar max drawdown för att mäta den största nedgången från en topp till en botten.
    """
    try:
        cumulative_returns = (1 + price_series.pct_change()).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        logging.info(f"✅ Max Drawdown beräknad: {max_drawdown:.2%}")
        return max_drawdown, drawdown
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av max drawdown: {str(e)}")
        return None, None


def implement_drawdown_protection(price_series, threshold=-0.2):
    """
    Implementerar skyddsåtgärder när drawdown når en viss tröskel.
    """
    try:
        max_drawdown, drawdown_series = calculate_max_drawdown(price_series)

        if max_drawdown <= threshold:
            logging.warning(
                f"🚨 Kritisk drawdown: {max_drawdown:.2%} - Förslag: Minska exponering!"
            )
            return "Reduce Exposure"
        else:
            logging.info(f"✅ Drawdown under kontroll: {max_drawdown:.2%}")
            return "Hold Position"
    except Exception as e:
        logging.error(f"❌ Fel vid implementering av drawdown protection: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad prisdata
    np.random.seed(42)
    simulated_prices = pd.Series(np.cumsum(np.random.randn(100)) + 100)

    max_dd, drawdown_series = calculate_max_drawdown(simulated_prices)
    print(f"📉 Max Drawdown: {max_dd:.2%}")

    protection_signal = implement_drawdown_protection(simulated_prices)
    print(f"🛡️ Drawdown Protection Signal: {protection_signal}")
