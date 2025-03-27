import pandas as pd
import numpy as np
from stable_baselines3 import PPO
from ai_learning.reinforcement_learning import TradingEnv
import time


def visualize_agent_behavior(model_path: str, df: pd.DataFrame):
    """
    Visualiserar hur en tränad RL-agent agerar steg för steg på ny data.

    Args:
        model_path (str): Sökväg till den tränade modellen (ex. "rl_trading_model.zip").
        df (pd.DataFrame): DataFrame med historiska data (close, momentum, volume).
    """
    # Ladda modellen
    model = PPO.load(model_path)

    # Initiera miljön
    env = TradingEnv(data=df)
    obs, _ = env.reset()

    print("\n📈 STARTAR VISUALISERING AV AGENTENS BESLUT")
    print("=" * 60)
    done = False
    step = 0

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        # Visualisering i konsolen
        print(f"Steg {step:3d} | Action: {action} | Reward: {reward:8.2f} | Portföljvärde: {env._get_portfolio_value():.2f}")

        time.sleep(0.2)
        step += 1

    env.close()
    print("=" * 60)
    print("✅ VISUALISERING SLUTFÖRD")


if __name__ == "__main__":
    # Dummydata för demo – byt till riktig marknadsdata för test
    np.random.seed(42)
    df = pd.DataFrame({
        "close": np.cumsum(np.random.randn(50) * 2 + 100),
        "momentum": np.random.randn(50),
        "volume": np.random.randint(100, 1000, size=50),
    })

    visualize_agent_behavior("rl_trading_model.zip", df)
