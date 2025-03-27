import logging

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model

# Konfigurera loggning
logging.basicConfig(filename="transfer_learning.log", level=logging.INFO)


def load_pretrained_model(base_model_path):
    """
    Laddar en förtränad AI-modell för finjustering på ny data.
    """
    try:
        base_model = keras.models.load_model(base_model_path)
        logging.info("✅ Förtränad modell laddad.")
        return base_model
    except Exception as e:
        logging.error(f"❌ Fel vid laddning av förtränad modell: {str(e)}")
        return None


def fine_tune_model(base_model, new_data, output_classes=2, learning_rate=0.001):
    """
    Finjusterar en befintlig AI-modell med ny marknadsdata.
    """
    try:
        feature_columns = [
            col for col in new_data.columns if col not in ["symbol", "date", "target"]
        ]
        X = new_data[feature_columns]
        y = new_data["target"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Skapa en ny output layer
        x = base_model.layers[-2].output  # Tar bort den gamla output-layern
        output_layer = Dense(output_classes, activation="softmax")(x)
        fine_tuned_model = Model(inputs=base_model.input, outputs=output_layer)

        fine_tuned_model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

        fine_tuned_model.fit(
            X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32
        )

        logging.info("✅ Modell finjusterad och tränad på ny data.")
        return fine_tuned_model
    except Exception as e:
        logging.error(f"❌ Fel vid finjustering av modellen: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    # Simulerad ny marknadsdata
    np.random.seed(42)
    new_data = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=500),
            "symbol": np.random.choice(["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"], 500),
            "momentum": np.random.randn(500),
            "volatility": np.random.rand(500),
            "sentiment": np.random.uniform(-1, 1, 500),
            "target": np.random.choice([0, 1], 500),  # 0 = Sälj, 1 = Köp
        }
    )

    base_model_path = "pretrained_model.h5"
    base_model = load_pretrained_model(base_model_path)

    if base_model:
        fine_tuned_model = fine_tune_model(base_model, new_data)
        print("📢 Modellen har finjusterats med ny marknadsdata!")
