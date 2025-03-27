import logging

import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Konfigurera loggning
logging.basicConfig(filename="strategy_auto_optimizer.log", level=logging.INFO)


def evaluate_strategy(params, price_series):
    """
    Utvärderar en handelsstrategi baserat på givna parametrar och returnerar dess avkastning.
    """
    try:
        short_window, long_window = int(params[0]), int(params[1])
        short_ma = price_series.rolling(window=short_window).mean()
        long_ma = price_series.rolling(window=long_window).mean()
        signals = np.where(short_ma > long_ma, 1, -1)
        returns = price_series.pct_change() * signals[:-1]
        avg_return = returns.mean()
        logging.info(f"✅ Strategi utvärderad med avkastning: {avg_return:.4f}")
        return -avg_return  # Negativ eftersom vi minimerar i optimeringen
    except Exception as e:
        logging.error(f"❌ Fel vid strategiutvärdering: {str(e)}")
        return np.inf


def optimize_strategy(price_series, param_bounds=((5, 50), (50, 200))):
    """
    Optimerar en strategi genom att hitta bästa parametrarna för glidande medelvärden.
    """
    try:
        initial_guess = [10, 100]
        result = minimize(
            evaluate_strategy,
            initial_guess,
            args=(price_series,),
            bounds=param_bounds,
            method="L-BFGS-B",
        )
        optimized_params = result.x
        logging.info(
            f"✅ Strategioptimering klar: Short MA={optimized_params[0]:.0f}, Long MA={optimized_params[1]:.0f}"
        )
        return optimized_params
    except Exception as e:
        logging.error(f"❌ Fel vid strategioptimering: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad prisdata
    np.random.seed(42)
    simulated_prices = pd.Series(np.cumsum(np.random.randn(100)) + 100)

    optimized_params = optimize_strategy(simulated_prices)
    print(
        f"🔍 Optimerade parametrar: Short MA={optimized_params[0]:.0f}, Long MA={optimized_params[1]:.0f}"
    )
