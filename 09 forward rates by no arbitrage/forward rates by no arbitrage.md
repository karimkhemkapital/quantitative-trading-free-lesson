Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-9-forward-rates-by-no-arbitrage

In the GBM / Black-Scholes lessons, we worked with two separate bricks that were working together without us really thinking about it.

The first one was a dynamics for the underlying.

And the second one was a discounting rule.

The dynamics under \(Q\) gave the "risk-neutral expectation" form, and the discounting rule was simple because we assumed a constant risk-free rate \(r\). So for any payoff \(H\), the price could be written:

$$
V_0 = e^{-rT}\mathbb{E}^Q[H].
$$

The important point here is not "GBM", not even "stocks". It is the structure: you take a future value, in the risk-neutral sense, then you bring it back to today with a discount factor.

In fixed income, we keep exactly that structure, but we change the input to discounting. Instead of a single number \(r\) that gives the factor \(e^{-rT}\), we take the discounting function directly:

$$
P(0,T).
$$

That is the price today of 1 paid at \(T\). And it is literally the same thing as in Black-Scholes when \(r\) is constant, because in that case:

$$
P(0,T) = e^{-rT}.
$$

So we are not changing the logic, we are just replacing "a constant rate" by "a discount curve".

In GBM / Black-Scholes, we had two separate blocks:

- a law for the underlying, the dynamics;
- a discounting rule, time is money.

And we took the discounting rule in the simplest possible form: a constant rate \(r\). So the moment you had a payoff at \(T\), you brought it back to 0 with a single factor:

$$
P(0,T) = e^{-rT}.
$$

And even if we did not always write \(P(0,T)\), we were already using it everywhere. In Black-Scholes, when we write:

$$
V_0 = e^{-rT}\mathbb{E}^Q[\text{payoff}],
$$

that \(e^{-rT}\) is already a price: the price at \(t=0\) of a certain cashflow "1 at date \(T\)".

We were just calling it a discount factor without naming it.

Now, in fixed income, we do exactly the same thing, except we stop pretending that this price depends on a single constant knob.

Instead of saying "ok, there is a rate \(r\) and it discounts everything the same", we say:

"Give me directly the prices today of certain cashflows at each maturity."

That is what \(P(0,T)\) is:

- you want 1 EUR guaranteed at date \(T\);
- the market tells you how much it costs today;
- that price is \(P(0,T)\).

So \(P(0,T)\) is a table:

$$
T \mapsto \text{price today of 1 paid at } T.
$$

And that is why it is the core of fixed income: because everything you do in rates, in the end, is manipulating dated cashflows, known or conditional on a fixing, and valuing them by bringing them back to 0. So your natural input object is this price table.

The bridge with GBM is extremely direct:

If rates are constant \(r\), the price of one certain euro at \(T\) must be \(e^{-rT}\), so:

$$
P(0,T) = e^{-rT}.
$$

If rates are not constant, or simply if there is not one \(r\) that works for everything, \(P(0,T)\) is no longer of the form \(e^{-rT}\) with a single \(r\). You keep the same "discount factor" idea, but you let it be a function of \(T\).

So the sentence "we replace a constant by a function" means exactly this:

- before: you used \(e^{-rT}\) everywhere;
- now: you use \(P(0,T)\) everywhere, and in the special case where \(r\) is constant, those two coincide.

If you want a mechanical picture:

- in Black-Scholes, you had one discount factor parameterized by \(r\);
- in fixed income, you have the whole family of discount factors, one per maturity.

And the immediate consequence, which leads to the FRA, is this:

Once you have \(P(0,T)\), you do not invent forwards anymore. You deduce them by no-arbitrage, because the prices of certain cashflows already pin down everything "forward" on simple deposits.

Once you have \(P(0,T)\), you no longer have the right to invent a "yield" or a "forward rate" by feel. Forwards are imposed by no-arbitrage.

That is why we attack an FRA now: it is the first rates derivative that collapses into a clean identity between discount factors, forward rate, and present value. An FRA is a forward contract on a simple rate: you lock today a rate \(K\) to borrow or lend over a future period \([T_1,T_2]\). Then the market tells you at \(T_1\) what the realized floating rate is for that period, and you pay the difference.

The whole lesson is learning how to go from:

$$
\text{discount curve} \rightarrow \text{forward over a period} \rightarrow \text{par strike} \rightarrow \text{PV if off-market},
$$

and checking that the two PV writings tell the same replication story.

## Forward Rate

We fix two dates:

$$
0 < T_1 < T_2
$$

and an accrual:

$$
\Delta = T_2 - T_1,
$$

in practice ACT/360, 30/360, etc.

We assume that at \(t=0\), the curve is given by the discount factors \(P(0,T)\). The simple forward over \([T_1,T_2]\) is then defined by the only relation compatible with no-arbitrage: investing 1 until \(T_2\) directly must be equivalent to investing 1 until \(T_1\), then rolling from \(T_1\) to \(T_2\) at the forward rate.

Write that at the payoff level at \(T_2\), and you get:

$$
1 + L(0;T_1,T_2)\Delta = \frac{P(0,T_1)}{P(0,T_2)}.
$$

And therefore:

$$
L(0;T_1,T_2)
= \frac{1}{\Delta}
\left(
\frac{P(0,T_1)}{P(0,T_2)} - 1
\right).
$$

It is important to read this as a constraint, not as an arbitrary definition: if \(P(0,T)\) is your price table, then \(L(0;T_1,T_2)\) is forced.

And yes, it can be negative: if the curve implies \(P(0,T_2) > P(0,T_1)\), then the ratio \(P(0,T_1)/P(0,T_2)\) is below 1, so the simple forward is below 0.

Economically, that means that over \([T_1,T_2]\), the market is pricing a negative money-market return.

## FRA

The FRA comes right after: it is an OTC agreement struck at \(t=0\) on a notional \(N\), where you fix a rate \(K\) for the future period \([T_1,T_2]\). The floating rate for that period is observed at \(T_1\), the fixing, and applied over \([T_1,T_2]\) with a simple interest convention.

The end-of-period payoff, at \(T_2\), for the side "receive float / pay fixed" is:

$$
\text{Payoff}_{T_2}
= N\Delta\left(L(T_1;T_1,T_2)-K\right).
$$

The sign is immediate: if rates rise and the fixing becomes larger than \(K\), you profit by receiving float.

And if you are a borrower who wants to lock future funding cost, you want protection against an increase: you take the side that gains when \(L\) goes up, so receive float / pay fixed, called payer FRA in many market conventions. The other side is the opposite profile.

At initiation, a par FRA is the one that is worth zero: no cash exchange at \(t=0\). In the single-curve deterministic setup, that simply imposes:

$$
K^\* = L(0;T_1,T_2)
= \frac{1}{\Delta}
\left(
\frac{P(0,T_1)}{P(0,T_2)} - 1
\right),
\qquad
V_0(K^\*) = 0.
$$

You can show it with no mystique: if you discount a simple-interest payoff on \([T_1,T_2]\) with the same curve \(P(0,T)\) that forced the forward, then PV must cancel when \(K\) equals the forward.

It is the exact same reflex as in Black-Scholes when you say: at fair price there is no arbitrage, so the initial net value of a forward is zero.

If now you take an off-market \(K\), the \(t=0\) value of the FRA, still from the perspective receive float / pay fixed, is, in the cleanest form:

$$
V_0
= N P(0,T_2)\Delta
\left(L(0;T_1,T_2)-K\right).
$$

It is literally:

$$
\text{discount to } T_2
\times \text{notional}
\times \text{accrual}
\times (\text{forward} - \text{fixed}).
$$

And you can rewrite it as a pure discount-factor replication by plugging in \(L(0;T_1,T_2)\).

First, the key identity:

$$
P(0,T_2)\Delta L(0;T_1,T_2)
= P(0,T_1)-P(0,T_2).
$$

Then:

$$
V_0
= N\left[
\left(P(0,T_1)-P(0,T_2)\right)
- P(0,T_2)\Delta K
\right].
$$

The signs read immediately: if:

$$
K > L(0;T_1,T_2),
$$

then:

$$
L-K < 0,
$$

so \(V_0 < 0\) for the receive-float / pay-fixed side.

Normal: you are paying fixed too expensively relative to the market forward. And the dependence in \(K\) is strictly linear, with a constant slope, the rate delta:

$$
\frac{\partial V_0}{\partial K}
= -N P(0,T_2)\Delta.
$$

## Settlement At \(T_1\)

In the market, there is a convention that always surprises the first time: many FRAs do not pay at \(T_2\), but settle at \(T_1\).

The idea is simply to pay, at the start of the period, the present value of the interest difference, using the realized period rate as the money-market discount factor.

If at \(T_1\) the fixing is \(L(T_1;T_1,T_2)\), then the cash settlement at \(T_1\) is:

$$
\text{Settlement}_{T_1}
=
\frac{
N\Delta\left(L(T_1;T_1,T_2)-K\right)
}{
1+\Delta L(T_1;T_1,T_2)
}.
$$

That is just the payoff at \(T_2\), discounted from \(T_2\) to \(T_1\) with the simple factor:

$$
\frac{1}{1+\Delta L}.
$$

Mechanically, it makes the contract cash-settle earlier, and it reduces credit exposure versus waiting for \(T_2\).

Small practical flag: in modern markets, we often live in multi-curve: forward curve for the index, OIS discount curve for PV. The logic stays identical, you just separate the roles:

- you take \(L(0;T_1,T_2)\) from the index forward curve;
- you discount with \(P_d(0,T)\) from the discount curve.

Here we keep single-curve, so the mechanics stays crystal clear.

## Python Skeleton

On the Python side, you do exactly what we did in previous lessons: you build a curve object, you compute a forward, you price, then you check an identity numerically.

Take maturities in years:

```python
T = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
```

You can either provide \(P(0,T)\) directly, or start from spot yields \(y(0,T)\) in continuous compounding and convert:

$$
P(0,T) = \exp(-y(0,T)T).
$$

Then you choose:

$$
N=10{,}000{,}000,
\qquad
T_1=1.0,
\qquad
T_2=1.5,
\qquad
\Delta=0.5.
$$

You need a function \(P0(T)\) that returns an interpolated discount factor. In practice, linear interpolation on \(\log P\) is standard because it preserves a clean exponential structure.

Here is a minimal skeleton:

```python
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
```

The reading is simple:

- \(P(0,T)\) is the primitive object.
- \(L(0;T_1,T_2)\) is forced by no-arbitrage.
- \(K^\*\) equals the forward when the FRA is at par.
- An off-market \(K\) creates a linear PV.
- The alternative PV formula is the same replication written directly with discount factors.
- Settlement at \(T_1\) is just the \(T_2\) payoff discounted back over the realized period.
