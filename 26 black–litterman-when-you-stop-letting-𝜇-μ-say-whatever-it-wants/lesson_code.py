import numpy as np


def implied_equilibrium_returns(Sigma, w_m, rf, mu_m):
    Sigma = np.asarray(Sigma, float)
    w_m = np.asarray(w_m, float).reshape(-1, 1)
    ones = np.ones((Sigma.shape[0], 1))

    sigma_m2 = float(w_m.T @ Sigma @ w_m)
    lam = (mu_m - rf) / sigma_m2 if sigma_m2 > 0 else np.nan
    pi = rf * ones + lam * (Sigma @ w_m)

    return pi.ravel(), lam


def black_litterman_posterior(Sigma, pi, P, q, Omega, tau=0.02):
    Sigma = np.asarray(Sigma, float)
    pi = np.asarray(pi, float).reshape(-1, 1)
    P = np.asarray(P, float)
    q = np.asarray(q, float).reshape(-1, 1)
    Omega = np.asarray(Omega, float)

    inv_tauSigma = np.linalg.inv(tau * Sigma)
    A = inv_tauSigma + P.T @ np.linalg.inv(Omega) @ P
    b = inv_tauSigma @ pi + P.T @ np.linalg.inv(Omega) @ q

    mu_bl = np.linalg.solve(A, b)
    return mu_bl.ravel()


def mv_direction(Sigma, mu, rf):
    Sigma = np.asarray(Sigma, float)
    mu = np.asarray(mu, float).reshape(-1, 1)
    ones = np.ones((Sigma.shape[0], 1))

    w = np.linalg.solve(Sigma, mu - rf * ones)
    w = w.ravel()

    return w / w.sum()

N = 6
a, b, c = 0, 1, 2

P = np.zeros((2, N))
P[0, a] = 1.0
P[0, b] = -1.0   # mu_a - mu_b = 2%

P[1, c] = 1.0    # mu_c = 8%

q = np.array([0.02, 0.08])

Omega = np.diag([0.02**2, 0.03**2])
