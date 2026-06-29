T = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]

import numpy as np

# ----- input curve (example) -----
T_grid = np.array([0.5, 1.0, 1.5, 2.0, 3.0, 5.0])

# either provide discount factors directly...
P_grid = np.array([0.9900, 0.9750, 0.9600, 0.9450, 0.9100, 0.8500])

# --- log-linear interpolation on P(0,T) ---
def P0(T):
    T = float(T)
    if T <= T_grid[0]:
        return float(P_grid[0])
    if T >= T_grid[-1]:
        return float(P_grid[-1])
    logP = np.log(P_grid)
    return float(np.exp(np.interp(T, T_grid, logP)))

# ----- FRA specs -----
N = 10_000_000
T1, T2 = 1.0, 1.5
Delta = T2 - T1

P1, P2 = P0(T1), P0(T2)

# forward simple
L0 = (P1 / P2 - 1.0) / Delta
print("P(0,T1)=", P1, " P(0,T2)=", P2)
print("Forward L0 =", L0)

# par strike
K_par = L0

# PV at par (should be ~0)
PV_par = N * P2 * Delta * (L0 - K_par)
print("PV(K_par) =", PV_par)

# off-market strike: +100bps
K = L0 + 0.01
PV1 = N * P2 * Delta * (L0 - K)
print("PV form 1 =", PV1)

# replication identity check
lhs = P2 * Delta * L0
rhs = P1 - P2
print("replication check (lhs - rhs) =", lhs - rhs)

# alternative PV form
PV2 = N * ((P1 - P2) - P2 * Delta * K)
print("PV form 2 =", PV2, " diff =", PV1 - PV2)

# settlement at T1 using hypothetical realized fixing
shock = 0.005
L_real = L0 + shock
settle_T1 = N * Delta * (L_real - K) / (1.0 + Delta * L_real)
print("Settlement at T1 (hypothetical) =", settle_T1)

# compare with payoff at T2 discounted back to T1 with realized rate
payoff_T2 = N * Delta * (L_real - K)
disc_T2_to_T1 = 1.0 / (1.0 + Delta * L_real)
print(
    "Payoff_T2 * disc =",
    payoff_T2 * disc_T2_to_T1,
    " diff =",
    settle_T1 - payoff_T2 * disc_T2_to_T1,
)
