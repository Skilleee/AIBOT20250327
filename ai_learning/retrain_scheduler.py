import schedule
import time
from ai_learning.retrain_rl import retrain_rl_agent_if_needed
from data_collection.market_data import fetch_forex_data

def start_retrain_schedule():
    def run_retrain_loop():
        df = fetch_forex_data("USD", "SEK", period="1mo")["history"]
        if df is not None and not df.empty:
            retrain_rl_agent_if_needed(
                df,
                current_model_path="rl_trading_model.zip",
                retrain_threshold_reward=50,
                retrain_timesteps=5000
            )

    # Schemalägg retrain varje måndag 06:00
    schedule.every().monday.at("06:00").do(run_retrain_loop)

    while True:
        schedule.run_pending()
        time.sleep(60)
