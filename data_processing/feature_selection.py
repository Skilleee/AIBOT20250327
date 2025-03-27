import logging
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.feature_selection import (SelectKBest, f_classif,
                                       mutual_info_regression)

# Konfigurera loggning
logging.basicConfig(filename="feature_selection.log", level=logging.INFO)


# Funktion för att välja de bästa funktionerna baserat på ANOVA F-test
def select_best_features_anova(X, y, k=5):
    """
    Väljer de bästa funktionerna med ANOVA F-test för klassificeringsproblem.
    """
    try:
        selector = SelectKBest(score_func=f_classif, k=k)
        selector.fit(X, y)
        selected_features = X.columns[selector.get_support()]
        logging.info(
            f"[{datetime.now()}] ✅ Valda bästa funktioner (ANOVA): {list(selected_features)}"
        )
        return selected_features
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid ANOVA feature selection: {str(e)}"
        )
        return None


# Funktion för att välja de bästa funktionerna med Mutual Information
def select_best_features_mutual_info(X, y, k=5):
    """
    Väljer de bästa funktionerna baserat på Mutual Information för regressionsproblem.
    """
    try:
        selector = SelectKBest(score_func=mutual_info_regression, k=k)
        selector.fit(X, y)
        selected_features = X.columns[selector.get_support()]
        logging.info(
            f"[{datetime.now()}] ✅ Valda bästa funktioner (Mutual Information): {list(selected_features)}"
        )
        return selected_features
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid Mutual Information feature selection: {str(e)}"
        )
        return None


# Funktion för att identifiera korrelerade funktioner och ta bort redundans
def remove_highly_correlated_features(X, threshold=0.9):
    """
    Tar bort funktioner som har hög korrelation (> threshold) för att minska redundans.
    """
    try:
        corr_matrix = X.corr()
        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        to_drop = [
            column
            for column in upper_triangle.columns
            if any(upper_triangle[column].abs() > threshold)
        ]
        reduced_X = X.drop(columns=to_drop)
        logging.info(
            f"[{datetime.now()}] ✅ Borttagna starkt korrelerade funktioner: {to_drop}"
        )
        return reduced_X
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid borttagning av starkt korrelerade funktioner: {str(e)}"
        )
        return X


# Exempelanrop
if __name__ == "__main__":
    np.random.seed(42)
    df = pd.DataFrame(
        np.random.rand(100, 10), columns=[f"feature_{i}" for i in range(10)]
    )
    target = np.random.randint(0, 2, size=100)

    selected_anova = select_best_features_anova(df, target)
    print(f"📊 ANOVA bästa funktioner: {selected_anova}")

    selected_mutual_info = select_best_features_mutual_info(df, target)
    print(f"📈 Mutual Information bästa funktioner: {selected_mutual_info}")

    reduced_df = remove_highly_correlated_features(df)
    print(
        f"🔍 Data efter borttagning av starkt korrelerade funktioner: {reduced_df.columns}"
    )
