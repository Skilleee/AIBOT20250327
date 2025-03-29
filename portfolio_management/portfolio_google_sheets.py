import logging
 from datetime import datetime
 from portfolio_management.portfolio_data_loader import fetch_all_portfolios
 
 # Strategier per konto
 ACCOUNT_STRATEGIES = {
     "Alice": {"horizon": 20, "risk": "medium-high"},
     "Valter": {"horizon": 20, "risk": "medium-high"},
     "Pension": {"horizon": 30, "risk": "low-medium"},
     "Investeringskonto": {"horizon": 10, "risk": "high"},
 }
 
 # Kategorier som anses offensiva
 HIGH_GROWTH_CATEGORIES = ["AI", "Teknik", "Blockchain", "Kryptovaluta"]
 DEFENSIVE_CATEGORIES = ["Global", "Tillväxtmarknad", "Hälsovård"]
 
 logging.basicConfig(filename="ai_trading_bot.log", level=logging.INFO)
 
 
 def analyze_asset(row, strategy):
     """
     Returnerar rekommendation: 'Köp mer', 'Behåll', eller 'Sälj'
     """
     kategori = row.get("Kategori")
     värde = row.get("Värde (SEK)", 0)
     antal = row.get("Antal", 0)
 
     if not kategori or not isinstance(värde, (int, float)):
         return "⚠️ Saknar data"
 
     offensiv = kategori in HIGH_GROWTH_CATEGORIES
     defensiv = kategori in DEFENSIVE_CATEGORIES
 
     # Enkel logik för AI-rekommendationer
     if strategy["risk"] == "high":
         if offensiv:
             return "📈 Köp mer"
         elif defensiv:
             return "🤝 Behåll"
         else:
             return "📉 Sälj"
 
     elif strategy["risk"] == "medium-high":
         if offensiv and värde < 1000:
             return "📈 Köp mer"
         elif defensiv:
             return "🤝 Behåll"
         else:
             return "📉 Sälj"
 
     elif strategy["risk"] == "low-medium":
         if defensiv:
             return "🤝 Behåll"
         elif offensiv:
             return "📉 Sälj"
         else:
             return "🤷 Osäker"
 
     return "🤷 Osäker"
 
 
 def generate_ai_recommendations():
     """
     Hämtar hela portföljen och returnerar AI-rekommendationer per konto.
     """
     portfolio = fetch_all_portfolios()
     recommendations = {}
 
     for account, rows in portfolio.items():
         strategy = ACCOUNT_STRATEGIES.get(account, {})
         account_recs = []
 
         for row in rows:
             namn = row.get("Aktie/Fond/ETF", "Okänd")
             rekommendation = analyze_asset(row, strategy)
             kategori = row.get("Kategori", "Okänd")
             värde = row.get("Värde (SEK)", 0)
 
             account_recs.append({
                 "namn": namn,
                 "kategori": kategori,
                 "värde": värde,
                 "rekommendation": rekommendation,
             })
 
         recommendations[account] = account_recs
 
     logging.info(f"[{datetime.now()}] 🧠 AI-genererade rekommendationer")
     return recommendations
 
 
 # För test
 if __name__ == "__main__":
     recs = generate_ai_recommendations()
     for konto, innehav in recs.items():
         print(f"\n📁 {konto}:")
         for post in innehav:
             print(f"• {post['namn']} ({post['kategori']} – {post['värde']} SEK): {post['rekommendation']}")
