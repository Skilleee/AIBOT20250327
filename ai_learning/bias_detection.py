import logging

import numpy as np
import pandas as pd
from sklearn.utils import resample

# Konfigurera loggning
logging.basicConfig(filename="bias_detection.log", level=logging.INFO)


def detect_class_imbalance(y):
    """
    Identifierar obalans i dataklasser och varnar om modellen är partisk.
    """
    try:
        class_distribution = y.value_counts(normalize=True)
        logging.info(f"✅ Klassfördelning: {class_distribution}")
        if class_distribution.min() < 0.1:
            logging.warning("⚠️ Möjlig klassobalans upptäckt!")
        return class_distribution
    except Exception as e:
        logging.error(f"❌ Fel vid klassobalansdetektion: {str(e)}")
        return None


def apply_data_resampling(X, y):
    """
    Hanterar klassobalans genom att upp- eller nedprova datasetet.
    """
    try:
        df = pd.concat([X, y], axis=1)
        majority_class = df[y.name].mode()[0]
        df_majority = df[df[y.name] == majority_class]
        df_minority = df[df[y.name] != majority_class]

        df_minority_upsampled = resample(
            df_minority, replace=True, n_samples=len(df_majority), random_state=42
        )
        balanced_df = pd.concat([df_majority, df_minority_upsampled])

        logging.info("✅ Dataresampling genomförd för att minska bias.")
        return balanced_df.drop(columns=[y.name]), balanced_df[y.name]
    except Exception as e:
        logging.error(f"❌ Fel vid dataresampling: {str(e)}")
        return None, None


# Exempelanrop
if __name__ == "__main__":
    np.random.seed(42)
    simulated_y = pd.Series(np.random.choice([0, 1], p=[0.9, 0.1], size=1000))

    class_distribution = detect_class_imbalance(simulated_y)
    print(f"📊 Klassfördelning: {class_distribution}")

    simulated_X = pd.DataFrame(
        np.random.randn(1000, 5), columns=[f"Feature_{i}" for i in range(5)]
    )
    balanced_X, balanced_y = apply_data_resampling(simulated_X, simulated_y)
    print(f"🔄 Resamplat dataset: {len(balanced_X)} observationer")
