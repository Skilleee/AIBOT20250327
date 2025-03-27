import logging

# Konfigurera loggning
logging.basicConfig(filename="hedging_strategies.log", level=logging.INFO)


def hedge_strategy(portfolio_risk_level):
    """
    Rekommenderar hedging-strategier baserat på risknivå.
    Returnerar en dictionary med strategi och metadata.
    """
    try:
        if portfolio_risk_level > 0.7:
            strategy = "Överväg att investera i guld, obligationer eller defensiva aktier."
            level = "Hög risk"
        elif portfolio_risk_level > 0.4:
            strategy = "Diversifiera med lågrisk-ETF:er och kassareserver."
            level = "Mellanrisk"
        else:
            strategy = "Portföljens risk är låg. Ingen ytterligare hedging krävs."
            level = "Låg risk"

        result = {
            "risk_level": portfolio_risk_level,
            "risk_category": level,
            "recommendation": strategy
        }

        logging.info(f"✅ Hedging-strategi föreslagen ({level}): {strategy}")
        return result

    except Exception as e:
        logging.error(f"❌ Fel vid hedging-analys: {str(e)}")
        return {
            "risk_level": portfolio_risk_level,
            "risk_category": "Okänd",
            "recommendation": "Ingen strategi"
        }


# Exempelanrop
if __name__ == "__main__":
    portfolio_risk = 0.65
    strategy = hedge_strategy(portfolio_risk)
    print(f"📢 Hedging-strategi ({strategy['risk_category']}): {strategy['recommendation']}")
