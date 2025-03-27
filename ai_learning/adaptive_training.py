import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Konfigurera loggning
logging.basicConfig(filename="adaptive_training.log", level=logging.INFO)


def load_training_data(file_path):
    """
    Laddar och förbereder träningsdata för modellen.
    """
    try:
        data = pd.read_csv(file_path)
        logging.info("✅ Träningsdata laddad.")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid laddning av träningsdata: {str(e)}")
        return None


def train_adaptive_model(data, model_path="adaptive_model.pkl"):
    """
    Tränar en adaptiv AI-modell och uppdaterar den med ny data vid behov.
    """
    try:
        feature_columns = [
            col for col in data.columns if col not in ["symbol", "date", "target"]
        ]
        X = data[feature_columns]
        y = data["target"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Ladda befintlig modell om den finns, annars skapa ny
        try:
            model = joblib.load(model_path)
            logging.info("✅ Existerande modell laddad.")
        except FileNotFoundError:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            logging.info("🔄 Ingen befintlig modell hittades, ny modell skapas.")

        # Träna eller finjustera modellen
        model.fit(X_train, y_train)

        # Utvärdera modellen
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"✅ Modell uppdaterad. Noggrannhet: {accuracy:.2%}")

        # Spara den uppdaterade modellen
        joblib.dump(model, model_path)
        logging.info("✅ Modell sparad.")

        return model
    except Exception as e:
        logging.error(f"❌ Fel vid träning av adaptiv modell: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad träningsdata
    np.random.seed(42)
    simulated_data = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=500),
            "symbol": np.random.choice(["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"], 500),
            "momentum": np.random.randn(500),
            "volatility": np.random.rand(500),
            "sentiment": np.random.uniform(-1, 1, 500),
            "target": np.random.choice([0, 1], 500),  # 0 = Sälj, 1 = Köp
        }
    )

    model = train_adaptive_model(simulated_data)
    print("📢 AI-modellen är uppdaterad och redo att använda!")
