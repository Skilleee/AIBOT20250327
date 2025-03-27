import logging

import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="tax_optimization.log", level=logging.INFO)


def optimize_tax_strategies(portfolio):
    """
    Analyserar skatteeffekter och föreslår strategier för att minimera skatter.
    """
    try:
        portfolio["tax_impact"] = portfolio["gains"] * portfolio["tax_rate"]
        portfolio_sorted = portfolio.sort_values(by="tax_impact", ascending=True)

        logging.info("✅ Skatteoptimering genomförd.")
        return portfolio_sorted[["symbol", "gains", "tax_impact"]]
    except Exception as e:
        logging.error(f"❌ Fel vid skatteanalys: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    portfolio_df = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT"],
            "gains": [10000, 5000, -2000, 8000],
            "tax_rate": [0.2, 0.15, 0.1, 0.18],
        }
    )

    optimized_taxes = optimize_tax_strategies(portfolio_df)
    print("📢 Skatteoptimerad portfölj:")
    print(optimized_taxes)
