import logging
from datetime import datetime

import requests

# Konfigurera loggning
logging.basicConfig(filename="institutional_flows.log", level=logging.INFO)

# API-konfiguration (exempel: WhaleWisdom, Fintel, Bloomberg)
FINTEL_API_URL = "https://fintel.io/api/institutional-ownership"


# Funktion för att hämta institutionella kapitalflöden
def fetch_institutional_flows(symbol):
    """
    Hämtar kapitalflöden från institutionella investerare (t.ex. hedgefonder och pensionsfonder).
    """
    try:
        params = {"ticker": symbol}
        response = requests.get(FINTEL_API_URL, params=params)
        data = response.json()

        inflows = data.get("inflows", 0)
        outflows = data.get("outflows", 0)
        net_flow = inflows - outflows

        logging.info(
            f"[{datetime.now()}] ✅ Institutionella flöden för {symbol}: Inflows: {inflows}, Outflows: {outflows}, Net: {net_flow}"
        )
        return {"inflows": inflows, "outflows": outflows, "net_flow": net_flow}
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av institutionella flöden för {symbol}: {str(e)}"
        )
        return None


# Funktion för att analysera institutionella investerares aktivitet
def analyze_institutional_sentiment(symbol):
    """
    Analyserar om kapitalflöden från institutionella investerare är positiva eller negativa.
    """
    flows = fetch_institutional_flows(symbol)
    if flows:
        net_flow = flows["net_flow"]
        sentiment = (
            "bullish" if net_flow > 0 else "bearish" if net_flow < 0 else "neutral"
        )
        logging.info(
            f"[{datetime.now()}] 📊 Institutionellt sentiment för {symbol}: {sentiment}"
        )
        return sentiment
    else:
        return "unknown"


# Exempelanrop
if __name__ == "__main__":
    stock_symbol = "AAPL"
    institutional_flows = fetch_institutional_flows(stock_symbol)
    print(f"🏦 Institutionella flöden för {stock_symbol}: {institutional_flows}")

    sentiment = analyze_institutional_sentiment(stock_symbol)
    print(f"📊 Institutionellt sentiment för {stock_symbol}: {sentiment}")
