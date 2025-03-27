import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="etf_fund_comparison.log", level=logging.INFO)


def compare_etfs_funds(funds):
    """
    Jämför ETF:er och fonder baserat på avgifter, avkastning och risk.
    """
    try:
        funds["risk_adjusted_return"] = funds["return"] / funds["volatility"]
        best_funds = funds.sort_values(by="risk_adjusted_return", ascending=False)

        logging.info("✅ ETF- och fondjämförelse genomförd.")
        return best_funds[
            ["symbol", "return", "volatility", "expense_ratio", "risk_adjusted_return"]
        ]
    except Exception as e:
        logging.error(f"❌ Fel vid fondjämförelse: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    funds_df = pd.DataFrame(
        {
            "symbol": ["SPY", "VOO", "ARKK", "QQQ"],
            "return": [0.1, 0.12, 0.08, 0.11],
            "volatility": [0.15, 0.13, 0.2, 0.17],
            "expense_ratio": [0.003, 0.004, 0.007, 0.005],
        }
    )

    best_funds = compare_etfs_funds(funds_df)
    print("📢 Jämförelse av ETF:er och fonder:")
    print(best_funds)
