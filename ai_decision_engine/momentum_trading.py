import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="momentum_trading.log", level=logging.INFO)


def calculate_momentum(prices, period=14):
    """
    Beräknar momentumindikator genom att jämföra nuvarande pris med priset X dagar tidigare.
    """
    try:
        momentum = prices - prices.shift(period)
        logging.info(f"✅ Momentum beräknat för {period} perioder.")
        return momentum
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av momentum: {str(e)}")
        return None


def relative_strength_index(prices, period=14):
    """
    Beräknar RSI (Relative Strength Index) för att mäta styrkan i momentum.
    """
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        logging.info(f"✅ RSI beräknat för {period} perioder.")
        return rsi
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av RSI: {str(e)}")
        return None


def momentum_strategy(prices, period=14, rsi_threshold=50):
    """
    Implementerar en enkel momentumstrategi baserad på RSI och momentumindikatorn.
    """
    try:
        momentum = calculate_momentum(prices, period)
        rsi = relative_strength_index(prices, period)

        signals = pd.Series(index=prices.index, dtype="object")
        signals[(momentum > 0) & (rsi > rsi_threshold)] = "BUY"
        signals[(momentum < 0) & (rsi < rsi_threshold)] = "SELL"

        logging.info(f"✅ Momentumstrategi genererad.")
        return signals
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av momentumstrategi: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad prisdata
    np.random.seed(42)
    simulated_prices = pd.Series(np.cumsum(np.random.randn(100)) + 100)

    momentum = calculate_momentum(simulated_prices)
    print(f"📊 Momentum: {momentum.tail()}")

    rsi = relative_strength_index(simulated_prices)
    print(f"📈 RSI: {rsi.tail()}")

    signals = momentum_strategy(simulated_prices)
    print(f"📢 Handelsignaler: {signals.tail()}")
