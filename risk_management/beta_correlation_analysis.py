import logging

import numpy as np

# Konfigurera loggning
logging.basicConfig(filename="beta_correlation_analysis.log", level=logging.INFO)


def calculate_beta_and_correlation(portfolio_returns, market_returns):
    """
    Beräknar portföljens beta och korrelation mot marknaden.
    """
    try:
        covariance = np.cov(portfolio_returns, market_returns)[0, 1]
        market_variance = np.var(market_returns)
        beta = covariance / market_variance
        correlation = np.corrcoef(portfolio_returns, market_returns)[0, 1]

        logging.info(f"✅ Beta: {beta:.2f}, Korrelation: {correlation:.2f}")
        return beta, correlation
    except Exception as e:
        logging.error(f"❌ Fel vid beta- och korrelationsanalys: {str(e)}")
        return None, None


# Exempelanrop
if __name__ == "__main__":
    np.random.seed(42)
    portfolio_returns = np.random.randn(100) / 100
    market_returns = np.random.randn(100) / 100
    beta, correlation = calculate_beta_and_correlation(
        portfolio_returns, market_returns
    )
    print(f"📢 Beta: {beta:.2f}, Korrelation: {correlation:.2f}")
