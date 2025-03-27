import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="portfolio_backtesting.log", level=logging.INFO)


def backtest_portfolio(portfolio, historical_data):
    """
    Testar portföljstrategier på historiska data för att analysera prestanda.
    """
    try:
        portfolio_returns = historical_data.pct_change().dot(portfolio["weights"])
        cumulative_returns = (1 + portfolio_returns).cumprod()

        logging.info("✅ Portföljstrategi backtestad.")
        return cumulative_returns
    except Exception as e:
        logging.error(f"❌ Fel vid backtestning: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    np.random.seed(42)
    historical_data = pd.DataFrame(
        np.random.randn(100, 4) / 100, columns=["AAPL", "TSLA", "NVDA", "MSFT"]
    )
    portfolio_df = pd.DataFrame(
        {"symbol": ["AAPL", "TSLA", "NVDA", "MSFT"], "weights": [0.3, 0.2, 0.25, 0.25]}
    )

    backtest_results = backtest_portfolio(portfolio_df, historical_data)
    print("📢 Backtestad portföljprestanda:")
    print(backtest_results)
