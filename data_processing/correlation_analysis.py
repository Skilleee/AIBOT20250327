import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Konfigurera loggning
logging.basicConfig(filename="correlation_analysis.log", level=logging.INFO)


def analyze_correlation(data):
    """
    Analyserar korrelation mellan variabler i datasetet.
    """
    try:
        correlation_matrix = data.corr()
        logging.info("✅ Korrelation mellan features analyserad.")
        return correlation_matrix
    except Exception as e:
        logging.error(f"❌ Fel vid korrelationsanalys: {str(e)}")
        return None


def plot_correlation_matrix(correlation_matrix):
    """
    Visualiserar korrelation mellan variabler.
    """
    try:
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Feature Correlation Matrix")
        plt.show()
        logging.info("✅ Korrelationsmatris plottad.")
    except Exception as e:
        logging.error(f"❌ Fel vid plottning av korrelationsmatris: {str(e)}")


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "feature1": np.random.rand(100),
            "feature2": np.random.rand(100),
            "feature3": np.random.rand(100) * 0.5 + np.random.rand(100) * 0.5,
        }
    )

    correlation_matrix = analyze_correlation(df)
    print("📢 Korrelationer mellan features:")
    print(correlation_matrix)
    plot_correlation_matrix(correlation_matrix)
