import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="sentiment_decision.log", level=logging.INFO)


def analyze_sentiment(sentiment_data):
    """
    Analyserar sentimentdata och returnerar en sammanfattad sentimentpoäng.
    """
    try:
        sentiment_score = sentiment_data["sentiment_score"].mean()
        logging.info(f"✅ Genomsnittlig sentimentpoäng beräknad: {sentiment_score:.4f}")
        return sentiment_score
    except Exception as e:
        logging.error(f"❌ Fel vid analys av sentiment: {str(e)}")
        return None


def adjust_decision_based_on_sentiment(
    sentiment_data, trade_log, sentiment_threshold=0.1
):
    """
    Justerar handelsbeslut baserat på sentimentdata.
    """
    try:
        sentiment_score = analyze_sentiment(sentiment_data)
        if sentiment_score is None:
            return None

        adjusted_decision = pd.Series("HOLD", index=trade_log.index)
        adjusted_decision[(sentiment_score > sentiment_threshold)] = "BUY"
        adjusted_decision[(sentiment_score < -sentiment_threshold)] = "SELL"

        logging.info("✅ Sentimentbaserade beslut genererade.")
        return adjusted_decision
    except Exception as e:
        logging.error(f"❌ Fel vid justering av beslut baserat på sentiment: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad sentimentdata
    sentiment_data = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
            "sentiment_score": [0.2, -0.15, 0.05, 0.1, -0.05],
        }
    )

    # Simulerad handelslogg
    trade_log = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
            "entry_price": [150, 700, 250, 300, 2800],
            "exit_price": [155, 680, 270, 310, 2900],
            "trade_date": pd.date_range(start="2023-01-01", periods=5),
        }
    )

    sentiment_adjusted_decision = adjust_decision_based_on_sentiment(
        sentiment_data, trade_log
    )
    print(f"📢 Sentimentjusterade beslut:")
    print(sentiment_adjusted_decision)
