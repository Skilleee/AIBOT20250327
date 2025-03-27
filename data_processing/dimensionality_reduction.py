import logging

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# Konfigurera loggning
logging.basicConfig(filename="dimensionality_reduction.log", level=logging.INFO)


def reduce_dimensions(data, n_components=2):
    """
    Minskar antalet features med hjälp av PCA.
    """
    try:
        pca = PCA(n_components=n_components)
        reduced_data = pca.fit_transform(data)
        logging.info(f"✅ Datadimensioner reducerade till {n_components} komponenter.")
        return pd.DataFrame(
            reduced_data, columns=[f"PC{i+1}" for i in range(n_components)]
        )
    except Exception as e:
        logging.error(f"❌ Fel vid dimensionell reduktion: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "feature1": np.random.rand(100),
            "feature2": np.random.rand(100),
            "feature3": np.random.rand(100),
            "feature4": np.random.rand(100),
        }
    )

    reduced_df = reduce_dimensions(df, n_components=2)
    print("📢 Dimensionellt reducerad data:")
    print(reduced_df.head())
