import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="data_cleaning.log", level=logging.INFO)


def clean_data(data):
    """
    Rensar datasetet genom att hantera saknade värden, outliers och dubbletter.
    """
    try:
        # Ta bort dubbletter
        data = data.drop_duplicates()

        # Hantera saknade värden genom att fylla i med medianvärden
        data = data.fillna(data.median())

        # Ta bort outliers baserat på Z-score
        z_scores = np.abs((data - data.mean()) / data.std())
        data = data[(z_scores < 3).all(axis=1)]

        logging.info(
            "✅ Data har rensats från dubbletter, outliers och saknade värden."
        )
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid datarensning: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad data
    df = pd.DataFrame(
        {
            "price": [100, 200, np.nan, 300, 400, 5000],  # Outlier på 5000
            "volume": [1000, 1500, 2000, np.nan, 2500, 3000],
        }
    )

    cleaned_df = clean_data(df)
    print("📢 Rensad data:")
    print(cleaned_df)
