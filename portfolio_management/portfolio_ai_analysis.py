import logging
from datetime import datetime
from portfolio_management.portfolio_google_sheets import fetch_all_portfolios

# Strategier per konto
ACCOUNT_STRATEGIES = {
    "Alice": {"horizon": 20, "risk": "medium-high"},
    "Valter": {"horizon": 20, "risk": "medium-high"},
    "Pension": {"horizon": 30, "risk": "low-medium"},
    "Investeringskonto": {"horizon": 10, "risk": "high"},
}

HIGH_GROWTH_CATEGORIES = ["AI", "Teknik", "Blockchain", "Kryptovaluta"]
DEFENSIVE_CATEGORIES = ["Global", "Tillväxtmarknad", "Hälsovård"]

# Förslag på investeringar som kan användas i olika konton
SUGGESTED_INVESTMENTS = {
    "AI": ["SEB AI - Artificial Intelligence C SEK", "iShares Robotics & AI ETF"],
    "Teknik": ["Swedbank Robur Technology", "Invesco Nasdaq 100 ETF"],
    "Global": ["Avanza Global", "Länsförsäkringar Global Indexnära"],
    "Tillväxtmarknad": ["Länsförsäkringar Tillväxtmarknad", "Swedbank Robur EM"],
    "Hälsovård": ["Swedbank Robur Healthcare", "iShares Healthcare ETF"],
    "Kryptovaluta": ["Bitcoin Zero SEK", "Ethereum Tracker EUR XBT"],
}

logging.basicConfig(filename="ai_trading_bot.log", level=logging.INFO)

def analyze_asset(row, strategy):
    kategori = row.get("Kategori")
    värde = row.get("Värde (SEK)", 0)
    if not kategori or not isinstance(värde, (int, float)):
        return "⚠️ Saknar data"

    offensiv = kategori in HIGH_GROWTH_CATEGORIES
    defensiv = kategori in DEFENSIVE_CATEGORIES

    if strategy["risk"] == "high":
        return "📈 Köp mer" if offensiv else "🤝 Behåll" if defensiv else "📉 Sälj"
    elif strategy["risk"] == "medium-high":
        if offensiv and värde < 1000:
            return "📈 Köp mer"
        elif defensiv:
            return "🤝 Behåll"
        else:
            return "📉 Sälj"
    elif strategy["risk"] == "low-medium":
        return "🤝 Behåll" if defensiv else "📉 Sälj" if offensiv else "🤷 Osäker"
    return "🤷 Osäker"

def generate_ai_recommendations():
    portfolio = fetch_all_portfolios()
    recommendations = {}

    for account, rows in portfolio.items():
        strategy = ACCOUNT_STRATEGIES.get(account, {})
        account_recs = []

        for row in rows:
            namn = row.get("Aktie/Fond/ETF", "Okänd")
            kategori = row.get("Kategori", "Okänd")
            värde = row.get("Värde (SEK)", 0)
            rekommendation = analyze_asset(row, strategy)

            account_recs.append({
                "namn": namn,
                "kategori": kategori,
                "värde": värde,
                "rekommendation": rekommendation,
            })

        recommendations[account] = account_recs

    logging.info(f"[{datetime.now()}] 🧠 AI-genererade rekommendationer")
    return recommendations

def suggest_new_investments(portfolio_data):
    suggestions = {}

    for account, rows in portfolio_data.items():
        owned_categories = set(row.get("Kategori") for row in rows if row.get("Kategori"))
        strategy = ACCOUNT_STRATEGIES.get(account, {})
        account_suggestions = []

        for category, candidates in SUGGESTED_INVESTMENTS.items():
            if category not in owned_categories:
                if strategy["risk"] == "high" or (strategy["risk"] == "medium-high" and category != "Kryptovaluta"):
                    account_suggestions.append((category, candidates[0]))

        suggestions[account] = account_suggestions

    return suggestions
