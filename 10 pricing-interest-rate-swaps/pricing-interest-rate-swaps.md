Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-10-pricing-interest-rate-swaps

In the previous lesson, what we had really built was not "a rate". It was a table of prices today for certain cashflows tomorrow. And that is what has to stay in your head, because everything starts there.

From the moment that table \(P(0,T)\) exists, on a simple period \([T_1,T_2]\), you already have no freedom left to "choose" a forward. The forward does not come from your mood, nor from some convention pulled out of nowhere. It comes simply from the fact that the curve already gives you the two prices that exactly frame that period: \(P(0,T_1)\) and \(P(0,T_2)\).

So automatically, the simple rate compatible with no-arbitrage falls out on its own:

$$
1 + L(0;T_1,T_2)\Delta
=
\frac{P(0,T_1)}{P(0,T_2)}.
$$

And therefore:

$$
L(0;T_1,T_2)
=
\frac{1}{\Delta}
\left(
\frac{P(0,T_1)}{P(0,T_2)} - 1
\right).
$$

At the core, the FRA was just the contract version of that same constraint. You lock a fixed rate \(K\) on \([T_1,T_2]\). At reset \(T_1\), you observe the fixing \(L(T_1;T_1,T_2)\). Then at maturity \(T_2\), you settle the difference on simple interest:

$$
\text{Payoff}_{T_2}
=
N\Delta\left(L(T_1;T_1,T_2)-K\right).
$$

And since you discount with exactly the same curve \(P(0,T)\) that already imposed the forward, the value at \(t=0\) does not require any imagination:

$$
V_0
=
N P(0,T_2)\Delta
\left(L(0;T_1,T_2)-K\right).
$$

Up to that point, we were still in something local:

- one period;
- one forward rate;
- one contract living on that single interval.

Now we widen the picture. We stop looking at one isolated period, and we take a schedule. Because in reality, a rates product is never just one point. It is a sequence of periods, a sequence of resets, and a sequence of payments.

## Schedule

We fix dates:

$$
T_0 < T_1 < \cdots < T_n.
$$

And we chop time into pieces:

$$
[T_0,T_1], [T_1,T_2], \ldots, [T_{n-1},T_n].
$$

There, fixed income becomes much more concrete. You are not following a price floating in empty space like in a GBM. You are looking at a cashflow machine.

At some dates, there are payments known from the start. At other dates, there are payments whose amount depends on a fixing observed at the beginning of each period. But in both cases, the job of \(P(0,T)\) does not change: bring each cashflow back to today.

So take a vanilla fixed-for-floating swap. You have:

- a notional \(N\);
- a start date \(T_0\);
- payment dates \(T_1 < \cdots < T_n\);
- on each period \([T_{i-1},T_i]\), an accrual \(\Delta_i\).

## Fixed Leg

The fixed leg does not tell any complicated story. At each date \(T_i\), it pays a coupon known from today:

$$
CF_{\text{fixed}}(T_i)
=
N K \Delta_i.
$$

If you price the fixed leg at \(t=0\), you are doing nothing more than a discounted sum of fixed coupons:

$$
PV_{\text{fixed}}
=
\sum_{i=1}^{n} P(0,T_i) N K \Delta_i
=
N K \sum_{i=1}^{n} \Delta_i P(0,T_i).
$$

The natural quantity that comes out here is the annuity:

$$
A
=
\sum_{i=1}^{n}\Delta_i P(0,T_i).
$$

So the fixed leg rewrites immediately as:

$$
PV_{\text{fixed}}
=
N K A.
$$

And that should feel right away: \(A\) is the present-value size of the fixed leg. If you move \(K\), you move that leg in a perfectly linear way.

## Floating Leg

The floating leg also pays at \(T_i\), except that its rate was not known at \(t=0\). It was fixed at the beginning of the period, at reset \(T_{i-1}\):

$$
CF_{\text{float}}(T_i)
=
N\Delta_i L(T_{i-1};T_{i-1},T_i).
$$

Here you need to see the swap for what it really is: a floating leg is nothing more than a strip of FRAs glued together. Period \(i\) has a rate fixed at \(T_{i-1}\) on \([T_{i-1},T_i]\), then paid at \(T_i\). It is exactly the same mechanics as before, repeated.

So when you say "payer swap", what you are really saying is:

- I pay all the fixed coupons;
- I receive all the floating coupons.

A "receiver swap" is just the opposite.

On the floating side, in deterministic single-curve, there is a closed form. But once again, it does not come from some special magic. It falls out of the same calculation as for an FRA, repeated period after period.

On each period, we already have:

$$
1 + \Delta_i L(0;T_{i-1},T_i)
=
\frac{P(0,T_{i-1})}{P(0,T_i)}.
$$

By rearranging:

$$
P(0,T_i)\Delta_i L(0;T_{i-1},T_i)
=
P(0,T_{i-1}) - P(0,T_i).
$$

Now sum over all periods. Everything collapses cleanly in the middle. The intermediate terms cancel in a chain. Only the beginning and the end remain:

$$
\sum_{i=1}^{n}
P(0,T_i)\Delta_i L(0;T_{i-1},T_i)
=
P(0,T_0) - P(0,T_n).
$$

So the floating leg, seen as a strip of discounted mini-FRAs, is simply worth:

$$
PV_{\text{float}}
=
N\left(P(0,T_0)-P(0,T_n)\right).
$$

And in the spot-start case, \(T_0=0\), so \(P(0,0)=1\), which gives:

$$
PV_{\text{float}}
=
N\left(1-P(0,T_n)\right).
$$

## Swap Value And Par Rate

From there, the par rate \(K^\*\) is nothing more than the rate that makes the initial value zero. Nothing else.

For a payer swap, the value is:

$$
PV_{\text{swap}}
=
PV_{\text{float}} - PV_{\text{fixed}}.
$$

And the par condition simply says:

$$
PV_{\text{float}} - PV_{\text{fixed}} = 0.
$$

So:

$$
N\left(P(0,T_0)-P(0,T_n)\right)
=
N K^\* A.
$$

And therefore:

$$
K^\*
=
\frac{P(0,T_0)-P(0,T_n)}{A}
=
\frac{P(0,T_0)-P(0,T_n)}
{\sum_{i=1}^{n}\Delta_i P(0,T_i)}.
$$

Again, this is not an artificial definition. It is just the only fixed rate that exactly balances the floating leg and the fixed leg.

If you strike at \(K^\*\), the initial value is zero.

If you strike at an off-market \(K\), then the value is read immediately:

$$
PV_{\text{swap}}
=
N\left(P(0,T_0)-P(0,T_n)\right)
- N K A
=
N A(K^\*-K).
$$

So if you are payer swap and \(K>K^\*\), you are paying a fixed rate that is too high, so your swap is negative. And if \(K<K^\*\), it is positive.

The sensitivity to the fixed rate drops out immediately:

$$
\frac{\partial PV_{\text{swap}}}{\partial K}
=
-N A.
$$

Which gives you a natural PV01:

$$
PV01 \approx N A \cdot 10^{-4}.
$$

And that too has to be read properly: the PV01 here is not some desk gadget. It is just the direct translation of the fact that the fixed leg is worth \(NKA\). One extra basis point on \(K\), and you move the value by roughly \(NA \times 10^{-4}\).

## Single-Curve And Multi-Curve

Small practical flag now: everything we just wrote is exact in single-curve.

Meaning: the same curve is used both to project the floating leg and to discount.

In multi-curve, you discount in OIS and you project the floating leg on another curve. At that point, the structure "sum of discounted floating cashflows" remains, but the shortcut:

$$
P(0,T_0)-P(0,T_n)
$$

no longer falls out exactly, because the telescoping with one single curve disappears.

Here we stay deliberately single-curve so the identities fall out cleanly and all the checks are exact.

## Python Skeleton

On the Python side, you literally reproduce the mechanics we just derived by hand.

You build \(P(0,T)\), you set your schedule, you compute \(A\), you deduce \(K^\*\), you price an off-market \(K\), you compute the PV01, then you verify numerically that the floating leg viewed as a strip of FRAs matches the closed form.

The code starts by defining a simple swap: starting today, semiannual payments up to 5 years, constant accruals of 0.5, notional of 10 million.

So already here, all we are doing is materializing the schedule we just described.

```python
import numpy as np

T0 = 0.0
T = np.arange(0.5, 5.0 + 0.5, 0.5)
Delta = np.full_like(T, 0.5, dtype=float)
Tn = float(T[-1])

N = 10_000_000
```

Then we define the curve. Not as a closed formula, but as grid points \((T_{\text{grid}},P_{\text{grid}})\). The function `P0(x)` just does log-linear interpolation, so it reconstructs a coherent discount factor for any intermediate maturity.

```python
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
```

After that, we evaluate the curve exactly on the swap payment dates. So `P_T` is the list of \(P(0,T_i)\). `P_T0` is the discount factor at the start. `P_Tn` is the one at the last maturity.

```python
P_T = np.array([P0(ti) for ti in T], dtype=float)
P_T0 = P0(T0)
P_Tn = P0(Tn)
```

Then we compute the annuity \(A\). That is the sum \(\sum \Delta_i P(0,T_i)\). And once you have \(A\), the par rate \(K^\*\) falls out immediately.

```python
A = float(np.sum(Delta * P_T))
K_star = (P_T0 - P_Tn) / A
```

Then we deliberately choose an off-market fixed rate:

```python
K = K_star + 0.005
```

So 50 bps above par. The point here is not style. The point is to see that the PV formula reacts exactly the way theory says it should.

So we price the floating leg in closed form, the fixed leg, then the swap itself:

```python
PV_float_closed = N * (P_T0 - P_Tn)
PV_fixed = N * K * A
PV_swap = PV_float_closed - PV_fixed
```

Then we compute the PV01. And right after that, we do a very simple check: we bump the fixed rate by 1 bp, so \(K+10^{-4}\), and we look at the change in swap value. It should line up with \(-PV01\).

```python
PV01 = N * A * 1e-4
PV_swap_up = PV_float_closed - N * (K + 1e-4) * A
```

After that, we rebuild the floating leg, but this time period by period, as a strip of FRAs. So we form `T_prev`, the list of resets \(T_{i-1}\), then `P_prev`, the discount factors at the beginning of each period.

```python
T_prev = np.concatenate(([T0], T[:-1]))
P_prev = np.array([P0(ti) for ti in T_prev], dtype=float)
```

From there, the simple forwards \(L_i\) are computed exactly as in the theoretical formula:

```python
L_i = (P_prev / P_T - 1.0) / Delta
```

And once you have those forwards, you recompose the floating leg as a sum of discounted mini-FRAs:

```python
PV_float_strip = float(np.sum(N * P_T * Delta * L_i))
```

The check is:

```python
print("A =", A)
print("K_star =", K_star)
print("PV_float_closed =", PV_float_closed)
print("PV_float_strip  =", PV_float_strip)
print("floating diff    =", PV_float_strip - PV_float_closed)
print("PV_fixed =", PV_fixed)
print("PV_swap  =", PV_swap)
print("PV01     =", PV01)
print("1bp bump check =", PV_swap_up - PV_swap)
```

The expected reading:

- `PV_float_strip` matches `PV_float_closed`;
- \(K^\*\) is the par swap rate;
- if \(K>K^\*\), the payer swap value is negative;
- the 1bp bump moves the value by approximately \(-PV01\);
- all of it comes from one object: the discount curve \(P(0,T)\).
