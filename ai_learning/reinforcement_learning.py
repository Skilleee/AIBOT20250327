import logging
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
from stable_baselines3 import PPO

# Konfigurera loggning
logging.basicConfig(
    filename="reinforcement_learning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class TradingEnv(gym.Env):
    """
    En förbättrad förstärkningsinlärningsmiljö för trading.

    Observation: [close, momentum, volume, balance, holding]
    Actions:
        0 = HOLD
        1 = BUY (10% av balance)
        2 = SELL (sälj allt)
    Reward: Förändring i portföljvärde
    """

    metadata = {"render.modes": ["human"]}
class TradingEnv(gym.Env):
    def __init__(self, data: pd.DataFrame, initial_balance: float = 10_000):
        super(TradingEnv, self).__init__()
        self.data = data.reset_index(drop=True)  # Spara dataframe som en variabel
        self.initial_balance = initial_balance

        # Definiera action och observation space
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)

        # Interna variabler
        self.current_step = 0
        self.balance = float(self.initial_balance)
        self.holding = 0.0

        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def _get_obs(self) -> np.ndarray:
        row = self.data.iloc[self.current_step]
        return np.array([
            row["close"],
            row["momentum"],
            row["volume"],
            self.balance,
            self.holding
        ], dtype=np.float32)

    def reset(self, seed=None, options=None) -> tuple[np.ndarray, dict]:
        super().reset(seed=seed)
        self.current_step = 0
        self.balance = float(self.initial_balance)
        self.holding = 0.0
        logging.info("Miljön återställd: balance=%.2f, holding=%.2f", self.balance, self.holding)
        return self._get_obs(), {}

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict]:
        old_value = self._get_portfolio_value()
        self._take_action(action)

        self.current_step += 1
        terminated = self.current_step >= len(self.data) - 1
        truncated = False

        new_value = self._get_portfolio_value()
        reward = new_value - old_value

        logging.info("Steg: %d, Action: %d, Reward: %.2f, Portföljvärde: %.2f",
                     self.current_step, action, reward, new_value)

        obs = self._get_obs() if not terminated else np.zeros(self.observation_space.shape, dtype=np.float32)
        return obs, reward, terminated, truncated, {}

    def _take_action(self, action: int):
        price = self.data.iloc[self.current_step]["close"]
        if action == 1:  # BUY
            amount_to_spend = 0.1 * self.balance
            if amount_to_spend > 0:
                units = amount_to_spend / price
                self.holding += units
                self.balance -= amount_to_spend
                logging.debug("Köpte: %.4f enheter till pris %.2f", units, price)
        elif action == 2:  # SELL
            if self.holding > 0:
                self.balance += self.holding * price
                logging.debug("Sålde: %.4f enheter till pris %.2f", self.holding, price)
                self.holding = 0.0

    def _get_portfolio_value(self) -> float:
        price = self.data.iloc[self.current_step]["close"]
        return self.balance + self.holding * price

    def render(self):
        portfolio_value = self._get_portfolio_value()
        print(f"Steg: {self.current_step} | Balance: {self.balance:.2f} | Holding: {self.holding:.4f} | Portföljvärde: {portfolio_value:.2f}")

    def close(self):
        logging.info("Miljön stängs.")

if __name__ == "__main__":
    np.random.seed(42)
    data = pd.DataFrame({
        "close": np.cumsum(np.random.randn(1000) * 2 + 100),
        "momentum": np.random.randn(1000),
        "volume": np.random.randint(100, 1000, size=1000),
        "return": np.random.randn(1000) / 100,
    })

    env = TradingEnv(data, initial_balance=10_000)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10_000)
    model.save("rl_trading_model.zip")
    print("📢 RL-modell är tränad och sparad!")
