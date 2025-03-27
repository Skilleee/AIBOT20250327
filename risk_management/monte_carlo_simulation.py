import numpy as np
import logging

# Konfigurera loggning
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monte_carlo_simulation_normal(initial_value, mean_return, volatility, days=252, simulations=1000):
    """
    Normalfördelad Monte Carlo-simulering.
    Returnerar dict: {"expected_value": ..., "type": "normal", "simulations": ...}
    """
    try:
        results = []
        for _ in range(simulations):
            daily_returns = np.random.normal(mean_return / days, volatility / np.sqrt(days), days)
            price_series = initial_value * (1 + daily_returns).cumprod()
            results.append(price_series[-1])
        expected_value = np.mean(results)
        logging.info("✅ Normalfördelad Monte Carlo-simulering genomförd.")
        return {
            "expected_value": float(expected_value),
            "type": "normal",
            "simulations": simulations
        }
    except Exception as e:
        logging.error(f"❌ Fel vid normal simulering: {str(e)}")
        return {"expected_value": None, "type": "normal", "simulations": simulations}


def monte_carlo_simulation_historical(returns: np.ndarray, num_simulations=1000, forecast_steps=252) -> dict:
    """
    Historisk Monte Carlo-simulering.
    Returnerar dict: {"expected_value": ..., "type": "historical", "simulations": ..., "series": [...]}
    """
    try:
        last_price = 100
        simulations = []
        for _ in range(num_simulations):
            price_series = [last_price]
            for _ in range(forecast_steps):
                simulated_return = np.random.choice(returns)
                new_price = price_series[-1] * (1 + simulated_return)
                price_series.append(new_price)
            simulations.append(price_series)

        final_values = [series[-1] for series in simulations]
        expected_value = np.mean(final_values)
        logging.info("✅ Historisk Monte Carlo-simulering genomförd.")
        return {
            "expected_value": float(expected_value),
            "type": "historical",
            "simulations": num_simulations,
            "series": simulations
        }
    except Exception as e:
        logging.error(f"❌ Fel vid historisk simulering: {str(e)}")
        return {"expected_value": None, "type": "historical", "simulations": num_simulations, "series": []}


def ensemble_monte_carlo(initial_value, mean_return, volatility, historical_returns, days=252, simulations=1000, weight_normal=0.4, weight_historical=0.6):
    """
    Kombinerar normal och historisk Monte Carlo-simulering.
    Returnerar dict: {"ensemble_value": ..., "normal": {...}, "historical": {...}}
    """
    normal_result = monte_carlo_simulation_normal(initial_value, mean_return, volatility, days, simulations)
    historical_result = monte_carlo_simulation_historical(historical_returns, simulations, days)

    ev_normal = normal_result["expected_value"] or 0
    ev_hist = historical_result["expected_value"] or 0

    ensemble_value = weight_normal * ev_normal + weight_historical * ev_hist

    logging.info(f"📊 Ensemble-värde: {ensemble_value:.2f}")
    return {
        "ensemble_value": float(ensemble_value),
        "normal": normal_result,
        "historical": historical_result
    }


# Exempelanrop
if __name__ == "__main__":
    initial_value = 100000
    mean_return = 0.07
    volatility = 0.2
    historical_returns = np.array([0.001, -0.002, 0.003, 0.002, -0.001])

    result = ensemble_monte_carlo(initial_value, mean_return, volatility, historical_returns)
    print(f"📈 Ensemble framtida portföljvärde: {result['ensemble_value']:.2f}")
    print(f"  🔹 Normal: {result['normal']['expected_value']:.2f}")
    print(f"  🔹 Historisk: {result['historical']['expected_value']:.2f}")
