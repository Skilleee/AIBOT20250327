import logging
from datetime import datetime

import requests

# Konfigurera loggning
logging.basicConfig(filename="api_handler.log", level=logging.INFO)

# API-konfiguration
AVANZA_API_URL = "https://www.avanza.se/_api/market"
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"
ALPACA_API_URL = "https://paper-api.alpaca.markets/v2"

# API-nycklar (ersätt med riktiga nycklar om nödvändigt)
ALPACA_API_KEY = "YOUR_ALPACA_API_KEY"
ALPACA_SECRET_KEY = "YOUR_ALPACA_SECRET_KEY"


# Funktion för att hämta aktiedata från Avanza
def fetch_avanza_stock(symbol):
    """
    Hämtar aktieinformation från Avanza.
    """
    try:
        response = requests.get(f"{AVANZA_API_URL}/{symbol}")
        data = response.json()
        logging.info(f"[{datetime.now()}] ✅ Hämtade Avanza-data för {symbol}: {data}")
        return data
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av Avanza-data för {symbol}: {str(e)}"
        )
        return None


# Funktion för att hämta kryptopriser från Binance
def fetch_binance_price(symbol):
    """
    Hämtar senaste kryptopriset från Binance.
    """
    try:
        response = requests.get(f"{BINANCE_API_URL}?symbol={symbol}")
        data = response.json()
        price = float(data["price"])
        logging.info(
            f"[{datetime.now()}] ✅ Hämtade Binance-data för {symbol}: {price} USD"
        )
        return price
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av Binance-data för {symbol}: {str(e)}"
        )
        return None


# Funktion för att hämta aktieinformation från Alpaca
def fetch_alpaca_stock(symbol):
    """
    Hämtar aktieinformation från Alpaca API.
    """
    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY,
    }
    try:
        response = requests.get(f"{ALPACA_API_URL}/assets/{symbol}", headers=headers)
        data = response.json()
        logging.info(f"[{datetime.now()}] ✅ Hämtade Alpaca-data för {symbol}: {data}")
        return data
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av Alpaca-data för {symbol}: {str(e)}"
        )
        return None


# Exempelanrop
if __name__ == "__main__":
    avanza_stock = fetch_avanza_stock("AAPL")
    print(f"📈 Avanza AAPL-data: {avanza_stock}")

    binance_price = fetch_binance_price("BTCUSDT")
    print(f"💰 Binance BTC/USDT-pris: {binance_price}")

    alpaca_stock = fetch_alpaca_stock("AAPL")
    print(f"🏦 Alpaca AAPL-data: {alpaca_stock}")
