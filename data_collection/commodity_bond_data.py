import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="commodity_bond_data.log", level=logging.INFO)


def fetch_commodity_prices(commodity):
    """
    Hämtar aktuell prisdata för en råvara.
    """
    try:
        url = f"https://api.commoditydata.com/prices?commodity={commodity}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Prisdata hämtad för: {commodity}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av råvarupriser: {str(e)}")
        return None


def fetch_bond_yields(country):
    """
    Hämtar aktuell obligationsränta för ett land.
    """
    try:
        url = f"https://api.bonddata.com/yields?country={country}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Obligationsräntor hämtade för: {country}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av obligationsräntor: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    commodity = "gold"
    country = "USA"

    gold_prices = fetch_commodity_prices(commodity)
    bond_yields = fetch_bond_yields(country)

    print(f"📢 Råvarupriser:", gold_prices)
    print(f"📢 Obligationsräntor:", bond_yields)
