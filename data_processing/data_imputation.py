import logging

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

# Konfigurera loggning
logging.basicConfig(filename="data_imputation.log", level=logging.INFO)


def impute_missing_values(data, method="knn", k=5):
    """
    Fyller i saknade värden med antingen KNN-imputation eller medelvärde.
    """
    try:
        if method == "knn":
            imputer = KNNImputer(n_neighbors=k)
            imputed_data = pd.DataFrame(
                imputer.fit_transform(data), columns=data.columns
            )
        elif method == "mean":
            imputed_data = data.fillna(data.mean())
        else:
            logging.error("❌ Ogiltig metod angiven för imputering.")
            return None

        logging.info(f"✅ Saknade värden ifyllda med {method}-metoden.")
        return imputed_data
    except Exception as e:
        logging.error(f"❌ Fel vid imputering av saknade värden: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "price": [100, 200, np.nan, 400, 500],
            "volume": [1000, 1500, 2000, np.nan, 3000],
        }
    )

    imputed_df = impute_missing_values(df, method="knn")
    print("📢 Imputerad data:")
    print(imputed_df)
