import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="crypto_market_data.log", level=logging.INFO)


def fetch_crypto_prices(symbol):
    """
    Hämtar aktuell prisdata för en kryptovaluta från en API.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Prisdata hämtad för: {symbol}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av kryptovalutapriser: {str(e)}")
        return None


def fetch_onchain_data(symbol):
    """
    Hämtar on-chain analysdata för en kryptovaluta.
    """
    try:
        url = f"https://api.glassnode.com/v1/metrics/{symbol}/onchain-data"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ On-chain data hämtad för: {symbol}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av on-chain data: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    crypto_symbol = "bitcoin"
    crypto_prices = fetch_crypto_prices(crypto_symbol)
    onchain_data = fetch_onchain_data(crypto_symbol)

    print(f"📢 Kryptoprisdata:", crypto_prices)
    print(f"📢 On-chain analysdata:", onchain_data)
