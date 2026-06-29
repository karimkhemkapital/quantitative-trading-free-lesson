import numpy as np
from math import log, sqrt
from scipy.stats import norm

# ---------------------
# inputs
# ---------------------
Nn = 10_000_000

expiries = np.array([1, 2, 3, 5, 10], dtype=float)
tenors   = np.array([1, 2, 5, 10], dtype=float)

# simple example Black vol surface sigma_B(E,X) (dimensionless)
# rows = expiries, cols = tenors
sigma_B = np.array([
    [0.35, 0.33, 0.30, 0.28],
    [0.32, 0.30, 0.28, 0.26],
    [0.30, 0.28, 0.26, 0.24],
    [0.27, 0.25, 0.23, 0.21],
    [0.22, 0.20, 0.19, 0.18],
], dtype=float)

# simple example Normal vol surface sigma_N(E,X) (rate units)
sigma_N = np.array([
    [0.015, 0.014, 0.013, 0.012],
    [0.014, 0.013, 0.012, 0.011],
    [0.013, 0.012, 0.011, 0.010],
    [0.012, 0.011, 0.010, 0.009],
    [0.010, 0.009, 0.0085, 0.008],
], dtype=float)

# ---------------------
# discount curve (example) + log-linear interpolation
# ---------------------
T_grid = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0], dtype=float)
P_grid = np.array([1.0, 0.9900, 0.9750, 0.9450, 0.9100, 0.8500, 0.7200, 0.5200],
                  dtype=float)

def P0(T):
    T = float(T)
    if T <= T_grid[0]:
        return float(P_grid[0])
    if T >= T_grid[-1]:
        return float(P_grid[-1])
    return float(np.exp(np.interp(T, T_grid, np.log(P_grid))))

def build_swap_objects(expiry, tenor, freq=2):
    """Semiannual by default (freq=2). Returns A(0), S(0), Tn."""
    T0 = float(expiry)
    Tn = float(expiry + tenor)
    step = 1.0 / freq
    pay_dates = np.arange(T0 + step, Tn + 1e-12, step)
    deltas = np.full_like(pay_dates, step, dtype=float)
    A0 = float(np.sum(deltas * np.array([P0(t) for t in pay_dates], dtype=float)))
    S0 = (P0(T0) - P0(Tn)) / A0
    return A0, S0, Tn

# ---------------------
# ATM swaption pricing (Black / Bachelier)
# ---------------------
def black_atm_swaption(N, A0, S0, sigma, T0):
    # ATM: K=S0, d1=+0.5*sigma*sqrt(T0), d2=-0.5*sigma*sqrt(T0)
    v = sigma * sqrt(T0)
    d1 = 0.5 * v
    d2 = -0.5 * v
    return N * A0 * (S0 * norm.cdf(d1) - S0 * norm.cdf(d2))

def bach_atm_swaption(N, A0, sigmaN, T0):
    # ATM: x=0, PV = N*A0*sigmaN*sqrt(T0)*phi(0)
    return N * A0 * sigmaN * sqrt(T0) * norm.pdf(0.0)

PV_black = np.zeros((len(expiries), len(tenors)))
PV_norm  = np.zeros((len(expiries), len(tenors)))

A_mat = np.zeros_like(PV_black)
S_mat = np.zeros_like(PV_black)

for i, E in enumerate(expiries):
    for j, X in enumerate(tenors):
        A0, S0, _ = build_swap_objects(E, X, freq=2)
        A_mat[i, j] = A0
        S_mat[i, j] = S0
        PV_black[i, j] = black_atm_swaption(Nn, A0, S0, sigma_B[i, j], E)
        PV_norm[i, j] = bach_atm_swaption(Nn, A0, sigma_N[i, j], E)

print("ATM PV grid (Black):\n", PV_black)
print("ATM PV grid (Normal):\n", PV_norm)

# ---------------------
# Price-matching conversion: Black -> equivalent Normal (ATM)
# ATM makes it clean because Bachelier ATM has closed form:
# PV_black = N*A0*sigmaN_equiv*sqrt(T0)*phi(0)
# => sigmaN_equiv = PV_black / (N*A0*sqrt(T0)*phi(0))
# ---------------------
phi0 = norm.pdf(0.0)
sigmaN_equiv = np.zeros_like(PV_black)

for i, E in enumerate(expiries):
    for j in range(len(tenors)):
        sigmaN_equiv[i, j] = PV_black[i, j] / (Nn * A_mat[i, j] * sqrt(E) * phi0)

print("Equivalent normal vol from Black ATM prices:\n", sigmaN_equiv)

# ---------------------
# Basic diagnostic prints (no plots, just slices)
# ---------------------

# term structure at tenor=10Y
j10 = np.where(tenors == 10)[0][0]
print("Term structure (Black vol) tenor=10Y:", list(zip(expiries, sigma_B[:, j10])))
print("Term structure (eq normal vol) tenor=10Y:", list(zip(expiries, sigmaN_equiv[:, j10])))

# tenor structure at expiry=2Y
i2 = np.where(expiries == 2)[0][0]
print("Tenor structure (Black vol) expiry=2Y:", list(zip(tenors, sigma_B[i2, :])))
print("Tenor structure (swap rate level S0) expiry=2Y:", list(zip(tenors, S_mat[i2, :])))
