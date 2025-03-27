"""
ai_learning/trading_rl_agent.py

Tränar en RL-agent med PPO på TradingEnv och sparar den tränade modellen till en fil.
"""

import logging
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from ai_learning.reinforcement_learning import TradingEnv

# Konfigurera loggning
logging.basicConfig(
    filename="train_rl_agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def train_rl_trading_agent(df: pd.DataFrame, timesteps: int = 100_000, model_path: str = "rl_trading_model.zip") -> PPO:
    """
    Tränar en RL-agent med PPO på TradingEnv.

    Args:
        df (pd.DataFrame): DataFrame med kolumnerna "close", "momentum", "volume" (och eventuellt "return").
        timesteps (int): Antal timesteps att träna RL-agenten.
        model_path (str): Filnamn eller sökväg där den tränade modellen ska sparas.

    Returns:
        PPO: Den tränade PPO-modellen.
    """
    def make_env():
        return TradingEnv(data=df)

    # Skapa en vektoriserad miljö med DummyVecEnv
    env = DummyVecEnv([make_env])
    logging.info("Startar träning av RL-agenten med %d timesteps...", timesteps)

    # Initiera PPO-modellen med MlpPolicy
    model = PPO("MlpPolicy", env, verbose=1)

    # Träna modellen
    model.learn(total_timesteps=timesteps)
    logging.info("Träningen klar, sparar modellen till %s", model_path)

    # Spara den tränade modellen
    model.save(model_path)
    logging.info("✅ RL-modell tränad och sparad till %s", model_path)

    # Stäng miljön för att frigöra resurser
    env.close()

    return model

if __name__ == "__main__":
    # Exempel: Generera simulerad data
    import numpy as np
    np.random.seed(42)
    data = pd.DataFrame({
        "close": np.cumsum(np.random.randn(1000) * 2 + 100),
        "momentum": np.random.randn(1000),
        "volume": np.random.randint(100, 1000, size=1000),
        "return": np.random.randn(1000) / 100,
    })

    # Träna RL-agenten med 10 000 timesteps och spara modellen
    train_rl_trading_agent(data, timesteps=10_000, model_path="rl_trading_model.zip")
