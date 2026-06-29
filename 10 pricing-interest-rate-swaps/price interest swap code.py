import numpy as np

T0 = 0.0
T = np.arange(0.5, 5.0 + 0.5, 0.5)
Delta = np.full_like(T, 0.5, dtype=float)
Tn = float(T[-1])

N = 10_000_000

T_grid = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 5.0], dtype=float)
P_grid = np.array([1.0, 0.9900, 0.9750, 0.9450, 0.9100, 0.8500], dtype=float)

def P0(x):
    x = float(x)
    if x <= T_grid[0]:
        return float(P_grid[0])
    if x >= T_grid[-1]:
        return float(P_grid[-1])
    logP = np.log(P_grid)
    return float(np.exp(np.interp(x, T_grid, logP)))

P_T = np.array([P0(ti) for ti in T], dtype=float)
P_T0 = P0(T0)
P_Tn = P0(Tn)

A = float(np.sum(Delta * P_T))
K_star = (P_T0 - P_Tn) / A

K = K_star + 0.005

PV_float_closed = N * (P_T0 - P_Tn)
PV_fixed = N * K * A
PV_swap = PV_float_closed - PV_fixed

PV01 = N * A * 1e-4
PV_swap_up = PV_float_closed - N * (K + 1e-4) * A

T_prev = np.concatenate(([T0], T[:-1]))
P_prev = np.array([P0(ti) for ti in T_prev], dtype=float)

L_i = (P_prev / P_T - 1.0) / Delta

PV_float_strip = float(np.sum(N * P_T * Delta * L_i))

print("A =", A)
print("K_star =", K_star)
print("PV_float_closed =", PV_float_closed)
print("PV_float_strip  =", PV_float_strip)
print("floating diff    =", PV_float_strip - PV_float_closed)
print("PV_fixed =", PV_fixed)
print("PV_swap  =", PV_swap)
print("PV01     =", PV01)
print("1bp bump check =", PV_swap_up - PV_swap)
