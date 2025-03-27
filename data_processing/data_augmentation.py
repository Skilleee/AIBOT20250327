import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="data_augmentation.log", level=logging.INFO)


def generate_synthetic_data(data, num_samples=100):
    """
    Skapar syntetiska datapunkter med bootstrapping.
    """
    try:
        synthetic_data = data.sample(n=num_samples, replace=True).reset_index(drop=True)
        logging.info(f"✅ Genererade {num_samples} syntetiska datapunkter.")
        return synthetic_data
    except Exception as e:
        logging.error(f"❌ Fel vid skapande av syntetisk data: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "price": np.random.randn(500) * 10 + 100,
            "volume": np.random.randint(1000, 5000, 500),
        }
    )

    augmented_df = generate_synthetic_data(df, num_samples=200)
    print("📢 Syntetisk data:")
    print(augmented_df.head())
