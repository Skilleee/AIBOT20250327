import yfinance as yf

def get_live_stock_info(symbol):
    """
    Hämtar livepris och valuta för en aktie med hjälp av yfinance.
    
    Args:
        symbol (str): Ticker-symbolet för aktien (t.ex. "TSLA", "AAPL").
    
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
        # Logga felet om så önskas
        return None, None

def generate_ai_recommendations():
    """
    Genererar och returnerar AI-rekommendationer i form av en dictionary.
    
    Returnerar:
        dict: Nycklarna är kontonamn (t.ex. "Huvudkonto", "Pensionskonto") och värdet är
              en lista med dictionaries med följande nycklar:
              - namn: aktiens namn
              - kategori: t.ex. "Aktie"
              - symbol: aktiens ticker
              - värde: aktiens pris (uppdateras med live-data)
              - valuta: aktiens valuta (uppdateras med live-data)
              - rekommendation: t.ex. "Köp", "Sälj", "Behåll"
              - motivering: kort motivering
              - riktkurs_3m, riktkurs_6m, riktkurs_12m: förväntade prisnivåer
              - pe_ratio, rsi, riskbedomning, historisk_prestanda: övrig info
    """
    # Exempeldata – de statiska delarna (rekommendation, motivering, riktkurser m.m.)
    recommendations = {
        "Huvudkonto": [
            {
                "namn": "Tesla",
                "kategori": "Aktie",
                "symbol": "TSLA",
                "värde": 850,   # Platshållare, uppdateras nedan
                "valuta": "USD",# Platshållare, uppdateras nedan
                "rekommendation": "Köp",
                "motivering": "Stark uppåttrend, hög volym.",
                "riktkurs_3m": "900 USD",
                "riktkurs_6m": "950 USD",
                "riktkurs_12m": "1100 USD",
                "pe_ratio": "N/A",
                "rsi": "N/A",
                "riskbedomning": "Låg",
                "historisk_prestanda": "Positiv"
            },
            {
                "namn": "Spotify",
                "kategori": "Aktie",
                "symbol": "SPOT",  # Exempelsymbol (noteras på amerikanska börsen, vilket ger USD)
                "värde": 120,      # Platshållare
                "valuta": "SEK",   # Platshållare – justeras om du vill konvertera
                "rekommendation": "Behåll",
                "motivering": "Stabil efterfrågan, långsiktig tillväxt.",
                "riktkurs_3m": "125 SEK",
                "riktkurs_6m": "130 SEK",
                "riktkurs_12m": "140 SEK",
                "pe_ratio": "N/A",
                "rsi": "N/A",
                "riskbedomning": "Medium",
                "historisk_prestanda": "Stabil"
            }
        ],
        "Pensionskonto": [
            {
                "namn": "Apple",
                "kategori": "Aktie",
                "symbol": "AAPL",
                "värde": 155,  # Platshållare
                "valuta": "USD",  # Platshållare
                "rekommendation": "Sälj",
                "motivering": "Överköpt, risk för korrigering.",
                "riktkurs_3m": "150 USD",
                "riktkurs_6m": "145 USD",
                "riktkurs_12m": "135 USD",
                "pe_ratio": "N/A",
                "rsi": "N/A",
                "riskbedomning": "Hög",
                "historisk_prestanda": "Negativ"
            }
        ]
    }
    
    # Uppdatera live priser och valuta med yfinance
    for konto, rec_list in recommendations.items():
        for rec in rec_list:
            symbol = rec.get("symbol")
            if symbol:
                price, currency = get_live_stock_info(symbol)
                if price is not None and currency is not None:
                    rec["värde"] = price
                    rec["valuta"] = currency
                else:
                    rec["värde"] = "N/A"
                    rec["valuta"] = "N/A"
    return recommendations

def suggest_new_investments(portfolios):
    """
    Genererar nya investeringsförslag baserat på portföljdata.
    
    Args:
        portfolios: Data från dina portföljer (ej detaljerat implementerat här).
    
    Returnerar:
        dict: Nycklar är kontonamn och värdet är en lista med tuples (kategori, namn).
    """
    suggestions = {
        "Huvudkonto": [("Aktie", "Microsoft"), ("Aktie", "Google")],
        "Pensionskonto": [("Aktie", "Amazon")]
    }
    return suggestions
