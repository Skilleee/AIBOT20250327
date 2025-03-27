import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="data_fetcher.log", level=logging.INFO)


def fetch_market_data(api_url, params=None):
    """
    Hämtar marknadsdata från en extern API.
    """
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.info("✅ Marknadsdata hämtad från API.")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Fel vid API-anrop: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    api_url = "https://api.marketdata.com/quotes"
    market_data = fetch_market_data(api_url)
    print("📢 Hämtad marknadsdata:", market_data)
