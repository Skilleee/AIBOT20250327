import logging
import random
import time

# Konfigurera loggning
logging.basicConfig(filename="live_trading_monitor.log", level=logging.INFO)


def fetch_real_time_data(symbols):
    """
    Simulerar hämtning av realtidsdata för en lista av aktier.
    """
    try:
        data = {symbol: round(random.uniform(100, 500), 2) for symbol in symbols}
        logging.info(f"✅ Realtidsdata hämtad: {data}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av realtidsdata: {str(e)}")
        return {}


def detect_abnormal_movements(real_time_prices, threshold=2.5):
    """
    Identifierar ovanliga prisrörelser baserat på en standardavvikelsers tröskel.
    """
    try:
        price_changes = {
            symbol: round(random.uniform(-3, 3), 2)
            for symbol in real_time_prices.keys()
        }
        alerts = {
            symbol: change
            for symbol, change in price_changes.items()
            if abs(change) > threshold
        }
        if alerts:
            logging.warning(f"⚠️ Ovanliga marknadsrörelser upptäckta: {alerts}")
        return alerts
    except Exception as e:
        logging.error(f"❌ Fel vid analys av marknadsrörelser: {str(e)}")
        return {}


def live_monitoring(symbols, interval=30):
    """
    Kontinuerligt övervakar realtidsmarknaden och identifierar anomalier.
    """
    while True:
        logging.info("🔍 Övervakar marknadsrörelser i realtid...")
        real_time_prices = fetch_real_time_data(symbols)
        alerts = detect_abnormal_movements(real_time_prices)
        if alerts:
            logging.info(f"🚨 Marknadslarm: {alerts}")
        time.sleep(interval)


# Exempelanrop
if __name__ == "__main__":
    symbols_to_monitor = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"]
    logging.info("🚀 Startar Live Trading Monitor...")
    live_monitoring(symbols_to_monitor)
