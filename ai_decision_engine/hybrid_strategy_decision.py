import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="hybrid_strategy_decision.log", level=logging.INFO)


def combine_trading_strategies(
    momentum_signals, mean_reversion_signals, macro_score, sentiment_score
):
    """
    Kombinerar momentum, mean reversion, makroekonomi och sentiment för att skapa en hybridstrategi.
    """
    try:
        combined_score = (
            (momentum_signals["momentum_signal"] * 0.4)
            + (mean_reversion_signals["mean_reversion_signal"] * 0.3)
            + (macro_score * 0.2)
            + (sentiment_score * 0.1)
        )

        decision = pd.Series("HOLD", index=momentum_signals.index)
        decision[combined_score > 0.5] = "BUY"
        decision[combined_score < -0.5] = "SELL"

        logging.info("✅ Hybridstrategi genererad baserat på kombinerade signaler.")
        return decision
    except Exception as e:
        logging.error(f"❌ Fel vid generering av hybridstrategi: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerade handelssignaler
    momentum_signals = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
            "momentum_signal": [1, -1, 0, 1, -1],
        }
    )

    mean_reversion_signals = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
            "mean_reversion_signal": [-1, 1, 0, -1, 1],
        }
    )

    macro_score = pd.Series([0.2, -0.1, 0.05, 0.15, -0.2], index=momentum_signals.index)
    sentiment_score = pd.Series(
        [0.1, -0.2, 0.05, 0.1, -0.1], index=momentum_signals.index
    )

    hybrid_decision = combine_trading_strategies(
        momentum_signals, mean_reversion_signals, macro_score, sentiment_score
    )
    print(f"📢 Hybridstrategi-baserade beslut:")
    print(hybrid_decision)
