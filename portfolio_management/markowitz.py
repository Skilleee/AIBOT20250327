import numpy as np
import pandas as pd
import cvxpy as cp

def markowitz_optimization(returns: pd.DataFrame, target_return: float = None) -> np.ndarray:
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(mean_returns)
    
    if target_return is None:
        target_return = np.percentile(mean_returns, 50)
    
    weights = cp.Variable(num_assets)
    portfolio_return = mean_returns.values.T @ weights
    portfolio_risk = cp.quad_form(weights, cov_matrix.values)
    
    constraints = [
        cp.sum(weights) == 1,
        portfolio_return >= target_return,
        weights >= 0
    ]
    
    prob = cp.Problem(cp.Minimize(portfolio_risk), constraints)
    prob.solve()
    
    return weights.value