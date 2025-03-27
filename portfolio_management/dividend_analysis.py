import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="dividend_analysis.log", level=logging.INFO)


def analyze_dividend_yield(portfolio):
    """
    Analyserar portföljens utdelningsavkastning och föreslår bättre alternativ.
    """
    try:
        portfolio["dividend_yield"] = portfolio["dividends"] / portfolio["price"]
        high_yield_stocks = portfolio.sort_values(
            by="dividend_yield", ascending=False
        ).head(5)

        logging.info("✅ Utdelningsanalys genomförd.")
        return high_yield_stocks[["symbol", "dividend_yield"]]
    except Exception as e:
        logging.error(f"❌ Fel vid utdelningsanalys: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    portfolio_df = pd.DataFrame(
        {
            "symbol": ["T", "VZ", "KO", "PFE", "JNJ"],
            "price": [30, 50, 60, 40, 150],
            "dividends": [2, 2.5, 2.8, 1.6, 3.8],
        }
    )

    high_yield = analyze_dividend_yield(portfolio_df)
    print("📢 Högavkastande utdelningsaktier:")
    print(high_yield)
