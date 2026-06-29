import numpy as np
from math import log, sqrt, exp, erf

# ---------- utils: normal cdf/pdf ----------
def n_cdf(x):
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def n_pdf(x):
    return (1.0 / sqrt(2.0 * np.pi)) * np.exp(-0.5 * x * x)

# ---------- Black-Scholes call (spot form) ----------
def bs_call(S0, K, r, q, T, sigma):
    if T <= 0:
        return max(S0 - K, 0.0)
    if sigma <= 0:
        # deterministic limit
        F = S0 * exp((r - q) * T)
        return exp(-r * T) * max(F - K, 0.0)
    F = S0 * exp((r - q) * T)
    vol_sqrtT = sigma * sqrt(T)
    d1 = (log(F / K) + 0.5 * sigma * sigma * T) / vol_sqrtT
    d2 = d1 - vol_sqrtT
    return exp(-r * T) * (F * n_cdf(d1) - K * n_cdf(d2))

# ---------- mock implied vol surface sigma_impl(K,T) ----------
# Replace this with your surface API from the previous lesson when you have it.
def sigma_impl_mock(S0, K, T):
    # simple smile: ATM ~ 20%, skew + term structure
    k = log(K / S0)
    base = 0.20 + 0.02 * (T / 5.0)
    skew = -0.15 * k
    curv = 0.25 * (k * k)
    return max(0.01, base + skew + curv)

# ---------- grids ----------
S0 = 100.0
r, q = 0.02, 0.00
T_grid = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0])
K_grid = np.arange(60.0, 140.0 + 1e-9, 2.0)
nT, nK = len(T_grid), len(K_grid)

# ---------- build call price surface C(K,T) ----------
C = np.zeros((nT, nK))
for j, T in enumerate(T_grid):
    for i, K in enumerate(K_grid):
        sig = sigma_impl_mock(S0, K, T)
        C[j, i] = bs_call(S0, K, r, q, T, sig)

# ---------- finite differences in T ----------
C_T = np.zeros_like(C)
for i in range(nK):
    # forward difference at first maturity
    C_T[0, i] = (C[1, i] - C[0, i]) / (T_grid[1] - T_grid[0])
    # backward difference at last maturity
    C_T[-1, i] = (C[-1, i] - C[-2, i]) / (T_grid[-1] - T_grid[-2])
    # central inside
    for j in range(1, nT - 1):
        dt = T_grid[j + 1] - T_grid[j - 1]
        C_T[j, i] = (C[j + 1, i] - C[j - 1, i]) / dt

# ---------- finite differences in K (first and second) ----------
C_K = np.zeros_like(C)
C_KK = np.zeros_like(C)
dK = K_grid[1] - K_grid[0]
for j in range(nT):
    # edges: one-sided
    C_K[j, 0] = (C[j, 1] - C[j, 0]) / dK
    C_K[j, -1] = (C[j, -1] - C[j, -2]) / dK
    C_KK[j, 0] = (C[j, 2] - 2 * C[j, 1] + C[j, 0]) / (dK ** 2)
    C_KK[j, -1] = (C[j, -1] - 2 * C[j, -2] + C[j, -3]) / (dK ** 2)
    for i in range(1, nK - 1):
        C_K[j, i] = (C[j, i + 1] - C[j, i - 1]) / (2 * dK)
        C_KK[j, i] = (C[j, i + 1] - 2 * C[j, i] + C[j, i - 1]) / (dK ** 2)

# ---------- Dupire local vol on (K,T) grid ----------
sigma_loc2 = np.zeros_like(C)
eps = 1e-12
for j, T in enumerate(T_grid):
    for i, K in enumerate(K_grid):
        denom = 0.5 * K * K * max(C_KK[j, i], eps)   # protect from tiny/negative
        num = C_T[j, i] + (r - q) * K * C_K[j, i] + q * C[j, i]
        sigma_loc2[j, i] = num / denom
# clip small negatives from numerical noise
sigma_loc2 = np.maximum(sigma_loc2, 0.0)
sigma_loc = np.sqrt(sigma_loc2)
print("min sigma_loc =", sigma_loc.min(), "max sigma_loc =", sigma_loc.max())

# ---------- bilinear interpolator for sigma_loc(S,t) ----------
def sigma_loc_ST(S, t):
    # clamp to grid
    t = float(t)
    S = float(S)
    if t <= T_grid[0]:
        j0 = 0
        j1 = 1
    elif t >= T_grid[-1]:
        j0 = nT - 2
        j1 = nT - 1
    else:
        j1 = np.searchsorted(T_grid, t)
        j0 = j1 - 1

    if S <= K_grid[0]:
        i0 = 0
        i1 = 1
    elif S >= K_grid[-1]:
        i0 = nK - 2
        i1 = nK - 1
    else:
        i1 = np.searchsorted(K_grid, S)
        i0 = i1 - 1

    t0, t1 = T_grid[j0], T_grid[j1]
    k0, k1 = K_grid[i0], K_grid[i1]

    # weights
    wt = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
    wk = 0.0 if k1 == k0 else (S - k0) / (k1 - k0)
    # bilinear
    s00 = sigma_loc[j0, i0]
    s01 = sigma_loc[j0, i1]
    s10 = sigma_loc[j1, i0]
    s11 = sigma_loc[j1, i1]
    return (1 - wt) * ((1 - wk) * s00 + wk * s01) + wt * ((1 - wk) * s10 + wk * s11)

# ---------- Monte Carlo pricing under local vol (example: European call) ----------
def mc_localvol_european_call(K, T, n_paths=20000, n_steps=200):
    dt = T / n_steps
    disc = exp(-r * T)
    S = np.full(n_paths, S0, dtype=float)
    for step in range(n_steps):
        t = step * dt
        sig = np.array([sigma_loc_ST(s, t) for s in S])
        Z = np.random.randn(n_paths)
        S *= np.exp((r - q - 0.5 * sig * sig) * dt + sig * np.sqrt(dt) * Z)
    payoff = np.maximum(S - K, 0.0)
    return disc * payoff.mean()

K_test, T_test = 100.0, 1.0
pv_mc = mc_localvol_european_call(K_test, T_test, n_paths=20000, n_steps=200)
pv_bs = bs_call(S0, K_test, r, q, T_test, sigma_impl_mock(S0, K_test, T_test))
print("PV MC localvol =", pv_mc, "PV BS from impl =", pv_bs, "diff =", pv_mc - pv_bs)
