import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="hedge_fund_positions.log", level=logging.INFO)


def fetch_hedge_fund_holdings(fund_name):
    """
    Hämtar hedgefonds innehav från offentliga rapporter.
    """
    try:
        url = f"https://api.hedgefunddata.com/holdings?fund={fund_name}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Innehavsdata hämtad för hedgefonden: {fund_name}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av hedgefondens innehav: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    fund = "Bridgewater Associates"
    hedge_fund_holdings = fetch_hedge_fund_holdings(fund)

    print(f"📢 Hedgefondsinnehav:", hedge_fund_holdings)
