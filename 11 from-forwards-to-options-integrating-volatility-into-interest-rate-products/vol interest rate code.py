import numpy as np
from math import log, sqrt
from scipy.stats import norm

# ---------- schedule ----------
T = np.arange(0.5, 5.0 + 0.5, 0.5)      # 0.5 ... 5.0
Delta = np.full_like(T, 0.5, dtype=float)
Nn = 10_000_000

# ---------- discount curve (example) ----------
T_grid = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 5.0], dtype=float)
P_grid = np.array([1.0, 0.9900, 0.9750, 0.9450, 0.9100, 0.8500], dtype=float)

def P0(x):
    x = float(x)
    if x <= T_grid[0]:
        return float(P_grid[0])
    if x >= T_grid[-1]:
        return float(P_grid[-1])
    return float(np.exp(np.interp(x, T_grid, np.log(P_grid))))

P = np.array([P0(ti) for ti in T], dtype=float)
P_prev = np.array([P0(0.0)] + [P0(ti) for ti in T[:-1]], dtype=float)

F = (P_prev / P - 1.0) / Delta

# forwards per period (single-curve)
F = (P_prev / P - 1.0) / Delta
tau_fix = T - Delta  # T_{i-1}

# ---------- Black caplet/floorlet ----------
def black_caplet(N, P_pay, delta, Fwd, K, sigma, tau):
    if tau <= 0:
        return N * P_pay * delta * max(Fwd - K, 0.0)
    vol = sigma * sqrt(tau)
    d1 = (log(Fwd / K) + 0.5 * vol * vol) / vol
    d2 = d1 - vol
    return N * P_pay * delta * (Fwd * norm.cdf(d1) - K * norm.cdf(d2))

def black_floorlet(N, P_pay, delta, Fwd, K, sigma, tau):
    if tau <= 0:
        return N * P_pay * delta * max(K - Fwd, 0.0)
    vol = sigma * sqrt(tau)
    d1 = (log(Fwd / K) + 0.5 * vol * vol) / vol
    d2 = d1 - vol
    return N * P_pay * delta * (K * norm.cdf(-d2) - Fwd * norm.cdf(-d1))

# ---------- Bachelier caplet/floorlet ----------
def bach_caplet(N, P_pay, delta, Fwd, K, sigmaN, tau):
    if tau <= 0:
        return N * P_pay * delta * max(Fwd - K, 0.0)
    s = sigmaN * sqrt(tau)
    x = (Fwd - K) / s
    return N * P_pay * delta * ((Fwd - K) * norm.cdf(x) + s * norm.pdf(x))

def bach_floorlet(N, P_pay, delta, Fwd, K, sigmaN, tau):
    if tau <= 0:
        return N * P_pay * delta * max(K - Fwd, 0.0)
    s = sigmaN * sqrt(tau)
    x = (Fwd - K) / s
    return N * P_pay * delta * ((K - Fwd) * norm.cdf(-x) + s * norm.pdf(x))

# ---------- cap pricing ----------
K_cap = 0.03
sigma_black = 0.20   # example flat Black vol
sigmaN = 0.01        # example flat normal vol

cap_black = 0.0
floor_black = 0.0
cap_norm = 0.0

for i in range(len(T)):
    cap_black += black_caplet(Nn, P[i], Delta[i], F[i], K_cap, sigma_black, tau_fix[i])
    floor_black += black_floorlet(Nn, P[i], Delta[i], F[i], K_cap, sigma_black, tau_fix[i])
    cap_norm += bach_caplet(Nn, P[i], Delta[i], F[i], K_cap, sigmaN, tau_fix[i])

print("Cap (Black)      =", cap_black)
print("Floor (Black)    =", floor_black)
print("Cap (Bachelier)  =", cap_norm)

# caplet/floorlet parity aggregated:
parity_rhs = np.sum(Nn * P * Delta * (F - K_cap))
print("Cap-Floor parity diff =", (cap_black - floor_black) - parity_rhs)

# ---------- swaption pricing ----------
expiry = 1.0
Tn = 5.0
sigma_swpt = 0.20

# annuity and forward swap rate for underlying swap from expiry to 5Y
mask = T > expiry
T_pay = T[mask]
Delta_pay = Delta[mask]

A0 = np.sum(Delta_pay * np.array([P0(ti) for ti in T_pay]))
S0 = (P0(expiry) - P0(Tn)) / A0

K_swpt = S0  # ATM

vol = sigma_swpt * sqrt(expiry)
d1 = (log(S0 / K_swpt) + 0.5 * vol * vol) / vol
d2 = d1 - vol

pv_payer = Nn * A0 * (S0 * norm.cdf(d1) - K_swpt * norm.cdf(d2))
pv_receiver = Nn * A0 * (K_swpt * norm.cdf(-d2) - S0 * norm.cdf(-d1))

print("A(0) =", A0)
print("S(0) =", S0)
print("Payer swaption (Black)    =", pv_payer)
print("Receiver swaption (Black) =", pv_receiver)
