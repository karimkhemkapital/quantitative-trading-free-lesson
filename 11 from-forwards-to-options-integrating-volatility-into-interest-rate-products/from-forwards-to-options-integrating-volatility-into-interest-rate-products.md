Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-11-from-forwards-to-options-integrating-volatility-into-interest-rate-products

In the previous lesson, we got used to reasoning the same way every time: you start from a curve \(P(0,T)\), so from a table of prices today, and you let that table impose the forwards by no-arbitrage.

On one period \([T_{i-1},T_i]\), you do not invent \(L_i\). It is already contained in \(P(0,T_{i-1})\) and \(P(0,T_i)\). And once you know how to do:

$$
\text{curve} \rightarrow \text{forward} \rightarrow \text{PV},
$$

you can start putting an optional wrapper around those same objects.

A cap, a floor, a swaption: that is exactly what it is. The same floating coupons, the same periods, the same calendars, but instead of accepting the coupon as it comes, you take an option on it.

The idea is not "we change worlds". It is just:

$$
\text{we keep the mechanics, we replace one linear piece by a max}(\cdot,0).
$$

Take one period \(i\), with dates \(T_{i-1}<T_i\) and accrual \(\Delta_i\). The floating rate governing that period is fixed at reset \(T_{i-1}\), and corresponds to the simple forward/Libor on \([T_{i-1},T_i]\):

$$
L(T_{i-1};T_{i-1},T_i).
$$

The coupon itself is paid at \(T_i\). So if we write a clean option payoff, it is necessarily of the form:

$$
\text{something fixed at } T_{i-1}, \text{ paid at } T_i.
$$

## Caplets And Floorlets

A caplet is the option that pays you when that fixing goes above a strike \(K\). Paid at \(T_i\):

$$
\text{Payoff}_{T_i}^{\text{caplet}}
=
N\Delta_i \max\left(L(T_{i-1};T_{i-1},T_i)-K,0\right).
$$

A floorlet is the mirror image:

$$
\text{Payoff}_{T_i}^{\text{floorlet}}
=
N\Delta_i \max\left(K-L(T_{i-1};T_{i-1},T_i),0\right).
$$

The reading here is simple:

- if you are a borrower, what hurts is the fixing going up, so you want to be long caplets: you cap your cost;
- if you are a lender, what hurts is the fixing going down, so you want to be long floorlets: you floor your return.

The fact that it is fixed at the beginning and paid at the end is just the life of a coupon: you know the rate at reset, you settle the interest on the payment date.

A cap with maturity \(T_n\) is not some mysterious object. It is just a sum of caplets over all periods of the schedule:

$$
\text{Cap}=\sum_{i=1}^{n}\text{Caplet}_i,
\qquad
\text{Floor}=\sum_{i=1}^{n}\text{Floorlet}_i.
$$

Therefore at time 0, you add the PVs because the cashflows occur on distinct dates:

$$
V_0(\text{Cap})
=
\sum_{i=1}^{n}V_0(\text{Caplet}_i),
\qquad
V_0(\text{Floor})
=
\sum_{i=1}^{n}V_0(\text{Floorlet}_i).
$$

To compute those PVs, you go back to the same starting point: the curve. In single-curve, the forward for period \(i\) is given by:

$$
F_i
=
L(0;T_{i-1},T_i)
=
\frac{1}{\Delta_i}
\left(
\frac{P(0,T_{i-1})}{P(0,T_i)}
-1
\right).
$$

And you keep in mind the local identity, which serves as a numerical check everywhere:

$$
P(0,T_i)\Delta_i F_i
=
P(0,T_{i-1})-P(0,T_i).
$$

At this stage, the only new input for a caplet or floorlet is volatility. Because the payoff is non-linear, max, you need a model for the distribution of the fixing at reset.

In practice, you do not reinvent anything: you use closed-form building blocks calibrated to market implied volatility. The two standard building blocks are:

- Black: lognormal;
- Bachelier: normal.

Both are used in real life, and Bachelier becomes natural as soon as forwards are small or negative.

## Black-76 Caplets

Under Black-76, you assume the forward \(F_i\) is lognormal under the right measure.

You take:

- \(F_i\): forward of period \(i\);
- \(\sigma_i\): Black implied volatility of that caplet;
- \(\tau_i\): time to fixing, so \(\tau_i=T_{i-1}\).

The caplet price at \(t=0\) is:

$$
V_0(\text{caplet}_i)
=
N P(0,T_i)\Delta_i
\left[
F_i\mathcal{N}(d_1)-K\mathcal{N}(d_2)
\right],
$$

with:

$$
d_1
=
\frac{\ln(F_i/K)+\frac{1}{2}\sigma_i^2\tau_i}
{\sigma_i\sqrt{\tau_i}},
\qquad
d_2
=
d_1-\sigma_i\sqrt{\tau_i}.
$$

And the floorlet:

$$
V_0(\text{floorlet}_i)
=
N P(0,T_i)\Delta_i
\left[
K\mathcal{N}(-d_2)-F_i\mathcal{N}(-d_1)
\right].
$$

The thing to keep clear here is:

- \(P(0,T_i)\) discounts to the payment date;
- \(\Delta_i\) scales the coupon size;
- \(\tau_i=T_{i-1}\) appears because the uncertainty is on the fixing at reset, not on the date when you pay.

And you have a parity that is really the backbone of option versus forward. Caplet minus floorlet at the same strike gives you back a linear payoff, so a FRA-type PV:

$$
\text{Caplet}_i-\text{Floorlet}_i
=
N P(0,T_i)\Delta_i(F_i-K).
$$

## Bachelier Caplets

If rates can be negative, the lognormal version can become awkward because you drag logs around. The Bachelier block avoids that: you assume the forward is normal, with a volatility \(\sigma_N\) in rate units.

You set:

$$
x
=
\frac{F_i-K}{\sigma_N\sqrt{\tau_i}}.
$$

Then:

$$
V_0(\text{caplet}_i)
=
N P(0,T_i)\Delta_i
\left[
(F_i-K)\mathcal{N}(x)
\sigma_N\sqrt{\tau_i}\varphi(x)
\right],
$$

and:

$$
V_0(\text{floorlet}_i)
=
N P(0,T_i)\Delta_i
\left[
(K-F_i)\mathcal{N}(-x)
\sigma_N\sqrt{\tau_i}\varphi(x)
\right].
$$

You can see the structure:

- intrinsic value: \(F-K\);
- time value: the term in \(\varphi\);
- no logs, so you can go negative without breaking the formula.

## Swaptions

The swaption is the same idea, but at the scale of a whole swap.

Instead of having an option on one floating coupon of period \(i\), you have an option to enter a fixed-for-floating swap at a future date, the expiry.

What matters is that the swaption does not decompose exactly as a "sum of caplets", because it is written on the swap rate as a whole, so on a correlated structure of forwards.

But for pricing, the standard reduction is very clean: you summarize the underlying swap by two numbers at time 0:

- a forward swap rate \(S(0)\);
- an annuity \(A(0)\).

The annuity is just the sum of discounts weighted by the accruals on the fixed dates:

$$
A(0)
=
\sum_{i=1}^{n}\Delta_i P(0,T_i),
$$

on the swap payments after expiry.

And the forward swap rate, for a swap that starts at \(T_0\) and ends at \(T_n\), is:

$$
S(0)
=
\frac{P(0,T_0)-P(0,T_n)}{A(0)}.
$$

Then you apply the same optional building block as for a caplet, but on \(S(0)\) instead of \(F_i\).

Under Black, for a payer swaption, the right to pay fixed \(K\) and receive floating at expiry \(T_0\):

$$
V_0(\text{payer swaption})
=
N A(0)
\left[
S(0)\mathcal{N}(d_1)-K\mathcal{N}(d_2)
\right],
$$

with:

$$
d_1
=
\frac{\ln(S(0)/K)+\frac{1}{2}\sigma^2T_0}
{\sigma\sqrt{T_0}},
\qquad
d_2
=
d_1-\sigma\sqrt{T_0}.
$$

And the receiver swaption:

$$
V_0(\text{receiver swaption})
=
N A(0)
\left[
K\mathcal{N}(-d_2)-S(0)\mathcal{N}(-d_1)
\right].
$$

You recover swaption parity, same logic as caplet/floorlet:

$$
\text{Payer}-\text{Receiver}
=
N A(0)(S(0)-K).
$$

## Python Skeleton

On the Python side, the sequence is deliberately the same as what we have been doing from the start:

1. You begin from a curve \(P(0,T)\).
2. You build the forwards \(F_i\).
3. You plug in a volatility model, Black or Bachelier.
4. You price by summing discounted optionlets.
5. You run the mechanical checks: parities and monotonicity in volatility.

The first block is just the schedule and the curve.

So here you are not doing anything exotic yet. You are building the exact same raw material as before: payment dates, accruals, notional, then a discount curve through a few points and a log-linear interpolation function.

```python
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
```

Once the curve is there, the forwards come out exactly as in the formula:

```python
F = (P_prev / P - 1.0) / Delta
```

That line is literally the implementation of:

$$
F_i
=
\frac{1}{\Delta_i}
\left(
\frac{P(0,T_{i-1})}{P(0,T_i)}
-1
\right).
$$

And `tau_fix = T - Delta` is just the reset time \(T_{i-1}\), because that is where the uncertainty lives in the Black or Bachelier formulas:

```python
# forwards per period (single-curve)
F = (P_prev / P - 1.0) / Delta
tau_fix = T - Delta  # T_{i-1}
```

Then come the pricing bricks. `black_caplet` and `black_floorlet` are just the closed forms period by period. The only thing to notice is that the payoff is still scaled by \(N\), by the discount factor to payment, and by the accrual.

```python
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
```

Then the Bachelier versions. Same idea, except you replace the lognormal geometry by a normal one. So there is no log, and that is exactly why this block is robust when forwards get close to zero or go negative.

```python
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
```

After that, you price a cap and a floor simply by looping over periods and summing caplets or floorlets. So the code is just the mirror of the theoretical statement: a cap is a sum of caplets.

```python
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
```

Then comes the first mechanical check. If your formulas are coherent, caplet/floorlet parity aggregated over the schedule has to hold.

The right-hand side is just the summed FRA-like linear piece:

$$
\sum_i N P(0,T_i)\Delta_i(F_i-K).
$$

And the printed difference should be numerically close to zero:

```python
# caplet/floorlet parity aggregated:
parity_rhs = np.sum(Nn * P * Delta * (F - K_cap))
print("Cap-Floor parity diff =", (cap_black - floor_black) - parity_rhs)
```

Then you move to swaptions. Here the code does exactly what the theory says: first isolate the underlying swap after expiry, then compress it into two numbers, the annuity \(A(0)\) and the forward swap rate \(S(0)\).

So `mask = T > expiry` selects the payment dates that belong to the underlying swap after expiry. `A0` is the annuity on that reduced schedule, and `S0` is the forward swap rate.

```python
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
```

Then the code sets the strike equal to the forward swap rate, so an ATM swaption, and applies the Black payer/receiver formulas exactly the same way as for one-period options.

```python
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
```

Finally, the second mechanical check is swaption parity. If the payer and receiver formulas are coherent, their difference has to match the linear swap value:

$$
N A(0)(S(0)-K).
$$

So the logic in Python is exactly the same as the logic in the math:

- start with the curve;
- the curve gives you the forwards;
- the only extra ingredient is the volatility model, Black or Bachelier, because now the payoff has a max;
- then you sum discounted optionlets, or you compress a whole swap into \(A(0)\) and \(S(0)\) for the swaption;
- at the end, you run the hard checks: parities, consistency, and sensitivity to volatility.

If those do not hold, then the bug is not in the market. It is in your construction.
