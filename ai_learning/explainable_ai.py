import logging

import joblib
import numpy as np
import pandas as pd
import shap

# Konfigurera loggning
logging.basicConfig(filename="explainable_ai.log", level=logging.INFO)


def load_model(model_path):
    """
    Laddar en sparad AI-modell.
    """
    try:
        model = joblib.load(model_path)
        logging.info("✅ Modell laddad för explainability-analys.")
        return model
    except Exception as e:
        logging.error(f"❌ Fel vid laddning av modellen: {str(e)}")
        return None


def explain_model_predictions(model, data):
    """
    Förklarar modellens beslut med hjälp av SHAP-värden.
    """
    try:
        explainer = shap.Explainer(model, data)
        shap_values = explainer(data)

        logging.info("✅ SHAP-värden beräknade för modellens beslut.")
        return shap_values
    except Exception as e:
        logging.error(f"❌ Fel vid SHAP-analys: {str(e)}")
        return None


def visualize_feature_importance(shap_values, feature_names):
    """
    Skapar en graf för att visualisera vilka faktorer som påverkar besluten mest.
    """
    try:
        shap.summary_plot(shap_values, feature_names=feature_names)
        logging.info("✅ Feature-importance visualiserad.")
    except Exception as e:
        logging.error(f"❌ Fel vid visualisering av feature-importance: {str(e)}")


# Exempelanrop
if __name__ == "__main__":
    # Simulerad träningsdata
    np.random.seed(42)
    feature_names = ["momentum", "volatility", "sentiment"]
    simulated_data = pd.DataFrame(
        {
            "momentum": np.random.randn(100),
            "volatility": np.random.rand(100),
            "sentiment": np.random.uniform(-1, 1, 100),
        }
    )

    # Ladda och förklara modellen
    model = load_model("best_model.pkl")
    if model:
        shap_values = explain_model_predictions(model, simulated_data)
        visualize_feature_importance(shap_values, feature_names)
        print("📢 AI-beslut har analyserats och förklarats!")
