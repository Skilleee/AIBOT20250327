import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="insider_transactions.log", level=logging.INFO)


def fetch_insider_trades(symbol):
    """
    Hämtar insiderhandel för ett specifikt företag.
    """
    try:
        url = f"https://api.insidertrading.com/trades?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Insiderhandel hämtad för: {symbol}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av insiderhandel: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    stock_symbol = "TSLA"
    insider_trades = fetch_insider_trades(stock_symbol)

    print(f"📢 Insidertransaktioner:", insider_trades)
