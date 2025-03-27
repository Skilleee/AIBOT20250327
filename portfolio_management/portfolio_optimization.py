import logging
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Konfigurera loggning
logging.basicConfig(filename="portfolio_optimization.log", level=logging.INFO)

def calculate_sharpe_ratio(returns: pd.DataFrame, weights: np.ndarray, risk_free_rate: float = 0.0) -> float:
    """
    Beräknar Sharpe Ratio för en portfölj med givna vikter.
    Antagande: Dagliga avkastningar, ca 252 handelsdagar/år.
    """
    freq = 252
    annual_return = (returns.mean() * freq).dot(weights)
    annual_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * freq, weights)))
    if annual_volatility == 0:
        return 0.0
    return (annual_return - risk_free_rate) / annual_volatility

def calculate_sortino_ratio(returns: pd.DataFrame, weights: np.ndarray, risk_free_rate: float = 0.0) -> float:
    """
    Beräknar Sortino Ratio för en portfölj med givna vikter.
    Endast negativa avkastningar inkluderas i beräkning av risk.
    """
    freq = 252
    annual_return = (returns.mean() * freq).dot(weights)

    # Filtrera dagar med negativ avkastning
    negative_returns = returns[returns < 0].fillna(0)
    if not negative_returns.empty:
        downside_std = np.sqrt(
            np.dot(weights.T, np.dot(negative_returns.cov() * freq, weights))
        )
    else:
        # Om inga negativa avkastningar => risk ~ 0
        downside_std = 1e-9

    return (annual_return - risk_free_rate) / downside_std


def optimize_portfolio(
    returns: pd.DataFrame,
    risk_tolerance: float = 0.5,
    method: str = "min_volatility",
    risk_free_rate: float = 0.0,
) -> dict:
    """
    Optimerar portföljens viktning baserat på vald metod:

    Metoder som stöds:
      - "min_volatility": Minimera portföljens volatilitet (originalfunktionen).
      - "max_sharpe": Maximera Sharpe Ratio.
      - "max_sortino": Maximera Sortino Ratio.

    Parametrar:
      returns: DataFrame med historiska avkastningar (rader = dagar, kolumner = aktier).
      risk_tolerance (RESERVERAD, använd i framtiden för extra logik).
      method: "min_volatility", "max_sharpe", "max_sortino".
      risk_free_rate: Riskfri ränta (används i Sharpe/Sortino).
    
    Returnerar:
      En ordbok { \"Aktie\": vikt } med portföljallokeringen.
    """
    try:
        # Beräkna kovariansmatris
        cov_matrix = returns.cov()
        num_assets = len(returns.columns)

        # Startgissning: jämn vikt
        initial_weights = np.ones(num_assets) / num_assets

        # -- Mål-funktioner --
        # Minimera volatilitet (original)
        def portfolio_volatility(weights: np.ndarray) -> float:
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        # Maximera Sharpe => minimera -Sharpe
        def negative_sharpe(weights: np.ndarray) -> float:
            return -calculate_sharpe_ratio(returns, weights, risk_free_rate)

        # Maximera Sortino => minimera -Sortino
        def negative_sortino(weights: np.ndarray) -> float:
            return -calculate_sortino_ratio(returns, weights, risk_free_rate)

        # Välj optimeringsmetod
        if method == "min_volatility":
            objective = portfolio_volatility
        elif method == "max_sharpe":
            objective = negative_sharpe
        elif method == "max_sortino":
            objective = negative_sortino
        else:
            logging.warning(f"Okänd metod '{method}', fallback: min_volatility.")
            objective = portfolio_volatility

        # Vikt-summan = 1
        constraints = ({"type": "eq", "fun": lambda w: np.sum(w) - 1},)
        # Varje vikt mellan 0% och 100%
        bounds = tuple((0, 1) for _ in range(num_assets))

        # Anropa optimering
        result = minimize(
            objective,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        if not result.success:
            logging.warning(f"Optimeringsvarning: {result.message}")

        optimized_weights = result.x
        optimized_portfolio = dict(zip(returns.columns, optimized_weights))

        logging.info(f"✅ Portföljoptimering klar (metod={method}).")
        return optimized_portfolio
    except Exception as e:
        logging.error(f"❌ Fel vid portföljoptimering: {str(e)}")
        return {}

# Exempelanrop
if __name__ == "__main__":
    # Simulerad data för 4 aktier
    np.random.seed(42)
    stock_returns = pd.DataFrame(
        np.random.randn(100, 4) / 100, columns=["AAPL", "TSLA", "NVDA", "MSFT"]
    )

    # 1) Minimera volatilitet (original)
    min_vol_portfolio = optimize_portfolio(stock_returns, method="min_volatility")
    print("🔹 Minsta volatilitet:", min_vol_portfolio)

    # 2) Maximera Sharpe Ratio
    max_sharpe_portfolio = optimize_portfolio(
        stock_returns, method="max_sharpe", risk_free_rate=0.01
    )
    print("\n🔹 Max Sharpe Ratio:", max_sharpe_portfolio)

    # 3) Maximera Sortino Ratio
    max_sortino_portfolio = optimize_portfolio(
        stock_returns, method="max_sortino", risk_free_rate=0.01
    )
    print("\n🔹 Max Sortino Ratio:", max_sortino_portfolio)
