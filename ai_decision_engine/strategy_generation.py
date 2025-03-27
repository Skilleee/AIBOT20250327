#!/usr/bin/env python3
import logging
from datetime import datetime
from typing import Optional, Dict, Any

import numpy as np
import pandas as pd

# För Prophet: Försök importera den nyare versionen, annars fbprophet
try:
    from prophet import Prophet
except ImportError:
    from fbprophet import Prophet

logging.basicConfig(
    filename="strategy_generation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def generate_momentum_strategy(
    data: pd.DataFrame,
    sentiment: Optional[Dict[str, float]] = None,
    macro_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Genererar en momentum-baserad strategi baserat på sentiment, pris och makrodata.
    """
    try:
        if "close" in data.columns and isinstance(data["close"], (pd.Series, list, np.ndarray)):
            signal = "buy"
            if sentiment and isinstance(sentiment, dict):
                signal = "buy" if sentiment.get("positive", 0) > sentiment.get("negative", 0) else "sell"
            elif macro_data and isinstance(macro_data, dict):
                signal = "buy" if macro_data.get("GDP", 0) > 0 else "sell"

            strategy = {
                "signal": signal,
                "confidence": 0.75,
                "source": "momentum",
                "sentiment_input": sentiment,
                "macro_input": macro_data
            }
            logger.info(f"✅ Momentum-strategi genererad: {strategy}")
            return strategy
        else:
            raise ValueError("Ogiltig eller saknad 'close'-data i input DataFrame.")
    except Exception as e:
        logger.error(f"❌ Fel i generate_momentum_strategy: {str(e)}")
        return {"signal": "neutral", "confidence": 0.0}

def generate_momentum_signal_series(
    data: pd.DataFrame,
    sentiment: Optional[Dict[str, float]] = None
) -> pd.DataFrame:
    """
    Returnerar en DataFrame med dagliga signaler baserat på sentimentdata.
    """
    try:
        df = data.copy()
        df["signal"] = "buy" if sentiment and sentiment.get("positive", 0) > sentiment.get("negative", 0) else "sell"
        logger.info(f"📊 Signalserie genererad: {df['signal'].iloc[-1]}")
        return df
    except Exception as e:
        logger.error(f"❌ Fel i generate_momentum_signal_series: {str(e)}")
        return pd.DataFrame()

def generate_mean_reversion_strategy(
    data: pd.DataFrame,
    window: int = 50,
    threshold: float = 2.0
) -> Optional[pd.DataFrame]:
    """
    Genererar en mean reversion-strategi genom Bollinger Bands.
    """
    try:
        df = data.copy()
        df["moving_avg"] = df["close"].rolling(window=window).mean()
        df["std_dev"] = df["close"].rolling(window=window).std()
        df["upper_band"] = df["moving_avg"] + (threshold * df["std_dev"])
        df["lower_band"] = df["moving_avg"] - (threshold * df["std_dev"])
        df["signal"] = np.where(
            df["close"] < df["lower_band"],
            1,  # Köp-signal
            np.where(df["close"] > df["upper_band"], -1, 0)  # Sälj-signal eller neutral
        )
        logger.info(f"✅ Mean reversion-strategi genererad med {window}-dagars Bollinger Bands.")
        return df[["close", "moving_avg", "upper_band", "lower_band", "signal"]]
    except Exception as e:
        logger.error(f"❌ Fel vid generering av mean reversion-strategi: {str(e)}")
        return None

def combine_strategies(
    momentum_data: pd.DataFrame,
    mean_reversion_data: Optional[pd.DataFrame]
) -> Optional[pd.DataFrame]:
    """
    Kombinerar momentum- och mean reversion-strategier till en hybridstrategi.
    """
    try:
        combined_data = momentum_data.copy()
        if "signal" not in combined_data.columns:
            combined_data["signal"] = 0

        if mean_reversion_data is not None and "signal" in mean_reversion_data.columns:
            combined_data["combined_signal"] = combined_data["signal"] + mean_reversion_data["signal"].fillna(0)
        else:
            combined_data["combined_signal"] = combined_data["signal"]

        logger.info("✅ Strategier kombinerade till en hybridmodell.")
        return combined_data[["close", "combined_signal"]]
    except Exception as e:
        logger.error(f"❌ Fel vid kombination av strategier: {str(e)}")
        return None

def generate_future_price_forecast(
    data: pd.DataFrame,
    forecast_days: int = 365
) -> pd.DataFrame:
    """
    Genererar en framtidsprognos för prisdata med hjälp av Prophet.
    """
    try:
        df = data.copy()
        df = df.rename(columns={"date": "ds", "close": "y"})
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)
        logger.info(f"✅ Tidsserieprognos genererad för {forecast_days} dagar.")
        return forecast
    except Exception as e:
        logger.error(f"❌ Fel vid generering av framtidsprognos: {str(e)}")
        return pd.DataFrame()

def extract_price_targets(forecast: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    Extraherar riktpriser från en framtidsprognos.
    """
    if forecast.empty:
        return {"3m": None, "6m": None, "12m": None}

    future_forecast = forecast[forecast["ds"] >= datetime.now()]
    price_targets = {"3m": None, "6m": None, "12m": None}

    forecast_3m = future_forecast.head(90)
    if len(forecast_3m) == 90:
        price_targets["3m"] = float(forecast_3m["yhat"].iloc[-1])

    forecast_6m = future_forecast.head(180)
    if len(forecast_6m) == 180:
        price_targets["6m"] = float(forecast_6m["yhat"].iloc[-1])

    forecast_12m = future_forecast.head(365)
    if len(forecast_12m) == 365:
        price_targets["12m"] = float(forecast_12m["yhat"].iloc[-1])

    return price_targets

if __name__ == "__main__":
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=200, freq="D")
    prices = np.cumsum(np.random.randn(200) * 2 + 100)
    stock_data = pd.DataFrame({"date": dates, "close": prices})
    stock_data.set_index("date", inplace=True)

    sentiment_data = {"positive": 0.6, "negative": 0.4}
    momentum_strategy_dict = generate_momentum_strategy(stock_data, sentiment_data)
    print(f"\n📈 Momentum-strategi (signal):\n{momentum_strategy_dict}")

    momentum_df = generate_momentum_signal_series(stock_data, sentiment_data)
    print(f"\n📉 Signalserie:\n{momentum_df.tail()}")

    mean_reversion_strategy = generate_mean_reversion_strategy(stock_data)
    if mean_reversion_strategy is not None:
        print(f"\n📊 Mean Reversion-strategi:\n{mean_reversion_strategy.tail()}")
    else:
        print("\n⚠️ Kunde inte generera mean reversion-strategi")

    combined_strategy = combine_strategies(momentum_df, mean_reversion_strategy)
    if combined_strategy is not None:
        print(f"\n🔀 Hybridstrategi:\n{combined_strategy.tail()}")
    else:
        print("\n⚠️ Kunde inte kombinera strategier")

    df_for_forecast = pd.DataFrame({"date": dates, "close": prices})
    forecast = generate_future_price_forecast(df_for_forecast, forecast_days=365)
    if not forecast.empty:
        price_targets = extract_price_targets(forecast)
        print(f"\n🎯 Riktpriser (3m, 6m, 12m): {price_targets}")
    else:
        print("\n⚠️ Kunde inte generera prognos")
