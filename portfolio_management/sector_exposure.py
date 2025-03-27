import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="sector_exposure.log", level=logging.INFO)


def analyze_sector_exposure(portfolio):
    """
    Analyserar sektorexponering och identifierar över-/underexponering.
    """
    try:
        sector_exposure = portfolio.groupby("sector")["allocation"].sum()
        logging.info("✅ Sektorexponering analyserad.")
        return sector_exposure
    except Exception as e:
        logging.error(f"❌ Fel vid analys av sektorexponering: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    portfolio_df = pd.DataFrame(
        {
            "symbol": ["AAPL", "JPM", "XOM", "MSFT", "AMZN"],
            "sector": ["Tech", "Finance", "Energy", "Tech", "Tech"],
            "allocation": [0.3, 0.2, 0.15, 0.25, 0.1],
        }
    )

    sector_dist = analyze_sector_exposure(portfolio_df)
    print("📢 Sektorexponering:")
    print(sector_dist)
