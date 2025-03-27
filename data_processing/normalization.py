import logging
from datetime import datetime
import numpy as np
from typing import Optional

# Konfigurera loggning
logging.basicConfig(
    filename="normalization.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def min_max_normalization(data: np.ndarray) -> Optional[np.ndarray]:
    """
    Normaliserar data med Min-Max scaling (skalar mellan 0 och 1).
    """
    try:
        data_min = np.min(data)
        data_max = np.max(data)
        if data_max == data_min:
            logger.warning(f"[{datetime.now()}] ⚠️ Alla värden är lika, returnerar en noll-array.")
            return np.zeros_like(data)
        normalized_data = (data - data_min) / (data_max - data_min)
        logger.info(f"[{datetime.now()}] ✅ Min-Max Normalisering genomförd.")
        return normalized_data
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid Min-Max normalisering: {str(e)}")
        return None

def z_score_standardization(data: np.ndarray) -> Optional[np.ndarray]:
    """
    Standardiserar data med hjälp av Z-score normalisering.
    """
    try:
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            logger.warning(f"[{datetime.now()}] ⚠️ Standardavvikelsen är 0, returnerar en noll-array.")
            return np.zeros_like(data)
        standardized_data = (data - mean) / std
        logger.info(f"[{datetime.now()}] ✅ Z-score Standardisering genomförd.")
        return standardized_data
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid Z-score standardisering: {str(e)}")
        return None

def winsorize_data(data: np.ndarray, limit: float = 0.05) -> Optional[np.ndarray]:
    """
    Hanterar outliers genom Winsorization (klipper extrema värden).
    """
    try:
        lower_bound = np.percentile(data, limit * 100)
        upper_bound = np.percentile(data, (1 - limit) * 100)
        winsorized_data = np.clip(data, lower_bound, upper_bound)
        logger.info(f"[{datetime.now()}] ✅ Winsorization genomförd med gräns {limit}.")
        return winsorized_data
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid Winsorization: {str(e)}")
        return None

def log_scale_data(data: np.ndarray) -> Optional[np.ndarray]:
    """
    Skalar data med en logaritmisk transformation för att hantera skevhet.
    """
    try:
        log_scaled_data = np.log1p(data)
        logger.info(f"[{datetime.now()}] ✅ Logaritmisk skalning genomförd.")
        return log_scaled_data
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid logaritmisk skalning: {str(e)}")
        return None

if __name__ == "__main__":
    sample_data = np.array([100, 200, 300, 400, 500, 1000, 5000])
    min_max_data = min_max_normalization(sample_data)
    print(f"📏 Min-Max Normaliserad data: {min_max_data}")
    z_score_data = z_score_standardization(sample_data)
    print(f"📊 Z-score Standardiserad data: {z_score_data}")
    winsorized_data = winsorize_data(sample_data)
    print(f"🔍 Winsoriserad data: {winsorized_data}")
    log_scaled_data = log_scale_data(sample_data)
    print(f"📈 Logaritmiskt skalad data: {log_scaled_data}")
