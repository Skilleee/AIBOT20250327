import numpy as np

def ensemble_predictions(predictions_list: list) -> np.ndarray:
    """
    Exempel: Kombinera flera prediktioner genom medelvärdesaggregering.
    """
    ensemble_pred = np.mean(predictions_list, axis=0)
    return ensemble_pred

def make_final_decision(analysis_results: dict) -> str:
    """
    Exempel på en funktion som tar emot olika analysresultat (t.ex. prognoser, riskanalyser)
    och returnerar en textrekommendation eller beslut.
    """
    # Här kan du implementera egen logik för att vikta olika signaler.
    # Exempel:
    if analysis_results.get("arima_trend") == "upp" and analysis_results.get("risk_level") < 0.05:
        return "Rekommendation: Öka innehav."
    else:
        return "Rekommendation: Avvakta."