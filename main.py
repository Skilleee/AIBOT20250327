import os
import logging
import threading
import argparse
import pandas as pd
import numpy as np
import schedule
import time
from datetime import datetime

from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Ange tidszon
os.environ['TZ'] = 'Europe/Stockholm'
time.tzset()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Egna imports
from ai_decision_engine.optimal_entry_exit import optimal_entry_exit_strategy, generate_entry_exit_dataframe, plot_entry_exit_signals
from ai_decision_engine.strategy_generation import generate_momentum_strategy
from data_collection.market_data import fetch_forex_data
from data_collection.sentiment_analysis import analyze_sentiment
from data_collection.macro_data import fetch_macro_data
from data_collection.news_analysis import fetch_and_analyze_news, get_recent_headlines
from data_processing.normalization import min_max_normalization
from data_processing.volatility_analysis import calculate_daily_volatility
# Vi tar bort den ursprungliga generate_trading_signals då vi skapar en egen signalslista
#from live_trading.live_signal_generator import generate_trading_signals
from live_trading.telegram_signal_sender import send_telegram_signal
from portfolio_management.rebalancing import rebalancing
from portfolio_management.hedge_strategy import hedge_strategy
from portfolio_management.portfolio_data_loader import fetch_all_portfolios
from reports.generate_report import generate_pdf_report
from reports.weekly_market_report import generate_weekly_market_report
from reports.macro_event_impact import generate_macro_event_impact_report
from reports.monthly_performance_report import send_monthly_report
from notifications.telegram_bot import (
    send_ai_recommendations,
    send_pdf_report_to_telegram,
    send_telegram_message,
    send_chart_to_telegram
)
from risk_management.adaptive_stop_loss import adaptive_stop_loss
from risk_management.value_at_risk import calculate_var
from risk_management.monte_carlo_simulation import monte_carlo_simulation_normal as monte_carlo_simulation
from utils.process_manager import manage_processes
from ai_learning.retrain_scheduler import start_retrain_schedule
from ai_learning.retrain_rl import retrain_rl_agent
from ai_learning.backtest_rl import backtest_rl_agent
from stable_baselines3 import PPO

parser = argparse.ArgumentParser()
parser.add_argument("--force-retrain", action="store_true", help="Tvinga retraining av RL-agent")
parser.add_argument("--no-report", action="store_true", help="Skippa PDF-rapportgenerering")
parser.add_argument("--test-mode", action="store_true", help="Aktivera testläge")
args = parser.parse_args()

# Hjälpfunktion: Konvertera värdesträngar till float
def convert_value(value_str):
    try:
        value_str = value_str.replace("kr", "").strip().replace(" ", "").replace(",", ".")
        return float(value_str)
    except Exception:
        return 0.0

# Hjälpfunktion: Beräkna dagliga avkastningar (returns) från prisdata
def compute_returns(prices: np.ndarray) -> np.ndarray:
    # Avkastning: (pris_t+1 - pris_t) / pris_t
    return np.diff(prices) / prices[:-1]

def daily_ai_report():
    logging.info("🚀 Startar daglig AI-rutin...")
    try:
        trade_log = pd.DataFrame()  # Tom handelslogg om ingen finns

        # Hämta portföljdata och välj "Investeringskonto" om möjligt
        portfolio_data = fetch_all_portfolios()
        if "Investeringskonto" in portfolio_data and not portfolio_data["Investeringskonto"].empty:
            portfolio_df = portfolio_data["Investeringskonto"]
        else:
            portfolio_df = next((df for df in portfolio_data.values() if not df.empty), pd.DataFrame())

        # Mappa om portföljdata om nödvändiga kolumner saknas
        if not (("symbol" in portfolio_df.columns) and ("allocation" in portfolio_df.columns)):
            if "Ticker" in portfolio_df.columns:
                portfolio_df["symbol"] = portfolio_df["Ticker"]
            if "Värde (SEK)" in portfolio_df.columns:
                portfolio_df["value_numeric"] = portfolio_df["Värde (SEK)"].apply(convert_value)
                total_value = portfolio_df["value_numeric"].sum()
                if total_value > 0:
                    portfolio_df["allocation"] = portfolio_df["value_numeric"] / total_value
                else:
                    portfolio_df["allocation"] = 0.0

        if "symbol" in portfolio_df.columns and "allocation" in portfolio_df.columns:
            rebalanced_df = rebalancing(portfolio_df.copy())
        else:
            logging.error("Portföljdata saknar nödvändiga kolumner ('symbol', 'allocation') för rebalansering.")
            rebalanced_df = None

        pdf_path = generate_pdf_report(trade_log, rebalanced_df=rebalanced_df)
        send_ai_recommendations()
        send_pdf_report_to_telegram(pdf_path)

        forex_result = fetch_forex_data("USD", "SEK", period="1mo")
        df = forex_result.get("history")
        if df is not None and not df.empty:
            optimal_entry = optimal_entry_exit_strategy({"prices": df["Close"]})
            logging.info(f"Optimal entry/exit: {optimal_entry}")
            plot_entry_exit_signals(generate_entry_exit_dataframe(df["Close"]))
            chart_file = "charts/entry_exit_plot_" + datetime.now().strftime("%Y%m%d") + ".png"
            send_chart_to_telegram(chart_file, caption=f"Entry/Exit-signal ({datetime.today().date()})")

        logging.info("✅ Daglig AI-rapport skickad.")
    except Exception as e:
        logging.error(f"Fel i daglig AI-rutin: {str(e)}")

def weekly_summary():
    try:
        macro_report_data = {
            "sp500": 2.1,
            "nasdaq": 1.8,
            "tech_sector": 2.5,
            "sentiment": "Negativ",
            "event": "Fed höjde räntan med 0.25%"
        }
        report = generate_weekly_market_report(macro_report_data)
        if report:
            send_telegram_message(report)
            with open("weekly_report.pdf", "w") as f:
                f.write(report)
            send_pdf_report_to_telegram("weekly_report.pdf")
    except Exception as e:
        logging.error(f"Fel i veckorapport: {str(e)}")

def monthly_summary():
    logging.info("🗓️ Genererar månadsrapport...")
    try:
        example_data = {
            "Investeringskonto": {
                "portfolio_return": 5.2,
                "sp500": 4.3,
                "best_performer": "AAPL",
                "best_return": 8.1,
                "worst_performer": "TSLA",
                "worst_return": -2.3,
            },
            "Pension": {
                "portfolio_return": 3.1,
                "sp500": 4.3,
                "best_performer": "MSFT",
                "best_return": 6.5,
                "worst_performer": "XACT Norden",
                "worst_return": -1.4,
            }
        }
        send_monthly_report(example_data)
    except Exception as e:
        logging.error(f"❌ Fel vid månadsrapport: {str(e)}")

def monthly_check_and_run():
    if datetime.today().day == 1:
        monthly_summary()

def main():
    logging.info("🚀 AI Trading Bot startar...")

    if not args.test_mode:
        threading.Thread(target=start_retrain_schedule, daemon=True).start()
        schedule.every().day.at("08:00").do(daily_ai_report)
        schedule.every().monday.at("08:05").do(weekly_summary)
        schedule.every().day.at("08:10").do(monthly_check_and_run)

    # RL-modell: kontrollera om filen "rl_trading_model.zip" finns
    rl_model_path = "rl_trading_model.zip"
    if os.path.exists(rl_model_path):
        try:
            rl_model = PPO.load(rl_model_path)
            logging.info("✅ RL-modell laddad")
        except Exception as e:
            logging.warning(f"Fel vid laddning av RL-modell: {str(e)}")
            rl_model = None
    else:
        logging.warning(f"Ingen RL-modell hittad: Filen '{rl_model_path}' existerar inte.")
        rl_model = None

    try:
        forex_result = fetch_forex_data("USD", "SEK", period="1mo")
        df = forex_result.get("history")
        if df is None or df.empty:
            logging.error("Ingen valutahistorik hittad")
            return

        # Konvertera prisdata till en float-array
        prices = df["Close"].values.astype(np.float32)
        # Beräkna dagliga avkastningar istället för att använda priser direkt
        returns = compute_returns(prices)

        portfolio_data = fetch_all_portfolios()
        if "Investeringskonto" in portfolio_data and not portfolio_data["Investeringskonto"].empty:
            portfolio_df = portfolio_data["Investeringskonto"]
        else:
            portfolio_df = next((df for df in portfolio_data.values() if not df.empty), pd.DataFrame())

        if not (("symbol" in portfolio_df.columns) and ("allocation" in portfolio_df.columns)):
            if "Ticker" in portfolio_df.columns:
                portfolio_df["symbol"] = portfolio_df["Ticker"]
            if "Värde (SEK)" in portfolio_df.columns:
                portfolio_df["value_numeric"] = portfolio_df["Värde (SEK)"].apply(convert_value)
                total_value = portfolio_df["value_numeric"].sum()
                if total_value > 0:
                    portfolio_df["allocation"] = portfolio_df["value_numeric"] / total_value
                else:
                    portfolio_df["allocation"] = 0.0

        headlines = get_recent_headlines(limit=15)
        sentiment = analyze_sentiment(texts=headlines)
        macro_data = fetch_macro_data()
        news_sentiment = fetch_and_analyze_news("stock market")

        normalized_data = min_max_normalization(prices)
        volatility = calculate_daily_volatility(prices)

        df_input = pd.DataFrame({"close": normalized_data})
        strategy_dict = generate_momentum_strategy(df_input, sentiment, macro_data)
        logging.info(f"Momentum-strategi: {strategy_dict}")
        optimal_entry = optimal_entry_exit_strategy({"prices": df["Close"]})
        logging.info(f"Optimal entry/exit: {optimal_entry}")

        # Använd de dagliga avkastningarna för riskberäkning
        calculate_var(returns)
        monte_carlo_simulation(100000, 0.07, 0.2)

        if "symbol" in portfolio_df.columns and "allocation" in portfolio_df.columns:
            rebalanced = rebalancing(portfolio_df)
            hedge_strategy(rebalanced)
        else:
            logging.error("Portföljdata saknar nödvändiga kolumner ('symbol', 'allocation') för rebalansering.")

        if not args.no_report:
            generate_pdf_report(
                trade_log=None,
                filename=None,
                rl_backtest_result=None,
                adjusted_assets=None,
                rebalanced_df=rebalanced if "symbol" in portfolio_df.columns and "allocation" in portfolio_df.columns else None
            )
            dummy_macro_data = {
                "sp500": 2.1,
                "nasdaq": 1.8,
                "tech_sector": 2.5,
                "sentiment": "Negativ",
                "event": "Fed höjde räntan med 0.25%"
            }
            generate_weekly_market_report(dummy_macro_data)
            generate_macro_event_impact_report(dummy_macro_data)

        if not args.test_mode:
            if rl_model:
                obs = np.array([df.iloc[-1]["Close"], 0.0, 0.0, 10000.0, 0.0], dtype=np.float32)
                rl_action, _ = rl_model.predict(obs, deterministic=True)
                # Skapa en signalslista manuellt (eftersom vi inte använder den ursprungliga generate_trading_signals)
                signals = [f"Makrodata: Indicator={macro_data.get('indicator', 'N/A')}, Value={macro_data.get('value', 'N/A')}"]
                signals.append(f"RL-agent action: {rl_action}")
                message = "📢 Trading Signal:\n" + "\n".join(signals)
                send_telegram_signal(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
            manage_processes(tasks=[])

        logging.info("✅ Bot körning avslutad korrekt")

        if not args.test_mode:
            while True:
                schedule.run_pending()
                time.sleep(60)

    except Exception as e:
        logging.error(f"Fel i huvudloopen: {str(e)}")

# Hjälpfunktion för att beräkna dagliga avkastningar
def compute_returns(prices: np.ndarray) -> np.ndarray:
    return np.diff(prices) / prices[:-1]

if __name__ == "__main__":
    main()
