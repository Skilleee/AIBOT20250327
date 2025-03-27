import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from ai_learning.trading_rl_agent import train_rl_trading_agent
from ai_learning.backtest_rl import backtest_rl_agent


def log_rl_training_result(model_name, reward, final_value, notes=""):
    """Loggar träningsresultat till training_history.csv"""
    log_file = "training_history.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "timestamp": timestamp,
        "model_name": model_name,
        "reward": reward,
        "final_value": final_value,
        "notes": notes
    }

    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df = df.tail(50)  # Behåll endast senaste 50 rader
    else:
        df = pd.DataFrame([row])

    df.to_csv(log_file, index=False)


def generate_training_history_plot():
    """Skapar träningshistorik-graf och sparar som PNG"""
    log_file = "training_history.csv"
    if not os.path.exists(log_file):
        print("⚠️ Inget träningslogg hittat för att skapa graf.")
        return

    df = pd.read_csv(log_file)

    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["reward"], marker="o", label="Reward")
    plt.plot(df["timestamp"], df["final_value"], marker="x", label="Final Portfolio Value")
    plt.xticks(rotation=45)
    plt.xlabel("Datum")
    plt.ylabel("Värde")
    plt.title("📈 RL-träningens historik")
    plt.legend()
    plt.tight_layout()
    plt.savefig("training_history_plot.png")
    plt.close()
    print("✅ Sparade träningsgraf som training_history_plot.png")


def retrain_rl_agent_if_needed(
    df: pd.DataFrame,
    current_model_path="rl_trading_model.zip",
    retrain_threshold_reward=50,
    retrain_timesteps=5000
):
    """
    Backtestar aktuell RL-modell och tränar om den vid låg reward.
    """
    print("\n🔁 Startar RL-retrain-loop...")

    # Om ingen befintlig modell finns, träna från början
    if not os.path.exists(current_model_path):
        print("⚠️ Ingen befintlig RL-modell hittad, tränar ny från början.")
        train_rl_trading_agent(df, timesteps=retrain_timesteps, model_path=current_model_path)
        return

    # Backtesta aktuell modell
    result = backtest_rl_agent(df, model_path=current_model_path)
    reward = float(result["reward"])
    final_value = float(result["final_value"])

    print(f"📊 Backtest-resultat: Reward={reward:.2f}, Portföljvärde={final_value:.2f}")

    # Logga och rita graf
    log_rl_training_result(current_model_path, reward, final_value, notes="Auto-retrain check")
    generate_training_history_plot()

    # Avgör om retraining krävs
    if reward < retrain_threshold_reward:
        print("🔄 Reward under tröskel – tränar om RL-agent...")
        backup_path = current_model_path.replace(".zip", "_backup.zip")
        shutil.copy(current_model_path, backup_path)
        print(f"📦 Backup sparad: {backup_path}")

        train_rl_trading_agent(df, timesteps=retrain_timesteps, model_path=current_model_path)
        print(f"✅ RL-agenten tränades om och sparades till {current_model_path}")
    else:
        print("✅ RL-agenten presterar tillräckligt bra – ingen retraining behövs.")


def retrain_rl_agent(df, timesteps=3000, model_path="rl_trading_model.zip"):
    """Extern wrapper som används i main.py"""
    retrain_rl_agent_if_needed(df, current_model_path=model_path, retrain_timesteps=timesteps)
