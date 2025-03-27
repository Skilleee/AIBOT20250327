import logging
from datetime import datetime
import pandas as pd
from typing import Dict, Any

# Konfigurera loggning
logging.basicConfig(filename="execution_feedback.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def evaluate_trade_performance(trade_log: pd.DataFrame) -> Dict[str, Any]:
    """
    Utvärderar hur väl tidigare rekommendationer har presterat baserat på faktiska marknadsrörelser.
    Returnerar en dict med win_rate, avg_return och antal trades.
    """
    try:
        trade_log = trade_log.copy()
        trade_log["return"] = (trade_log["exit_price"] - trade_log["entry_price"]) / trade_log["entry_price"]
        trade_log["win"] = trade_log["return"] > 0
        win_rate = trade_log["win"].mean()
        avg_return = trade_log["return"].mean()

        logger.info(f"[{datetime.now()}] ✅ Handelsutvärdering: Win rate: {win_rate:.2%}, Genomsnittlig avkastning: {avg_return:.2%}")
        return {
            "win_rate": round(float(win_rate), 4),
            "avg_return": round(float(avg_return), 4),
            "num_trades": len(trade_log)
        }
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid handelsutvärdering: {str(e)}")
        return {"win_rate": None, "avg_return": None, "num_trades": 0}

def refine_trading_strategy(trade_log: pd.DataFrame, threshold: float = 0.02) -> Dict[str, Any]:
    """
    Förbättrar strategin genom att analysera vilka signaler som fungerade bäst och justera framtida beslut.
    Returnerar en dict med antal bra/dåliga trades och en rekommendation.
    """
    try:
        if "return" not in trade_log.columns:
            trade_log["return"] = (trade_log["exit_price"] - trade_log["entry_price"]) / trade_log["entry_price"]

        good_trades = trade_log[trade_log["return"] > threshold]
        bad_trades = trade_log[trade_log["return"] < -threshold]

        recommendation = "adjust_threshold_up" if len(bad_trades) > len(good_trades) else "keep"
        logger.info(f"[{datetime.now()}] ✅ Strategiutvärdering: {len(good_trades)} bra trades, {len(bad_trades)} dåliga. Rekommendation: {recommendation}")
        return {
            "good_trades": len(good_trades),
            "bad_trades": len(bad_trades),
            "recommendation": recommendation
        }
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid strategianalys: {str(e)}")
        return {"good_trades": 0, "bad_trades": 0, "recommendation": "unknown"}

if __name__ == "__main__":
    # Simulerad handelslogg
    trade_log = pd.DataFrame({
        "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
        "entry_price": [150, 700, 250, 300, 2800],
        "exit_price": [155, 680, 270, 310, 2900],
        "trade_date": pd.date_range(start="2023-01-01", periods=5),
    })

    performance = evaluate_trade_performance(trade_log)
    print(f"📊 Handelsutvärdering: {performance}")
    strategy_refinement = refine_trading_strategy(trade_log)
    print(f"🔍 Justerad strategi: {strategy_refinement}")
