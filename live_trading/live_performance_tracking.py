import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="live_performance_tracking.log", level=logging.INFO)


def track_signal_performance(signals, actual_prices):
    """
    Utvärderar hur väl AI:ns signaler presterar i realtid.
    """
    try:
        signals["actual_return"] = (
            actual_prices["close"] - actual_prices["close"].shift(1)
        ) / actual_prices["close"].shift(1)
        signals["success"] = (signals["signal"] == "BUY") & (
            signals["actual_return"] > 0
        ) | (signals["signal"] == "SELL") & (signals["actual_return"] < 0)
        accuracy = signals["success"].mean()

        logging.info(f"✅ Signalträffsäkerhet: {accuracy:.2%}")
        return accuracy
    except Exception as e:
        logging.error(f"❌ Fel vid spårning av signalprestanda: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    signals_df = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=300),
            "signal": ["BUY", "SELL", "HOLD"] * 100,
        }
    )

    actual_prices_df = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=300),
            "close": (
                100
                + pd.Series(range(300))
                + pd.Series(range(300)).apply(lambda x: x % 5 - 2)
            ).cumsum(),
        }
    )

    accuracy = track_signal_performance(signals_df, actual_prices_df)
    print(f"📢 Signalträffsäkerhet: {accuracy:.2%}")
