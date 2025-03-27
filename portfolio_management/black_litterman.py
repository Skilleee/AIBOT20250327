import numpy as np

def black_litterman_optimization(prior_returns: np.ndarray,
                                 cov_matrix: np.ndarray,
                                 P: np.ndarray,
                                 Q: np.ndarray,
                                 omega: np.ndarray,
                                 tau: float = 0.05) -> np.ndarray:
    inv_tau_sigma = np.linalg.inv(tau * cov_matrix)
    inv_omega = np.linalg.inv(omega)
    M = np.linalg.inv(inv_tau_sigma + P.T @ inv_omega @ P)
    adjusted_returns = M @ (inv_tau_sigma @ prior_returns + P.T @ inv_omega @ Q)
    return adjusted_returns