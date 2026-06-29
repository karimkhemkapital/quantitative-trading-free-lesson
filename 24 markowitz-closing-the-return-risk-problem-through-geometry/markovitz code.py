import numpy as np
import pandas as pd

def estimate_mu_sigma(returns: pd.DataFrame, ann: int = 252):
    mu = returns.mean().values * ann
    Sigma = returns.cov().values * ann
    return mu, Sigma

def port_mu_sigma(w: np.ndarray, mu: np.ndarray, Sigma: np.ndarray):
    mu_p = float(w @ mu)
    sig_p = float(np.sqrt(w @ Sigma @ w))
    return mu_p, sig_p

import cvxpy as cp

def efficient_frontier(mu, Sigma, mu_grid, long_only=False, w_max=None):
    n = len(mu)
    w = cp.Variable(n)
    risk = cp.quad_form(w, Sigma)

    cons_base = [cp.sum(w) == 1]
    if long_only:
        cons_base += [w >= 0]
    if w_max is not None:
        cons_base += [w <= w_max]

    sigs, mus, weights = [], [], []
    for mu_bar in mu_grid:
        cons = cons_base + [w @ mu == mu_bar]
        prob = cp.Problem(cp.Minimize(risk), cons)
        prob.solve(solver=cp.OSQP, verbose=False)

        if w.value is None:
            sigs.append(np.nan)
            mus.append(mu_bar)
            weights.append(None)
            continue

        wv = np.array(w.value).ravel()
        mu_p, sig_p = port_mu_sigma(wv, mu, Sigma)
        sigs.append(sig_p)
        mus.append(mu_p)
        weights.append(wv)

    return np.array(sigs), np.array(mus), weights

def tangency_portfolio_closed_form(mu, Sigma, r_f):
    n = len(mu)
    mu_ex = mu - r_f * np.ones(n)
    w_raw = np.linalg.solve(Sigma, mu_ex)
    w = w_raw / np.sum(w_raw)
    mu_T, sig_T = port_mu_sigma(w, mu, Sigma)
    S_T = (mu_T - r_f) / sig_T
    return w, mu_T, sig_T, S_T

def tangency_portfolio_qp(mu, Sigma, r_f, long_only=False, w_max=None):
    n = len(mu)
    mu_ex = mu - r_f * np.ones(n)

    w = cp.Variable(n)
    risk = cp.quad_form(w, Sigma)

    # one single gauge: excess return fixed to 1
    cons = [w @ mu_ex == 1]
    if long_only:
        cons += [w >= 0]
    if w_max is not None:
        cons += [w <= w_max]

    prob = cp.Problem(cp.Minimize(risk), cons)
    prob.solve(solver=cp.OSQP, verbose=False)
    if w.value is None:
        return None, np.nan, np.nan, np.nan

    w_raw = np.array(w.value).ravel()
    w_disp = w_raw / np.sum(w_raw)  # optional: budget-1 display

    mu_T, sig_T = port_mu_sigma(w_disp, mu, Sigma)
    S_T = (mu_T - r_f) / sig_T
    return w_disp, mu_T, sig_T, S_T
