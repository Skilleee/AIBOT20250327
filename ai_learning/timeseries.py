import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

def forecast_arima(series: pd.Series, order=(1, 1, 1), forecast_steps=5) -> np.ndarray:
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_steps)
    return forecast.values

def forecast_lstm(series: np.ndarray, forecast_steps=5, epochs=50, batch_size=32) -> np.ndarray:
    scaler = MinMaxScaler(feature_range=(0, 1))
    series_scaled = scaler.fit_transform(series.reshape(-1, 1))
    
    def create_dataset(data, look_back=5):
        X, Y = [], []
        for i in range(len(data) - look_back):
            X.append(data[i:(i + look_back), 0])
            Y.append(data[i + look_back, 0])
        return np.array(X), np.array(Y)
    
    look_back = 5
    X, Y = create_dataset(series_scaled, look_back)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    model = Sequential()
    model.add(LSTM(50, input_shape=(look_back, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    es = EarlyStopping(monitor='loss', patience=5, verbose=1)
    model.fit(X, Y, epochs=epochs, batch_size=batch_size, verbose=0, callbacks=[es])
    
    # Gör framtida prognoser steg för steg
    last_sequence = series_scaled[-look_back:]
    predictions = []
    current_sequence = last_sequence.copy()
    for _ in range(forecast_steps):
        current_sequence_reshaped = current_sequence.reshape((1, look_back, 1))
        pred = model.predict(current_sequence_reshaped, verbose=0)
        predictions.append(pred[0, 0])
        current_sequence = np.append(current_sequence[1:], pred[0, 0])
    
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    return predictions
