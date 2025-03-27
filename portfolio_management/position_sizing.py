import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="position_sizing.log", level=logging.INFO)


def calculate_position_sizing(portfolio, risk_per_trade=0.02, total_capital=100000):
    """
    Beräknar optimal positionstorlek per tillgång baserat på risknivå.
    """
    try:
        portfolio["position_size"] = (risk_per_trade * total_capital) / portfolio[
            "stop_loss"
        ]

        logging.info("✅ Position sizing beräknad.")
        return portfolio[["symbol", "position_size"]]
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av position sizing: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    portfolio_df = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT"],
            "stop_loss": [5, 10, 8, 6],  # Exempel på stop-loss nivåer per aktie
        }
    )

    optimal_positions = calculate_position_sizing(portfolio_df)
    print("📢 Optimal position sizing:")
    print(optimal_positions)
