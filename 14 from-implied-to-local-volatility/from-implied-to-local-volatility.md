Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# From Implied To Local Volatility

an implied volatility surface \(\sigma_{\mathrm{impl}}(K,T)\). it gives you, for each strike and each maturity, "the vol" that makes Black-Scholes consistent with the market price. so you already have a crucial piece of information: the market does not live with a single constant \(\sigma\). it lives with a two-dimensional function.

local volatility is the most direct response to that. you keep the Black-Scholes structure a Brownian motion, a diffusion model but you stop freezing the vol. instead of a number, you use a function that depends on the level and on time: \(\sigma_{\mathrm{loc}}(S,t)\). and that function is not "chosen" at random: it is built so that the model reproduces exactly the prices of all European options observed on the surface, in an ideal setting where everything is smooth and noise-free.

we work under the risk-neutral measure \(Q\), with a continuous dividend yield \(q\) and a risk-free rate \(r\), taken constant here to keep the mechanics clean. the dynamics become

$$
dS_t = (r-q)S_t\,dt + \sigma_{\mathrm{loc}}(S_t,t)S_t\,dW_t^Q,
\quad S_0 > 0.
$$

there, the role of \(\sigma_{\mathrm{loc}}\) is clear it is the object that has to "carry" the smile. under Black-Scholes, constant vol cannot do that, so you necessarily see a gap between theory and the surface. under local vol, you change only one thing: you let the diffusion adapt to the point \((S,t)\).

the central postulate is stated without any detour for every strike \(K\) and every maturity \(T\), the European call price given by the local vol model matches the market price

$$
C_{\mathrm{mkt}}(K,T) = C_{\mathrm{loc}}(K,T)
\quad \text{for all } (K,T).
$$

that means two things at the same time. on one side, it is extremely strong: in theory, you can fit all vanillas perfectly. on the other side, it does not automatically guarantee perfect pricing for exotics, because an exotic depends on the path, hence on the joint dynamics of \(S_t\), not only on the marginal law of \(S_T\). local vol is built to match marginals, not to "guess" the true hidden dynamics.

the central mathematical piece that links "vanilla prices" and "local vol" is Dupire's equation written in the \((K,T)\) space. let \(C(K,T)\) denote the price at \(t=0\) of a European call with strike \(K\) and maturity \(T\). under absence of arbitrage and regularity assumptions the derivatives exist properly \(C(K,T)\) satisfies the forward equation

$$
\frac{\partial C}{\partial T}
= \frac{1}{2}\sigma_{\mathrm{loc}}(K,T)^2 K^2
\frac{\partial^2 C}{\partial K^2}
- (r-q)K\frac{\partial C}{\partial K}
- qC.
$$

here, \(\sigma_{\mathrm{loc}}(K,T)\) should be read as \(\sigma_{\mathrm{loc}}(S,t)\) evaluated at the point \(S=K\) and time \(t=T\) in this forward formulation. the initial condition is simply the payoff at time zero

$$
C(K,0) = (S_0-K)^+
$$

if you look closely at the equation, you immediately see why convexity in strike is such a hard issue the term \(\partial^2 C/\partial K^2\) appears in the denominator when you isolate \(\sigma_{\mathrm{loc}}^2\), and it is also the object that represents the risk-neutral density

$$
f_T(K) = \frac{\partial^2 C}{\partial K^2}
$$

so if your surface produces call prices that are not convex, or a density that is negative in some places, you break the whole mechanism: \(\sigma_{\mathrm{loc}}^2\) can become negative or blow up by isolating \(\sigma_{\mathrm{loc}}^2\) in the PDE, you get Dupire's formula

$$
\sigma_{\mathrm{loc}}(K,T)^2
=
\frac{
\frac{\partial C}{\partial T}
+ (r-q)K\frac{\partial C}{\partial K}
+ qC
}{
\frac{1}{2}K^2\frac{\partial^2 C}{\partial K^2}
}.
$$

this is the "engineering" formula: if you know \(C(K,T)\) everywhere and it is smooth enough, you can compute \(\sigma_{\mathrm{loc}}(K,T)\). in practice, you do not observe \(C\) everywhere and you observe quotes, so a discrete implied surface. the concrete path is therefore

you start from \(\sigma_{\mathrm{impl}}(K,T)\), the implied surface you convert it into prices \(C(K,T)\) through Black-Scholes you differentiate numerically with respect to \(K\) and \(T\) you plug that into Dupire to obtain \(\sigma_{\mathrm{loc}}(K,T)\) you interpret \(\sigma_{\mathrm{loc}}(S,t)\) through the identification \(S=K\) and there is one thing you need to keep in mind immediately. numerical differentiation amplifies noise... fitting a surface is already a discipline. extracting local vol is more nervous, because now you need your surface to be properly differentiable, not just interpolable.

in terms of representation, you can work directly in \((K,T)\), but you often gain stability by moving to moneyness and total variance. if you use the forward \(F(T)\), or spot adjusted for carry, you set

$$
k = \ln\left(\frac{K}{F(T)}\right)
$$

$$
w(k,T) = \sigma_{\mathrm{impl}}(k,T)^2T
$$

empirically, \(w\) is often more regular in \(T\) than \(\sigma\), and that also helps limit calendar issues but even if you store everything in \(w(k,T)\), the final Dupire calculation goes through price derivatives, so at some point you come back to \(C\).

once \(\sigma_{\mathrm{loc}}(S,t)\) is built, you can use it as a pricing engine. on Europeans, you must recover the prices of the surface and that is the whole point. on exotics, you can price through PDE local vol is Markovian, so grids work well or through Monte Carlo.

a simple MC scheme in log-Euler form, discretized over \(t\), is written as

$$
S_{t+\Delta t}
= S_t \exp\left(
\left(r-q-\frac{1}{2}\sigma_{\mathrm{loc}}(S_t,t)^2\right)\Delta t
+ \sigma_{\mathrm{loc}}(S_t,t)\sqrt{\Delta t}\,Z
\right),
\quad Z \sim \mathcal{N}(0,1).
$$

```python
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
```

what you want to see in the outputs is simple: \(\sigma_{\mathrm{loc}}\) stays positive and reasonable, not a minefield full of absurd spikes, and when you reprice a European through local vol Monte Carlo, you come back close to the Black-Scholes price built from \(\sigma_{\mathrm{impl}}\), up to MC error. if it diverges too much, it is almost always a derivatives problem noise or a convexity problem, meaning the density is not being held properly.

and for exotics, you do not need a big speech. you take a path-dependent payoff barrier, Asian you price it under local vol with the same MC or PDE engine. then you compare it to a reference, constant vol or stochastic vol if you have one, to read the style of the model.

