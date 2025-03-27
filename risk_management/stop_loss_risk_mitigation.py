import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="stop_loss_risk_mitigation.log", level=logging.INFO)


def analyze_stop_loss_levels(portfolio, stop_loss_percentage=0.05):
    """
    Utvärderar hur effektiva stop-loss-nivåer är och föreslår justeringar.
    """
    try:
        portfolio["stop_loss_price"] = portfolio["current_price"] * (
            1 - stop_loss_percentage
        )
        logging.info("✅ Stop-loss nivåer analyserade och föreslagna.")
        return portfolio[["symbol", "current_price", "stop_loss_price"]]
    except Exception as e:
        logging.error(f"❌ Fel vid stop-loss analys: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    portfolio_df = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT"],
            "current_price": [150, 800, 600, 310],
        }
    )

    stop_loss_analysis = analyze_stop_loss_levels(portfolio_df)
    print("📢 Stop-loss analys:")
    print(stop_loss_analysis)
