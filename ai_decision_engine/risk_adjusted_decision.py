import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="risk_adjusted_decision.log", level=logging.INFO)


def calculate_risk_metrics(trade_log):
    """
    Beräknar riskmått såsom volatilitet, drawdown och Sharpe-ratio.
    """
    try:
        trade_log["return"] = (
            trade_log["exit_price"] - trade_log["entry_price"]
        ) / trade_log["entry_price"]
        volatility = trade_log["return"].std()
        max_drawdown = trade_log["return"].cumsum().min()
        sharpe_ratio = trade_log["return"].mean() / volatility if volatility > 0 else 0

        logging.info(
            f"✅ Riskmått beräknade: Volatilitet={volatility:.4f}, Max Drawdown={max_drawdown:.4f}, Sharpe Ratio={sharpe_ratio:.4f}"
        )
        return {
            "volatility": volatility,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
        }
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av riskmått: {str(e)}")
        return None


def adjust_decision_based_on_risk(trade_log, risk_threshold=0.02):
    """
    Justerar beslut baserat på risknivåer.
    """
    try:
        risk_metrics = calculate_risk_metrics(trade_log)
        if risk_metrics is None:
            return None

        adjusted_decision = pd.Series("HOLD", index=trade_log.index)
        adjusted_decision[
            (trade_log["return"] > risk_threshold) & (risk_metrics["sharpe_ratio"] > 1)
        ] = "BUY"
        adjusted_decision[
            (trade_log["return"] < -risk_threshold)
            | (risk_metrics["max_drawdown"] < -0.1)
        ] = "SELL"

        logging.info("✅ Riskjusterade beslut genererade.")
        return adjusted_decision
    except Exception as e:
        logging.error(f"❌ Fel vid justering av beslut baserat på risk: {str(e)}")
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

    risk_adjusted_decision = adjust_decision_based_on_risk(trade_log)
    print(f"📢 Riskjusterade beslut:")
    print(risk_adjusted_decision)
