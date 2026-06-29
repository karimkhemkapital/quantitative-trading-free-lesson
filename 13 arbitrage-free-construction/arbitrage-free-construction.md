Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Lesson 16 - Arbitrage-Free Construction

the missing piece now is step zero. before you even fit a smile, you have to clean what the market gave you. because a fit does not "fix" an input contradiction it just spreads it around. if you mix crossed quotes, bid/ask that's too wide, strikes misaligned with the forward, or calls and puts not reconciled through parity, you can easily get a curve that looks smooth visually... but is already structurally wrong.

in practice, the first discipline is: bring everything back into the same language. same maturity, same forward, same discounting, same convention. very often, the market quotes cleaner puts on one side of ATM and cleaner calls on the other. so instead of fitting "whatever is on the screen," you rebuild one coherent call price set through put-call parity. that way, the object you check stays unique one curve \(K \mapsto C(K,T)\).

and then you can impose the discrete guardrails, not in continuous theory, but exactly on the points you actually have.

if \(K_1 < K_2 < \cdots < K_n\) for a fixed maturity, then at the very least calls must decrease with strike

$$
C(K_{i+1},T) \le C(K_i,T).
$$

and call spreads must also behave properly. the slope in strike cannot go wild. in discrete form, convexity means the slopes become less negative as \(K\) increases. in other words, if you define

$$
s_i = \frac{C(K_{i+1},T)-C(K_i,T)}{K_{i+1}-K_i},
$$

then you need

$$
s_{i+1} \ge s_i.
$$

that is the grid version of \(\partial_K^2 C \ge 0\). if that breaks, your butterfly breaks. and if your butterfly breaks, your density breaks.

and that point matters because it is the mathematical hinge of the whole lesson: under the usual spot-discounted convention, the risk-neutral density satisfies

$$
\frac{\partial^2 C}{\partial K^2}(K,T) = DF(T) \cdot f_T(K)
$$

if you work in forward convention where the discount factor is absorbed, then you get the shorter form you already wrote

$$
f_T(K) \propto \frac{\partial^2 C}{\partial K^2}(K,T).
$$

so yes, when convexity turns negative, this is not "a slightly ugly smile." you have literally manufactured a negative probability somewhere. and the moment you differentiate further to produce gammas, vegas, or worse, a local vol, the model gives it back to you immediately.

same story across time. before talking about elegant interpolation, you first have to look at what the quotes are saying vertically at fixed strike, or more cleanly at fixed log-moneyness, a longer maturity should not give you less time value than a shorter one. in prices

$$
C(K,T_2) \ge C(K,T_1) \quad \text{if } T_2 > T_1.
$$

and in your total variance representation, the practical condition that calms a lot of the problem is

$$
w(k,T_2) \ge w(k,T_1) \quad \text{for all } k.
$$

with

$$
w = \sigma_{\mathrm{impl}}^2 T
$$

that is why working in \(w\) really changes your life. you are no longer interpolating a cosmetic volatility. you are interpolating an object that directly carries accumulated uncertainty through time. once you do that, calendar structure becomes much easier to read, and repairs become much less absurd.

there is another trap, and it is a very desk-level one: a surface can look fine to the eye, look nice in a heatmap, and still be useless for hedging. why? because what kills a surface is not necessarily the level. it is local nervousness. one artificial bump around a strike can still leave you with a mid that looks "acceptable," while generating a gamma that flips sign across three ticks. so the real validation is never visual. it is in prices and derivatives.

in other words: when you bring out your builder, the question is not just "does \(\sigma_{\mathrm{impl}}(K,T)\) look reasonable?"

the real questions are

does \(C(K,T)\) decrease in \(K\)?

does \(C(K,T)\) remain convex in \(K\)?

does \(C(K,T)\) increase in \(T\)?

do the greeks move smoothly when I shift \(K\) a bit, \(T\) a bit, or \(S\) a bit?

if even one of those answers is "no," then the surface is not finished. it is just drawn.

here is a small Python block for discrete control that fits naturally right after the fit at each maturity

```python
import numpy as np
import numpy as np

def static_noarb_checks_discrete(K, C, tol=1e-10):
    K = np.asarray(K, dtype=float)
    C = np.asarray(C, dtype=float)

    order = np.argsort(K)
    K = K[order]
    C = C[order]

    # monotonicity: C decreasing in K
    mono_ok = np.all(np.diff(C) <= tol)

    # discrete convexity on non-uniform grid
    slopes = np.diff(C) / np.diff(K)   # expected <= 0
    convex_ok = np.all(np.diff(slopes) >= -tol)

    return {
        "mono_ok": bool(mono_ok),
        "convex_ok": bool(convex_ok),
        "min_slope": float(np.min(slopes)),
        "max_slope": float(np.max(slopes)),
        "min_slope_diff": float(np.min(np.diff(slopes))) if len(slopes) > 1 else np.nan,
    }
```

and for time, your calendar check can also be written in the dumbest possible way, which is exactly why it is robust

```python
def calendar_check(price_fn, K_grid, T_grid, F_fn, DF_fn, tol=1e-10):
    out = []
    for K in K_grid:
        prices = [price_fn(K, T, F_fn(T), DF_fn(T)) for T in T_grid]
        ok = all(prices[i+1] >= prices[i] - tol for i in range(len(prices)-1))
        out.append({"K": float(K), "ok": bool(ok), "prices": prices})
    return out
```

and that is the real bridge into what comes next.

once your surface is clean, you can start asking it for more than "give me an implied vol." you can ask it for a density. you can ask it for a local volatility. you can ask it for an implicit dynamic that stays coherent with the vanilla book.

for instance, if later you want to move into Dupire, you will need derivatives of the surface with respect to \(T\) and twice with respect to \(K\). the local volatility formula, in the standard case with rates \(r\) and dividend yield \(q\), is

$$
\sigma_{\mathrm{loc}}^2(K,T)
= \frac{\partial_T C + (r-q)K\partial_K C + qC}{\frac{1}{2}K^2\partial_K^2 C}.
$$

and there you immediately see why a dirty surface is fatal. if \(\partial_K^2 C\) is noisy, negative, or just too small because of some stupid interpolation, the denominator blows up and your local vol turns into a monster. so it is not really "how to fill a grid." it is "how to prepare an object coherent enough to survive differentiation without disintegrating."

said differently: the implied surface is not the end of the job. it is the intermediate layer between raw quotes and everything else. off-grid pricing, hedging, density extraction, local vol, wing stress, exotic calibration. if that layer is shaky, everything you stack on top of it is shaky too.

so the cleanest version of the conclusion would be something like this:

the market never gives you "a surface." it gives you points, so noise, so local contradictions. building a surface is not smoothing things to make them look nice. it is taking those points and manufacturing a global object that stays coherent when you convert it into prices, densities, greeks, and time structure. the true working space is not \(\sigma\), but price, or at least a representation like \((k,w)\) where the constraints stay readable. and the final validation is never done on the color of a heatmap. it is done on three hard questions: does price decrease in strike, does it remain convex, does it respect time. if yes, then you have started building a surface. if not, you have only interpolated points.
