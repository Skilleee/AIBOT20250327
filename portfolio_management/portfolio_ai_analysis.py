import yfinance as yf

def get_live_stock_info(symbol):
    """
    Hämtar livepris och valuta för en aktie med hjälp av yfinance.
    Returnerar (price, currency) eller (None, None) vid fel.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        price = info.get("regularMarketPrice")
        currency = info.get("currency")
        return price, currency
    except Exception as e:
        # Om något går fel, returnera None
        return None, None

def generate_ai_recommendations():
    """
    Returnerar en dictionary med kontonamn som nycklar och en lista av
    rekommendations-dictionaries som värden.
    Varje dictionary innehåller:
      - namn: aktiens namn
      - kategori: t.ex. Aktie
      - symbol: aktiens ticker
      - värde: aktiens pris (uppdateras med live-data)
      - valuta: aktiens valuta (uppdateras med live-data)
      - rekommendation: t.ex. Köp, Sälj, Behåll
      - motivering: motivering till rekommendationen
      - riktkurs_3m, riktkurs_6m, riktkurs_12m: förväntade prisnivåer
      - pe_ratio, rsi, riskbedomning, historisk_prestanda: övrig information
    """
    # Exempeldata – statiska delar som sedan uppdateras med live-data
    recommendations = {
        "Huvudkonto": [
            {
                "namn": "Tesla",
                "kategori": "Aktie",
                "symbol": "TSLA",
                "värde": 850,  # kommer att uppdateras
                "valuta": "USD",  # platshållare
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
                "symbol": "SPOT",  # exempelsymbol, justera om nödvändigt
                "värde": 120,      # kommer att uppdateras
                "valuta": "SEK",   # platshållare
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
                "värde": 155,  # kommer att uppdateras
                "valuta": "USD",  # platshållare
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
    
    # Uppdatera varje rekommendationspost med live-data
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
    Returnerar en dictionary med kontonamn som nycklar och en lista av
    tuple (kategori, namn) med nya investeringsförslag.
    """
    suggestions = {
        "Huvudkonto": [("Aktie", "Microsoft"), ("Aktie", "Google")],
        "Pensionskonto": [("Aktie", "Amazon")]
    }
    return suggestions
