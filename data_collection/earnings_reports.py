import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="earnings_reports.log", level=logging.INFO)


def fetch_earnings_report(symbol):
    """
    Hämtar kvartalsvisa vinstdata för ett företag.
    """
    try:
        url = f"https://api.earningsdata.com/reports?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Vinstdata hämtad för: {symbol}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av vinstdata: {str(e)}")
        return None


def analyze_earnings_surprise(symbol):
    """
    Analyserar om ett företag överträffade eller missade analytikers förväntningar.
    """
    try:
        report = fetch_earnings_report(symbol)
        if report:
            surprise = report["actual_eps"] - report["estimated_eps"]
            logging.info(f"✅ Analys av vinstöverraskning för {symbol}: {surprise}")
            return surprise
        return None
    except Exception as e:
        logging.error(f"❌ Fel vid analys av vinstöverraskning: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    stock_symbol = "AAPL"
    earnings_data = fetch_earnings_report(stock_symbol)
    earnings_surprise = analyze_earnings_surprise(stock_symbol)

    print(f"📢 Kvartalsrapporter:", earnings_data)
    print(f"📢 Vinstöverraskning:", earnings_surprise)
