import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Optional, Tuple

# Konfigurera loggning
logging.basicConfig(filename="strategy_performance.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> Optional[float]:
    """
    Beräknar Sharpe-kvoten för att mäta riskjusterad avkastning.
    """
    try:
        excess_returns = returns - risk_free_rate / 252
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
        logger.info(f"✅ Sharpe Ratio beräknad: {sharpe_ratio:.2f}")
        return sharpe_ratio
    except Exception as e:
        logger.error(f"❌ Fel vid beräkning av Sharpe Ratio: {str(e)}")
        return None

def calculate_sortino_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> Optional[float]:
    """
    Beräknar Sortino-kvoten, som fokuserar på nedsiderisk.
    """
    try:
        downside_returns = returns[returns < 0]
        downside_deviation = np.std(downside_returns)
        if downside_deviation == 0:
            logger.warning("⚠️ Nedåtriktad standardavvikelse är 0, kan inte beräkna Sortino Ratio.")
            return None
        excess_returns = returns - risk_free_rate / 252
        sortino_ratio = np.mean(excess_returns) / downside_deviation
        logger.info(f"✅ Sortino Ratio beräknad: {sortino_ratio:.2f}")
        return sortino_ratio
    except Exception as e:
        logger.error(f"❌ Fel vid beräkning av Sortino Ratio: {str(e)}")
        return None

def plot_strategy_performance(trade_log: pd.DataFrame, output_file: str = "strategy_performance.png") -> None:
    """
    Skapar ett diagram över handelsstrategins avkastning över tiden.
    """
    try:
        if "return" not in trade_log.columns:
            raise ValueError("Kolumnen 'return' saknas i trade_log")
        trade_log["Cumulative Returns"] = (1 + trade_log["return"]).cumprod()
        plt.figure(figsize=(10, 5))
        plt.plot(trade_log["Cumulative Returns"], label="Strategins Avkastning", color="blue")
        plt.axhline(y=1, color="gray", linestyle="--", label="Startvärde")
        plt.legend()
        plt.title("Strategins Prestanda")
        plt.xlabel("Handel")
        plt.ylabel("Avkastning")
        plt.savefig(output_file)
        plt.close()
        logger.info("✅ Strategins prestandadiagram genererat.")
    except Exception as e:
        logger.error(f"❌ Fel vid skapande av prestandadiagram: {str(e)}")

def log_ai_recommendation(recommendations: list, trade_log_file: str = "trade_log.csv") -> None:
    """
    Lagrar AI:s rekommendationer i en CSV-fil.
    """
    try:
        df = pd.DataFrame(recommendations)
        df["timestamp"] = datetime.now()
        header = not pd.io.common.file_exists(trade_log_file)
        df.to_csv(trade_log_file, mode="a", header=header, index=False)
        logger.info(f"✅ {len(df)} AI-rekommendation(er) loggad(e) i {trade_log_file}.")
    except Exception as e:
        logger.error(f"❌ Fel vid loggning av AI-rekommendationer: {str(e)}")

def simulate_pl_from_log(trade_log: pd.DataFrame) -> Tuple[Optional[float], pd.DataFrame]:
    """
    Simulerar P/L baserat på in- och utpriser i trade_log.
    Returnerar total avkastning och uppdaterad trade_log.
    """
    try:
        if "return" not in trade_log.columns:
            trade_log["return"] = (trade_log["exit_price"] - trade_log["entry_price"]) / trade_log["entry_price"]
        total_return = (1 + trade_log["return"]).prod() - 1
        logger.info(f"✅ Simulerad totalavkastning: {total_return:.2%}")
        return total_return, trade_log
    except Exception as e:
        logger.error(f"❌ Fel vid P/L-simulering: {str(e)}")
        return None, trade_log

if __name__ == "__main__":
    trade_log = pd.DataFrame({
        "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
        "entry_price": [150, 700, 250, 300, 2800],
        "exit_price": [155, 680, 270, 310, 2900],
        "return": [0.033, -0.028, 0.08, 0.033, 0.035],
        "trade_date": pd.date_range(start="2023-01-01", periods=5),
    })

    sharpe = calculate_sharpe_ratio(trade_log["return"].values)
    sortino = calculate_sortino_ratio(trade_log["return"].values)
    print(f"📊 Sharpe Ratio: {sharpe:.2f}" if sharpe is not None else "Sharpe Ratio kunde inte beräknas")
    print(f"📉 Sortino Ratio: {sortino:.2f}" if sortino is not None else "Sortino Ratio kunde inte beräknas")
    plot_strategy_performance(trade_log)
    sample_recs = [
        {"symbol": "TSLA", "signal": "BUY", "recommended_price": 210.5},
        {"symbol": "AAPL", "signal": "SELL", "recommended_price": 155.2},
    ]
    log_ai_recommendation(sample_recs, "trade_log.csv")
    total_return, updated_log = simulate_pl_from_log(trade_log)
    print(f"📈 Totalavkastning: {total_return:.2%}" if total_return is not None else "Totalavkastning kunde inte beräknas")
