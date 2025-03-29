import yfinance as yf
import logging
from portfolio_management.portfolio_google_sheets import fetch_all_portfolios

logger = logging.getLogger(__name__)

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
        dict: Nycklarna är kontonamn (ex. "Alice", "Valter", "Pension", "Investeringskonto") och värdet är en lista
              med dictionaries med rekommendationer för varje aktie.
    """
    portfolios = fetch_all_portfolios()  # Exempelvis: { "Alice": [ {...}, {...} ], "Valter": [...], ... }
    recommendations = {}

    for account, stocks in portfolios.items():
        recommendations[account] = []
        for stock in stocks:
            # Kontrollera att stock är en dictionary
            if not isinstance(stock, dict):
                logger.error(f"Felaktigt format på stockdata för konto '{account}': {stock}")
                continue  # Hoppa över objektet om det inte är ett dict
            name = stock.get("name", "Okänt")
            symbol = stock.get("symbol", "")
            if symbol:
                price, currency = get_live_stock_info(symbol)
            else:
                price, currency = "N/A", "N/A"

            # Generera en enkel rekommendation – här kan du lägga till mer avancerad logik
            rec = {
                "namn": name,
                "kategori": "Aktie",
                "symbol": symbol,
                "värde": price,
                "valuta": currency,
                "rekommendation": "Behåll",  # Exempelrekommendation
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
        portfolios: Data från Google Sheets (används ej detaljerat här).
    
    Returnerar:
        dict: Nycklarna är kontonamn och värdet är en lista med tuples (kategori, namn) med investeringsförslag.
    """
    # Exempeldata – anpassa efter dina behov
    suggestions = {
        "Alice": [("Aktie", "Microsoft"), ("Aktie", "Google")],
        "Valter": [],
        "Pension": [("Aktie", "Amazon")],
        "Investeringskonto": []
    }
    return suggestions
