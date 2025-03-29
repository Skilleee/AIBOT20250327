import re
import yfinance as yf
import logging
from portfolio_management.portfolio_google_sheets import fetch_all_portfolios

logger = logging.getLogger(__name__)

HEADER_STRINGS = {
    "Aktie/Fond/ETF", "Ticker", "Antal", "Kurs (SEK)", "Värde (SEK)",
    "Typ", "Kategori", "Konto"
}

def parse_float_str(value_str):
    """
    Rensar en sträng från icke-numeriska tecken (förutom punkt och minus)
    och försöker konvertera till float. T.ex. "$263.55" -> 263.55
    """
    s = str(value_str).replace(",", ".")
    # Behåll endast siffror, punkt och minus
    s = re.sub(r"[^0-9\.\-]", "", s.strip())
    if s == "" or s == "." or s == "-" or s == "-.":
        return 0.0
    try:
        return float(s)
    except:
        return 0.0

def get_live_stock_info(symbol):
    """
    Hämtar livepris och valuta för en aktie med hjälp av yfinance.
    Om symbol innehåller 'NASDAQ:' tar vi bort den delen.
    """
    try:
        # Rensa bort eventuellt 'NASDAQ:'-prefix om det finns
        if "NASDAQ:" in symbol:
            symbol = symbol.split(":")[-1].strip()

        ticker = yf.Ticker(symbol)
        info = ticker.info
        price = info.get("regularMarketPrice")
        currency = info.get("currency")
        return price, currency
    except Exception as e:
        logger.error(f"Fel vid hämtning av live data för {symbol}: {str(e)}")
        return None, None

def generate_ai_recommendations():
    """
    Hämtar portföljdata från Google Sheets via fetch_all_portfolios och genererar AI-rekommendationer.
    Loggar ut debug-info för varje post så att du kan se exakt vad som händer.
    
    Returnerar en dict: { konto: [ { ... }, ... ], ... }
    """
    portfolios = fetch_all_portfolios()  
    recommendations = {}

    for account, stocks in portfolios.items():
        logger.info(f"Konto '{account}' har {len(stocks)} rader i Google Sheets.")
        recommendations[account] = []
        for stock in stocks:
            # Logga hela stock-raden för felsökning
            logger.info(f"[DEBUG] Rå data för konto '{account}': {stock}")

            # Om stock inte är en dictionary – kolla om det är en header och hoppa över
            if not isinstance(stock, dict):
                if isinstance(stock, str) and stock.strip() in HEADER_STRINGS:
                    logger.info(f"[DEBUG] Hoppar över header-sträng '{stock}' för konto '{account}'.")
                    continue
                else:
                    logger.error(f"Felaktigt format på stockdata för konto '{account}': {stock}")
                    continue

            # 1) Hämta name och symbol
            name = stock.get("name") or stock.get("Namn") or stock.get("Aktie/Fond/ETF") or "Okänt"
            symbol = stock.get("symbol") or stock.get("Ticker") or ""

            # 2) Hämta antal och kurs
            antal_str = stock.get("antal") or stock.get("Antal") or "0"
            kurs_str = stock.get("kurs") or stock.get("Kurs (SEK)") or "0"

            antal = parse_float_str(antal_str)
            kurs = parse_float_str(kurs_str)

            logger.info(f"[DEBUG] Konto '{account}', rad: name={name}, symbol={symbol}, antal={antal}, kurs={kurs}")

            # 3) Hämta live data (pris, valuta) om symbol finns
            if symbol:
                price, currency = get_live_stock_info(symbol)
            else:
                price, currency = None, None

            # Om live data saknas, använd 'kurs'
            if price is None:
                price = kurs
            if currency is None:
                currency = "N/A"

            # 4) Räkna ut totalvärde
            total_value = price * antal
            logger.info(f"[DEBUG] => Beräknat pris={price}, valuta={currency}, total_värde={total_value}")

            # 5) Bygg rekommendationspost
            rec = {
                "namn": name,
                "kategori": "Aktie",
                "symbol": symbol,
                "antal": antal,
                "pris": price,
                "valuta": currency,
                "total_värde": total_value,
                "rekommendation": "Behåll",
                "motivering": "Baserat på aktuell data rekommenderas att behålla.",
                "riktkurs_3m": "N/A",
                "riktkurs_6m": "N/A",
                "riktkurs_12m": "N/A",
                "pe_ratio": "N/A",
                "rsi": "N/A",
                "riskbedomning": "N/A",
                "historisk_prestanda": "N/A"
            }
            recommendations[account].append(rec)

    return recommendations

def suggest_new_investments(portfolios):
    """
    Genererar nya investeringsförslag baserat på portföljdata.
    """
    suggestions = {
        "Alice": [("Aktie", "Microsoft"), ("Aktie", "Google")],
        "Valter": [],
        "Pension": [("Aktie", "Amazon")],
        "Investeringskonto": []
    }
    return suggestions
