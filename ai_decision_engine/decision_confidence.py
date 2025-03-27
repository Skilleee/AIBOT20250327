import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="decision_confidence.log", level=logging.INFO)


def calculate_decision_confidence(trade_signals, risk_metrics, sentiment_score):
    """
    Beräknar en konfidensnivå för varje handelsbeslut baserat på signalstyrka, risknivå och sentiment.
    """
    try:
        signal_strength = trade_signals["signal_strength"]
        risk_factor = (
            1 - risk_metrics["volatility"]
        )  # Lägre volatilitet ger högre konfidens
        sentiment_factor = (sentiment_score + 1) / 2  # Normaliserad till 0-1

        confidence_score = (
            (signal_strength * 0.5) + (risk_factor * 0.3) + (sentiment_factor * 0.2)
        )
        logging.info("✅ Konfidensnivå beräknad för handelsbeslut.")
        return confidence_score
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av konfidensnivå: {str(e)}")
        return None


def adjust_decision_based_on_confidence(trade_signals, confidence_threshold=0.7):
    """
    Modifierar handelsbeslut beroende på hur säker modellen är på sina signaler.
    """
    try:
        confidence_score = calculate_decision_confidence(
            trade_signals,
            trade_signals["risk_metrics"],
            trade_signals["sentiment_score"],
        )

        adjusted_decision = pd.Series("HOLD", index=trade_signals.index)
        adjusted_decision[confidence_score > confidence_threshold] = "BUY"
        adjusted_decision[confidence_score < (1 - confidence_threshold)] = "SELL"

        logging.info("✅ Handelsbeslut justerade baserat på konfidensnivå.")
        return adjusted_decision
    except Exception as e:
        logging.error(
            f"❌ Fel vid justering av beslut baserat på konfidensnivå: {str(e)}"
        )
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerade handelssignaler
    trade_signals = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
            "signal_strength": [0.8, 0.6, 0.4, 0.9, 0.7],
            "risk_metrics": [
                {"volatility": 0.02},
                {"volatility": 0.05},
                {"volatility": 0.03},
                {"volatility": 0.04},
                {"volatility": 0.06},
            ],
            "sentiment_score": [0.2, -0.15, 0.05, 0.1, -0.05],
        }
    )

    confidence_adjusted_decision = adjust_decision_based_on_confidence(trade_signals)
    print(f"📢 Beslut baserade på konfidensnivå:")
    print(confidence_adjusted_decision)
