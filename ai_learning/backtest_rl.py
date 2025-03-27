"""
backtest_rl.py

Backtestar en redan tränad RL-modell (ex. PPO) mot historisk data,
räknar ut PnL, etc.
"""

import os
import logging
import pandas as pd
import numpy as np
from stable_baselines3 import PPO
from ai_learning.reinforcement_learning import TradingEnv

# Konfigurera loggning
logging.basicConfig(
    filename="backtest_rl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def backtest_rl_agent(df: pd.DataFrame, model_path="rl_trading_model.zip"):
    """
    Backtestar en tränad RL-agent på historisk data.
    
    Args:
        df (pd.DataFrame): DataFrame med kolumner som "close", "momentum", "volume".
        model_path (str): Sökväg till den tränade RL-modellen.
    
    Returns:
        dict: {"reward": totalt_reward, "final_value": slutligt_portföljvärde}
    """

    if not isinstance(model_path, str):
        raise ValueError(f"❌ Model path måste vara en sträng, men fick: {type(model_path)}")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ RL-modellen hittades inte på {model_path}")

    logging.info(f"📥 Laddar RL-modell från: {os.path.abspath(model_path)}")
    print(f"📥 Laddar RL-modell från: {os.path.abspath(model_path)}")

    try:
        model = PPO.load(model_path)
    except Exception as e:
        logging.error(f"⚠️ Misslyckades att ladda RL-modellen: {str(e)}")
        raise

    # Initiera TradingEnv
    env = TradingEnv(data=df)

    obs, _ = env.reset()
    done = False
    total_reward = 0.0
    step = 0

    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward

        # Logga varje steg
        current_value = env._get_portfolio_value()
        msg = f"Steg {step:3d} | Action: {action} | Reward: {reward:.2f} | Portföljvärde: {current_value:.2f}"
        logging.info(msg)
        print(msg)
        step += 1

    final_value = env._get_portfolio_value()
    summary = f"✅ Backtest: Totalt reward = {total_reward:.2f}, slutligt portföljvärde = {final_value:.2f}"
    logging.info(summary)
    print(summary)

    return {"reward": total_reward, "final_value": final_value}

if __name__ == "__main__":
    # Exempel: Dummydata för test
    df = pd.DataFrame({
        "close": [100, 101, 102, 103, 104],
        "momentum": [0.1, 0.2, -0.1, 0.3, -0.2],
        "volume": [500, 400, 600, 550, 500],
    })

    result = backtest_rl_agent(df, model_path="rl_trading_model.zip")
