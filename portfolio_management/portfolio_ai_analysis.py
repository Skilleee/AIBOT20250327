# portfolio_management/portfolio_ai_analysis.py

def generate_ai_recommendations():
    """
    Returnerar en dictionary med kontonamn som nycklar och en lista av
    rekommendations-dictionaries som värden.
    Varje dictionary innehåller bland annat 'namn', 'kategori', 'värde', 'valuta',
    'rekommendation', 'motivering', 'riktkurs_3m', 'riktkurs_6m', 'riktkurs_12m',
    'pe_ratio', 'rsi', 'riskbedomning' och 'historisk_prestanda'.
    """
    recommendations = {
        "Huvudkonto": [
            {
                "namn": "Tesla",
                "kategori": "Aktie",
                "värde": 850,
                "valuta": "USD",
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
                "värde": 120,
                "valuta": "SEK",
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
                "värde": 155,
                "valuta": "USD",
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
