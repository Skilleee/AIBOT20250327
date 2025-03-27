import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="live_sentiment_tracking.log", level=logging.INFO)


def fetch_live_sentiment(keyword):
    """
    Hämtar sentimentdata från sociala medier och nyheter i realtid.
    """
    try:
        url = f"https://api.sentimentanalysis.com/live?keyword={keyword}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Live-sentimentdata hämtad för: {keyword}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av live-sentimentdata: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    stock_symbol = "AAPL"
    sentiment_data = fetch_live_sentiment(stock_symbol)
    print("📢 Live-sentimentdata:", sentiment_data)
