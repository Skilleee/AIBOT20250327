import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="capital_allocation_decision.log", level=logging.INFO)


def calculate_optimal_allocation(
    trade_log, risk_metrics, max_allocation=0.3, min_allocation=0.05
):
    """
    Beräknar optimal kapitalallokering baserat på risknivå och handelsavkastning.
    """
    try:
        trade_log["return"] = (
            trade_log["exit_price"] - trade_log["entry_price"]
        ) / trade_log["entry_price"]

        # Normalisera avkastningen och riskmåtten
        normalized_return = (trade_log["return"] - trade_log["return"].min()) / (
            trade_log["return"].max() - trade_log["return"].min()
        )
        normalized_risk = (
            risk_metrics["volatility"] - risk_metrics["volatility"].min()
        ) / (risk_metrics["volatility"].max() - risk_metrics["volatility"].min())

        # Beräkna allokering som en funktion av avkastning och risk
        allocation = (
            max_allocation * normalized_return - min_allocation * normalized_risk
        )
        allocation = np.clip(allocation, min_allocation, max_allocation)

        logging.info("✅ Kapitalallokering beräknad för varje handel.")
        return allocation
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av kapitalallokering: {str(e)}")
        return None


def adjust_allocation_based_on_market(trade_log, market_conditions):
    """
    Justerar kapitalallokeringen baserat på marknadsläge (bullish/bearish/neutral).
    """
    try:
        market_factor = {"bullish": 1.2, "neutral": 1.0, "bearish": 0.8}

        adjusted_allocation = trade_log["allocation"] * market_factor.get(
            market_conditions, 1.0
        )
        logging.info("✅ Kapitalallokering justerad baserat på marknadsläge.")
        return adjusted_allocation
    except Exception as e:
        logging.error(f"❌ Fel vid justering av kapitalallokering: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad handelslogg
    trade_log = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
            "entry_price": [150, 700, 250, 300, 2800],
            "exit_price": [155, 680, 270, 310, 2900],
            "trade_date": pd.date_range(start="2023-01-01", periods=5),
        }
    )

    # Simulerad riskanalys
    risk_metrics = pd.DataFrame({"volatility": [0.02, 0.05, 0.03, 0.04, 0.06]})

    optimal_allocation = calculate_optimal_allocation(trade_log, risk_metrics)
    trade_log["allocation"] = optimal_allocation

    adjusted_allocation = adjust_allocation_based_on_market(trade_log, "bullish")
    trade_log["adjusted_allocation"] = adjusted_allocation

    print(f"📢 Kapitalallokering efter justering:")
    print(trade_log[["symbol", "allocation", "adjusted_allocation"]])
