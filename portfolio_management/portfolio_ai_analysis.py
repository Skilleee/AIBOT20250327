# portfolio_management/portfolio_ai_analysis.py

def generate_ai_recommendations():
    """
    Returnerar en dictionary med kontonamn som nycklar och en lista av
    rekommendations-dictionaries som värden.
    """
    # Exempeldata – ersätt med din faktiska modell och datainsamling
    recommendations = {
        "Huvudkonto": [
            {
                "namn": "Tesla",
                "kategori": "Aktie",
                "värde": 850,
                "rekommendation": "Köp",
                "motivering": "Stark uppåttrend, hög volym.",
                "riktkurs_3m": "900 kr",
                "riktkurs_6m": "950 kr",
                "riktkurs_12m": "1100 kr",
                "pe_ratio": "N/A",
                "rsi": "N/A",
                "riskbedomning": "Låg",
                "historisk_prestanda": "Positiv"
            },
            {
                "namn": "Spotify",
                "kategori": "Aktie",
                "värde": 120,
                "rekommendation": "Behåll",
                "motivering": "Stabil efterfrågan, långsiktig tillväxt.",
                "riktkurs_3m": "125 kr",
                "riktkurs_6m": "130 kr",
                "riktkurs_12m": "140 kr",
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
                "rekommendation": "Sälj",
                "motivering": "Överköpt, risk för korrigering.",
                "riktkurs_3m": "150 kr",
                "riktkurs_6m": "145 kr",
                "riktkurs_12m": "135 kr",
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
    # Exempeldata – ersätt med logik baserat på faktiska portföljdata
    suggestions = {
        "Huvudkonto": [("Aktie", "Microsoft"), ("Aktie", "Google")],
        "Pensionskonto": [("Aktie", "Amazon")]
    }
    return suggestions
