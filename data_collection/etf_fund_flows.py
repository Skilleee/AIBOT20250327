import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="etf_fund_flows.log", level=logging.INFO)


def fetch_etf_flows(etf_symbol):
    """
    Hämtar kapitalflöden för en specifik ETF.
    """
    try:
        url = f"https://api.etfdata.com/fund_flows?symbol={etf_symbol}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ ETF-flöden hämtade för: {etf_symbol}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av ETF-flöden: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    etf_symbol = "SPY"
    etf_flows = fetch_etf_flows(etf_symbol)

    print(f"📢 ETF-flödesdata:", etf_flows)
