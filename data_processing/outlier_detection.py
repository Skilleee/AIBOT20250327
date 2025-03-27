import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="outlier_detection.log", level=logging.INFO)


def detect_outliers(data, method="zscore", threshold=3):
    """
    Identifierar outliers i datasetet baserat på vald metod.
    """
    try:
        if method == "zscore":
            z_scores = np.abs((data - data.mean()) / data.std())
            outliers = data[(z_scores > threshold).any(axis=1)]
        elif method == "iqr":
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[
                ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)
            ]
        else:
            logging.error("❌ Ogiltig metod angiven för outlier-detektering.")
            return None

        logging.info(f"✅ Identifierade {len(outliers)} outliers i datasetet.")
        return outliers
    except Exception as e:
        logging.error(f"❌ Fel vid identifiering av outliers: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "price": [100, 200, 300, 400, 5000],  # Outlier på 5000
            "volume": [1000, 1500, 2000, 2500, 3000],
        }
    )

    outliers_df = detect_outliers(df, method="iqr")
    print("📢 Identifierade outliers:")
    print(outliers_df)
