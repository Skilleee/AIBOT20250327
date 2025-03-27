import numpy as np
from arch import arch_model

def forecast_garch(returns: np.ndarray, forecast_steps=5) -> np.ndarray:
    am = arch_model(returns, vol='Garch', p=1, q=1)
    res = am.fit(disp='off')
    forecasts = res.forecast(horizon=forecast_steps)
    variance_forecast = forecasts.variance.iloc[-1].values
    return variance_forecast
