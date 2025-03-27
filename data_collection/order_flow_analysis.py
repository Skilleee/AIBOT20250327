import logging
from datetime import datetime

import requests

# Konfigurera loggning
logging.basicConfig(filename="order_flow_analysis.log", level=logging.INFO)

# API-konfiguration (exempelvis från Nasdaq, NYSE, eller andra börser)
ORDER_FLOW_API_URL = "https://api.example.com/orderflow"


# Funktion för att hämta orderflöden
def fetch_order_flow(symbol):
    """
    Hämtar och analyserar orderflöden för en aktie.
    """
    try:
        params = {"symbol": symbol}
        response = requests.get(ORDER_FLOW_API_URL, params=params)
        data = response.json()

        buy_orders = data.get("buy_orders", 0)
        sell_orders = data.get("sell_orders", 0)
        net_flow = buy_orders - sell_orders

        logging.info(
            f"[{datetime.now()}] ✅ Orderflöde för {symbol}: Buy Orders: {buy_orders}, Sell Orders: {sell_orders}, Net: {net_flow}"
        )
        return {
            "buy_orders": buy_orders,
            "sell_orders": sell_orders,
            "net_flow": net_flow,
        }
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av orderflöde för {symbol}: {str(e)}"
        )
        return None


# Funktion för att analysera orderflöden
def analyze_order_flow_sentiment(symbol):
    """
    Analyserar orderflöden och identifierar om köparna eller säljarna dominerar.
    """
    flows = fetch_order_flow(symbol)
    if flows:
        net_flow = flows["net_flow"]
        sentiment = (
            "bullish" if net_flow > 0 else "bearish" if net_flow < 0 else "neutral"
        )
        logging.info(
            f"[{datetime.now()}] 📊 Orderflödessentiment för {symbol}: {sentiment}"
        )
        return sentiment
    else:
        return "unknown"


# Exempelanrop
if __name__ == "__main__":
    stock_symbol = "AAPL"
    order_flow = fetch_order_flow(stock_symbol)
    print(f"📊 Orderflöde för {stock_symbol}: {order_flow}")

    sentiment = analyze_order_flow_sentiment(stock_symbol)
    print(f"📈 Orderflödessentiment för {stock_symbol}: {sentiment}")
