import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="data_preprocessing.log", level=logging.INFO)


def clean_and_normalize_data(data):
    """
    Rensar och normaliserar datasetet.
    """
    try:
        # Hantera saknade värden
        data = data.dropna()

        # Normalisera data
        for col in data.select_dtypes(include=[np.number]):
            data[col] = (data[col] - data[col].mean()) / data[col].std()

        logging.info("✅ Data rensad och normaliserad.")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid dataförberedelse: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {"price": [100, 200, 300, 400, 500], "volume": [1000, 1500, 2000, 2500, 3000]}
    )
    processed_df = clean_and_normalize_data(df)
    print("📢 Förberedd data:")
    print(processed_df)
