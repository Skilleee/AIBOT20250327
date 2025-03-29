import yfinance as yf
import logging
from portfolio_management.portfolio_google_sheets import fetch_all_portfolios

logger = logging.getLogger(__name__)

# Lista med kända headersträngar som kan förekomma i Google Sheets-data.
HEADER_STRINGS = {
    "Aktie/Fond/ETF", "Ticker", "Antal", "Kurs (SEK)", "Värde (SEK)",
    "Typ", "Kategori", "Konto"
}

def get_live_stock_info(symbol):
    """
    Hämtar livepris och valuta för en aktie med hjälp av yfinance.
    
    Args:
        symbol (str): Ticker-symbolet (t.ex. "TSLA", "AAPL").
    
    Returns:
        tuple: (price, currency) om lyckat, annars (None, None).
    """
    try:
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
    Hämtar portföljdata från Google Sheets via fetch_all_portfolios och genererar AI-rekommendationer
    baserat på dessa data.
    
    Returnerar:
        dict: { konto_namn: [ { ...rekommendation... }, ... ], ... }
    """
    portfolios = fetch_all_portfolios()  
    # portfolios förväntas vara i formatet:
    # {
    #   "Alice": [
    #       {"name": "Apple Inc", "symbol": "AAPL", "antal": 10, "kurs": 160, ...},
    #       ...
    #   ],
    #   "Valter": [...],
    #   ...
    # }

    recommendations = {}

    for account, stocks in portfolios.items():
        recommendations[account] = []
        for stock in stocks:
            # Hoppa över headersträngar eller om stock inte är en dict
            if not isinstance(stock, dict):
                if isinstance(stock, str) and stock.strip() in HEADER_STRINGS:
                    continue
                else:
                    logger.error(f"Felaktigt format på stockdata för konto '{account}': {stock}")
                    continue

            # Försök läsa ut nödvändig data
            name = stock.get("name", "Okänt")
            symbol = stock.get("symbol") or stock.get("Ticker") or ""
            antal = stock.get("antal", 0)
            kurs = stock.get("kurs", 0)  # Kan vara senaste kända kursen från Sheets
            # Hämta live data (price, currency)
            if symbol:
                price, currency = get_live_stock_info(symbol)
            else:
                price, currency = None, None

            # Om yfinance inte gav något pris, använd 'kurs' som fallback
            if price is None:
                price = kurs
            if currency is None:
                currency = "N/A"

            # Räkna ut beräknat värde
            total_value = 0
            if isinstance(price, (int, float)) and isinstance(antal, (int, float)):
                total_value = price * antal

            # Generera en enkel rekommendation – anpassa efter din egen AI-logik
            rec = {
                "namn": name,
                "kategori": "Aktie",
                "symbol": symbol,
                "antal": antal,
                "pris": price,
                "valuta": currency,
                "total_värde": total_value,
                "rekommendation": "Behåll",  # Exempel
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
    
    Args:
        portfolios (dict): Data från Google Sheets.

    Returnerar:
        dict: { "Alice": [("Aktie", "Microsoft"), ...], "Valter": [...], ... }
    """
    # Exempeldata – anpassa efter dina behov eller basera på portfolios
    suggestions = {
        "Alice": [("Aktie", "Microsoft"), ("Aktie", "Google")],
        "Valter": [],
        "Pension": [("Aktie", "Amazon")],
        "Investeringskonto": []
    }
    return suggestions
