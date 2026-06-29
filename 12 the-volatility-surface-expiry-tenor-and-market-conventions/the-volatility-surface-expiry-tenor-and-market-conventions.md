Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-12-the-volatility-surface-expiry-tenor-and-market-conventions

A caplet was an option on a period fixing. A swaption was an option on a forward swap rate, so on an object that was itself already built from \(P(0,T)\) and a calendar.

Here, we are not adding a new product.

We are just clarifying one point that comes back everywhere as soon as you touch rate options: volatility in rates is not a single \(\sigma\). It is not "the market vol". It is a vol attached to a specific object, at a specific date, and often to a specific length.

In equity, the underlying is simple. You look at \(S_t\) or \(S_T\), and you talk about "the stock vol".

In rates, that is not how it works.

You do not trade the vol of an abstract "spot rate". You trade vol on forwards for caplets or on forward swap rates for swaptions.

So the right question is never:

$$
\text{what is the vol?}
$$

The right question is always:

$$
\text{vol of what, on which expiry, and on which curve underlying?}
$$

Take a caplet on the period \([T_{i-1},T_i]\). The object that carries the uncertainty is not the payment at \(T_i\). The payment is just the date when you settle the cash.

The uncertainty is on the fixing observed at the reset \(T_{i-1}\). That is where you discover the floating coupon. That is where the rate can still move before being locked.

So the risk horizon of a caplet is not the time to payment. It is the time to fixing.

And that is exactly why, in Black or Bachelier formulas, you see:

$$
\tau_i = T_{i-1}.
$$

It is the time during which the forward can still live before it gets fixed.

For a swaption, it is exactly the same logic, but at the scale of a full swap.

You have an expiry date \(T_0\). At that date, you have the right to enter or not enter a swap. So the uncertainty is what the forward swap rate will be worth at that moment. Not what happens later in the cashflows: that is the life of the underlying. The option itself is played at the exercise date.

So the risk horizon of a swaption is \(T_0\).

And there you recover exactly the same separation as from the beginning: where the thing gets fixed versus where it gets paid. Once you see that, you understand why the market does not have one vol, but a surface.

Because there has to be a standard way to quote this whole family of objects. And in rates, that standard way is a two-dimensional surface. Two axes. Two axes with a very concrete meaning.

The first axis is expiry: the time to fixing or to exercise.

The second axis is tenor: the length of the underlying for swaptions, or the maturity of the cap for caps.

So when you see \(1Y \times 5Y\), it does not mean "6 years in total".

It means an option that expires in 1 year on a swap that will last 5 years starting from that date. So 1 year of waiting, then 5 years of swap.

That is why \(1Y \times 10Y\) and \(10Y \times 1Y\) have nothing to do with each other, even if, from very far away, both touch the calendar over 11 years.

In the first case, you take a short option on a long object.

In the second, you take a long option on a short object.

So you are not placing the same uncertainty in the same place at all.

## Vol Conventions

There is a second layer, which is really specific to rates: vol conventions, because rates can be low and they can even be negative.

That completely changes the way you model the underlying.

The Black convention assumes that the underlying, so the forward or the forward swap rate, is lognormal.

Structurally, it pushes toward the positive, and in the formula you carry logs:

$$
\ln(F/K)
\qquad\text{or}\qquad
\ln(S/K).
$$

That is very convenient when levels are comfortably positive. It also remains a huge part of market legacy.

The Bachelier convention assumes instead that the underlying is normal.

So it can cross zero with no problem at all. And the formulas are written directly in \(F-K\), with a normal density term. That is exactly why, in low-rate or negative-rate regimes, quoting in normal vol becomes natural.

You do not break the mechanics. Here you really need to feel a difference in dimension that matters a lot.

A Black vol is unitless. It is an annual percentage.

A normal vol is in rate units. Typically, in basis points per square root of year.

That is also where you see the level effect very clearly. If you take a stylized lognormal model:

$$
dF = \sigma F\,dW,
$$

then the absolute standard deviation behaves like:

$$
\operatorname{Std}(F)\approx \sigma F\sqrt{T}.
$$

So if the level \(F\) becomes small, the absolute moves mechanically become small as well.

By contrast:

$$
dF = \sigma_N dW,
$$

so:

$$
\operatorname{Std}(F)\approx \sigma_N\sqrt{T}.
$$

There, the absolute scale no longer depends on the level.

So when you look at "the same option" with a Black vol and a normal vol, you absolutely must not believe that you are looking at two ways of writing the same thing. You are not measuring the same quantity.

Above all that, you have the smile, or skew, in rates, especially visible on swaptions.

Vol is not flat in strike.

Payer and receiver do not live in the same tail of the distribution. If the market thinks the risk of rates going sharply higher does not have the same probability, nor the same premium, as rates going sharply lower, then that asymmetry will show up in implied vols.

Because in rates you have mean reversion, zero or negative bound effects, and correlations between forwards, the smile can become very structured, especially in certain areas: long expiries, stress periods, and so on.

The goal is not to do volatility microstructure. The goal is simply to read correctly what you are looking at: a surface in \((expiry, tenor)\), and if you go more finely, strike slices to read the smile.

## Quotes Are Not Parameters

Last conceptual point to keep clear: market vols are implied quotes, not model parameters.

A "5Y cap vol" quote is not information about one isolated caplet. It is information about the whole strip.

So if you want caplet vols, you have to bootstrap them. Basically, you peel the strip caplet by caplet with a structural assumption.

On the swaption side, it is precisely because swaptions touch many maturities at once, with a correlated and convex structure, that they are natural calibration instruments for term-structure models like Hull-White, HJM, or LMM later on.

For now, it is enough to keep this in your head:

$$
\text{a quote is not a parameter, and a surface is not one number.}
$$

A practical flag now.

In the real modern market, you discount in OIS and you project forwards on the index curve, such as SOFR, legacy IBOR, and so on. So the vol surface is attached to the index and the underlying: caps versus swaptions, conventions, and so on.

The expiry-tenor structure remains.

But your \(P(0,T)\) for PV and your forwards for the underlying no longer come from the same curve.

Here, we deliberately stay in single-curve so the objects remain transparent.

## Python Skeleton

On the Python side, the goal here is not to build an industrial pricer. The goal is to manipulate a mini-surface and to see the objects live properly.

So you take a grid of expiries \(E\) and tenors \(X\).

For each node \((E,X)\), you build the annuity \(A(0)\) and the forward swap rate \(S(0)\) from \(P(0,T)\) and a semiannual calendar. That already is the heart of the subject.

Because the surface node is not an abstract point. It is a real market object: an option expiring at \(E\), on a swap of length \(X\).

Then, once you have \(A(0)\) and \(S(0)\), you naturally get the ATM strike:

$$
K_{ATM}=S(0).
$$

And there, you price that ATM once under Black, once under Bachelier, using the vol quoted at that node. Then you run three simple diagnostics:

- the expiry structure;
- the tenor structure;
- the level effect: how equivalent normal vols change when \(S(0)\) is small or large.

The code starts by setting the inputs: a notional, a grid of expiries, a grid of tenors, then two surfaces: a Black vol surface, unitless, and a normal vol surface, in rate units.

```python
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
```

Then you set an example discount curve, then log-linear interpolation. Once again, you start from the same building block as everywhere else: \(P(0,T)\).

```python
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
```

The `build_swap_objects` function then does exactly what we just described: it takes an expiry and a tenor, builds the semiannual calendar of the underlying swap, computes the annuity \(A(0)\), then the forward swap rate \(S(0)\).

So at each surface node, you are really reconstructing the market object behind the quote.

```python
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
```

After that, you set the ATM pricing bricks. We deliberately stay at the cleanest point: ATM. Under Black, since \(K=S_0\), \(d_1\) and \(d_2\) simplify a lot. Under ATM Bachelier, you also have an ultra-clean form.

The idea is not to overdo it. It is just to make the surface live.

```python
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
```

Then you allocate matrices to store ATM PVs under Black and under Bachelier, as well as the intermediate objects \(A(0)\) and \(S(0)\). You loop over all nodes \((E,X)\).

Each time, you reconstruct the object, price it under both conventions, and store it.

```python
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
```

And there already, the code puts you in the market, because it forces you to think in expiry times tenor, not in generic vol.

Then you do a very clean Black to normal conversion, but only ATM, by price matching. Why only ATM? Because the ATM Bachelier formula is ultra-simple, so the conversion is direct.

The idea is simple. You say:

$$
\text{take the ATM price produced by Black, then ask which normal vol would give exactly that same price.}
$$

So:

$$
PV_{\text{black}}
=
N A(0)\sigma_N^{equiv}\sqrt{T_0}\varphi(0),
$$

which gives:

$$
\sigma_N^{equiv}
=
\frac{PV_{\text{black}}}
{N A(0)\sqrt{T_0}\varphi(0)}.
$$

That is exactly what the next loop does.

```python
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
```

There, you immediately see the level effect. That equivalent normal vol does not move only with the Black quote. It also moves with \(S(0)\), so with the level of the forward swap rate.

Then come the simplest diagnostics. No complicated plots, just slices.

First, an expiry structure for a given tenor, here 10Y. You look at how Black vol evolves when you lengthen the waiting time before exercise, with constant underlying length.

Then, a tenor structure for a given expiry, here 2Y. You read two things side by side: the vol structure and the level structure \(S(0)\). So you can already place the vol quote and the underlying level next to each other.

```python
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
```

Deep down, this code does exactly three things that immediately put you in the market.

First, it forces you to think in expiry times tenor, because everything is indexed like that.

Then, it shows you that the ATM price naturally scales with \(N\times A(0)\), so with the PV size of the underlying, and with vol.

Finally, it gives you a very simple Black to normal ATM conversion by price matching, and there you immediately see the level effect through \(S(0)\).

So the lesson is right there:

in rates, vol is never just a number by itself. It is always attached to:

- an object;
- a fixing or exercise horizon;
- an underlying length;
- a model convention;
- often a level.

And as long as you do not read all of that together, you are not really reading the surface.
