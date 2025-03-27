import logging

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Konfigurera loggning
logging.basicConfig(filename="self_learning_ai.log", level=logging.INFO)


def generate_features(price_series, window=10):
    """
    Skapar funktioner baserade på historiska prisrörelser för AI-modellen.
    """
    try:
        df = pd.DataFrame(price_series, columns=["Close"])
        df["Returns"] = df["Close"].pct_change()
        df["MA"] = df["Close"].rolling(window=window).mean()
        df["Volatility"] = df["Returns"].rolling(window=window).std()
        df.dropna(inplace=True)
        logging.info("✅ Funktioner genererade för AI-inlärning.")
        return df
    except Exception as e:
        logging.error(f"❌ Fel vid generering av funktioner: {str(e)}")
        return None


def train_self_learning_model(price_series):
    """
    Tränar en självförbättrande AI-modell för att identifiera handelsmönster.
    """
    try:
        df = generate_features(price_series)
        df["Target"] = np.where(df["Returns"] > 0, 1, 0)

        X = df[["MA", "Volatility"]]
        y = df["Target"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        logging.info(f"✅ AI-modell tränad. Noggrannhet: {accuracy:.2%}")
        return model, accuracy
    except Exception as e:
        logging.error(f"❌ Fel vid träning av AI-modell: {str(e)}")
        return None, None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad prisdata
    np.random.seed(42)
    simulated_prices = pd.Series(np.cumsum(np.random.randn(200)) + 100)

    model, accuracy = train_self_learning_model(simulated_prices)
    print(f"🤖 AI-modell tränad med noggrannhet: {accuracy:.2%}")
