import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# Konfigurera loggning
logging.basicConfig(filename="hyperparameter_tuning.log", level=logging.INFO)


def load_training_data(file_path):
    """
    Laddar träningsdata från CSV-fil.
    """
    try:
        data = pd.read_csv(file_path)
        logging.info("✅ Träningsdata laddad.")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid laddning av träningsdata: {str(e)}")
        return None


def tune_hyperparameters(data, model_path="best_model.pkl"):
    """
    Utför hyperparameteroptimering på en RandomForest-modell.
    """
    try:
        feature_columns = [
            col for col in data.columns if col not in ["symbol", "date", "target"]
        ]
        X = data[feature_columns]
        y = data["target"]

        param_grid = {
            "n_estimators": [50, 100, 200],
            "max_depth": [5, 10, 20, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
        }

        model = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(
            model, param_grid, cv=5, n_jobs=-1, verbose=1, scoring="accuracy"
        )
        grid_search.fit(X, y)

        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_

        logging.info(f"✅ Bästa hyperparametrar: {best_params}")
        logging.info(f"✅ Optimerad modell sparad.")

        joblib.dump(best_model, model_path)
        return best_model
    except Exception as e:
        logging.error(f"❌ Fel vid hyperparameteroptimering: {str(e)}")
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

    best_model = tune_hyperparameters(simulated_data)
    print("📢 Bästa hyperparametrar har hittats och modellen har optimerats!")
