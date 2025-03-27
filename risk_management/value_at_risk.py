import logging

import numpy as np

# Konfigurera loggning
logging.basicConfig(filename="value_at_risk.log", level=logging.INFO)


def calculate_var(returns, confidence_level=0.95):
    """
    Beräknar Value at Risk (VaR) för en given portfölj.
    """
    try:
        var = np.percentile(returns, (1 - confidence_level) * 100)
        logging.info(f"✅ VaR vid {confidence_level:.0%} konfidensnivå: {var:.2%}")
        return var
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av VaR: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    np.random.seed(42)
    returns = np.random.randn(1000) / 100
    var_95 = calculate_var(returns)
    print(f"📢 Value at Risk (95%): {var_95:.2%}")
