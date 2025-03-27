import os
import logging
import pandas as pd
import numpy as np
from ai_learning.train_rl import train_rl_trading_agent
from ai_learning.backtest_rl import backtest_rl_agent

# Konfigurera loggning
logging.basicConfig(
    filename="automate_rl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_automated_pipeline(timesteps=100_000, model_path="rl_trading_model.zip"):
    """
    Automatiserar RL-träning och backtesting i en pipeline.
    """
    logging.info("🚀 Startar automatiserad RL-pipeline...")
    
    # 1️⃣ Hämta data (exempel: generera syntetisk data)
    np.random.seed(42)
    df = pd.DataFrame({
        "close": np.cumsum(np.random.randn(1000) * 2 + 100),
        "momentum": np.random.randn(1000),
        "volume": np.random.randint(100, 1000, size=1000),
    })
    
    # 2️⃣ Träna RL-agenten
    logging.info("🎯 Startar träning av RL-agent...")
    model = train_rl_trading_agent(df, timesteps=timesteps, model_path=model_path)
    
    # 3️⃣ Backtesta RL-agenten
    logging.info("🔄 Startar backtesting av RL-agent...")
    performance = backtest_rl_agent(model_path, df)
    
    # 4️⃣ Logga resultat
    logging.info(f"📊 Backtesting-resultat: {performance}")
    logging.info("✅ RL-pipeline slutförd!")

if __name__ == "__main__":
    run_automated_pipeline()
