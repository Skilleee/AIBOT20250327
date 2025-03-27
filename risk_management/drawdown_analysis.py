import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="drawdown_analysis.log", level=logging.INFO)


def calculate_max_drawdown(returns):
    """
    Beräknar den maximala drawdownen i en portfölj.
    """
    try:
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()

        logging.info(f"✅ Maximal drawdown beräknad: {max_drawdown:.2%}")
        return max_drawdown
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av max drawdown: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    np.random.seed(42)
    returns = pd.Series(np.random.randn(100) / 100)
    max_dd = calculate_max_drawdown(returns)
    print(f"📢 Maximal drawdown: {max_dd:.2%}")
