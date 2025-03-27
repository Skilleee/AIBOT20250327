"""
train_rl.py

Tränar en RL-agent (ex. PPO) med hjälp av TradingEnv och stable_baselines3.
Sparar den tränade modellen till en fil.
"""

import sys
import os
# Lägg till projektets rotmapp i sys.path så att moduler i ai_learning hittas.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import pandas as pd
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# Försök importera TradingEnv från reinforcement_learning, annars definiera en fallback-version.
try:
    from ai_learning.reinforcement_learning import TradingEnv
except ModuleNotFoundError:
    import gym
    class TradingEnv(gym.Env):
        """
        Enkel fallback TradingEnv om reinforcement_learning inte finns.
        Action space: 0 = hold, 1 = buy, 2 = sell.
        Observation: nuvarande pris (float).
        """
        def __init__(self, data):
            super(TradingEnv, self).__init__()
            self.data = data.reset_index(drop=True)
            self.current_step = 0
            self.action_space = gym.spaces.Discrete(3)
            self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32)
        
        def reset(self):
            self.current_step = 0
            return np.array([self.data.iloc[0]["close"]], dtype=np.float32)
        
        def step(self, action):
            prev_price = self.data.iloc[self.current_step]["close"]
            self.current_step += 1
            done = self.current_step >= len(self.data) - 1
            current_price = self.data.iloc[self.current_step]["close"]
            reward = 0.0
            if action == 1:  # buy
                reward = current_price - prev_price
            elif action == 2:  # sell
                reward = prev_price - current_price
            return np.array([current_price], dtype=np.float32), reward, done, {}

# Konfigurera loggning
logging.basicConfig(
    filename="train_rl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Sätt ett seed för reproducibilitet
np.random.seed(42)

def train_rl_trading_agent(df: pd.DataFrame, timesteps: int = 100_000, model_path: str = "rl_trading_model.zip") -> PPO:
    """
    Tränar en RL-agent med PPO på TradingEnv och sparar modellen.
    
    Args:
        df (pd.DataFrame): DataFrame med kolumnerna "close", "momentum", "volume" (och eventuellt "return").
        timesteps (int): Antal träningssteg.
        model_path (str): Sökväg för att spara den tränade modellen.
        
    Returns:
        PPO: Den tränade modellen.
    """
    def make_env():
        return TradingEnv(data=df)

    # Skapa en vektoriserad miljö med DummyVecEnv
    env = DummyVecEnv([make_env])
    
    try:
        model = PPO("MlpPolicy", env, verbose=1, seed=42)
        logger.info(f"Startar RL-träning i {timesteps} steg...")
        model.learn(total_timesteps=timesteps)
        model.save(model_path)
        logger.info(f"✅ RL-modell tränad och sparad till {model_path}")
    except Exception as e:
        logger.error(f"❌ Fel under träning: {str(e)}")
        raise
    finally:
        env.close()
    
    return model

if __name__ == "__main__":
    # Exempeldata – se till att data har rätt kolumnnamn, t.ex. "close", "momentum", "volume"
    df = pd.DataFrame({
        "close": [101, 102, 103, 104, 105],
        "momentum": [0.1, -0.2, 0.05, 0.3, -0.1],
        "volume": [500, 600, 550, 700, 650],
    })

    # Träna modellen med färre tidsteg för teständamål
    train_rl_trading_agent(df, timesteps=10_000, model_path="rl_trading_model.zip")
