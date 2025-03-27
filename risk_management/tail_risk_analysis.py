import logging

import numpy as np

# Konfigurera loggning
logging.basicConfig(filename="tail_risk_analysis.log", level=logging.INFO)


def analyze_tail_risk(returns):
    """
    Analyserar tail risk i portföljens avkastning.
    """
    try:
        left_tail = np.percentile(returns, 5)
        right_tail = np.percentile(returns, 95)

        logging.info(
            f"✅ Tail risk analyserad: Left tail = {left_tail:.2%}, Right tail = {right_tail:.2%}"
        )
        return left_tail, right_tail
    except Exception as e:
        logging.error(f"❌ Fel vid tail risk-analys: {str(e)}")
        return None, None


# Exempelanrop
if __name__ == "__main__":
    np.random.seed(42)
    returns = np.random.randn(1000) / 100
    left, right = analyze_tail_risk(returns)
    print(f"📢 Tail risk: Left Tail = {left:.2%}, Right Tail = {right:.2%}")
