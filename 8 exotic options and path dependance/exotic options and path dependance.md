Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-8-exotic-options-and-path-dependence

So we saw that Brownian price moves inside a structure.

We talked about noise with delta-neutral inside the tunnel, and that tunnel gives a clean language to talk about dispersion, probabilities, and pricing.

Under the risk-neutral measure \(Q\), this framework becomes deliberately minimal: a constant risk-free rate \(r\), a constant volatility \(\sigma\), and a Brownian motion \(W_t^Q\).

So the underlying follows:

$$
dS_t = rS_t\,dt+\sigma S_t\,dW_t^Q,\qquad S_0>0.
$$

If a payoff depends on the path \(S_\cdot\), then its price at \(t=0\) is:

$$
V_0=e^{-rT}\mathbb{E}^Q[H(S_\cdot)].
$$

Up to now, we were often in "clean" payoffs in the sense that most of the action was about \(S_T\).

But here, in this lesson on exotics, the standard products flip the nature of the problem.

The question is no longer "can I contain my framework", it becomes "what happened during the trip".

And the moment the trip matters, Monte Carlo becomes the natural reflex: you simulate paths, you apply the payoff on each path, and you average under \(Q\).

The important point is that Monte Carlo on exotics does not break the theory, because it is still the same expectation under \(Q\), but it introduces mechanical traps.

Always the same four families of traps: discontinuity (digitals), the "touched / not touched" event (barriers), averaging (Asians), and extremes max/min (lookbacks).

Pricing is still an average, but the quality of the estimate depends on what the payoff "does" to the noise.

## Digitals

First case: digitals. Here the payoff is discontinuous, it is literally a switch.

Cash-or-nothing: it pays an amount \(Q\) if \(S_T>K\), otherwise 0:

$$
H=Q\,\mathbf{1}_{\{S_T>K\}}.
$$

Asset-or-nothing: it pays \(S_T\) if \(S_T>K\), otherwise 0:

$$
H=S_T\,\mathbf{1}_{\{S_T>K\}}.
$$

What makes it "violent" is the indicator \(\mathbf{1}_{\{S_T>K\}}\).

You literally split scenarios into two boxes with a door that slams.

On one side: \(S_T>K\) -> payoff is 1, or \(Q\), or \(S_T\). On the other: \(S_T\le K\) -> payoff is 0.

And the problem is that everything happens near \(K\). If \(S_T\) ends very close to the strike, a tiny difference, even microscopic, can flip the scenario from 0 to 1.

Result: two almost identical paths give totally different payoffs.

When you average in Monte Carlo, this "all or nothing" flip explodes the variability of the estimate, because the output is not progressive: it jumps.

Same logic for Greeks with bump-and-revalue. To estimate a delta, you typically do:

$$
\Delta\approx\frac{V(S_0+h)-V(S_0-h)}{2h}.
$$

Except for a digital, a small bump on \(S_0\) does not change the final payoff "a little": it can just push a bunch of scenarios across the threshold \(K\). So \(V(S_0+h)\) and \(V(S_0-h)\) do not differ smoothly, they differ because indicators randomly flipped.

The "derivative" you think you are measuring becomes mostly a story of draws switching sides, so very unstable noise around \(K\).

The standard way to keep the same economic meaning while making the calculation usable is to smooth the threshold: instead of a vertical wall, a soft transition.

For example a sigmoid on \(x=S_T-K\):

$$
g(x)=\frac{1}{1+e^{-ax}}.
$$

And you replace \(\mathbf{1}_{\{S_T>K\}}\) by \(g(S_T-K)\). The payoff stays a threshold, but the transition becomes differentiable, and that stabilizes sensitivity estimates a lot.

## Barriers

Second case: barriers. Here the payoff depends on an event along the path, not only on the end.

You introduce a level \(B\) and the idea "did the path touch the barrier or not?".

Example down barrier with \(B<S_0\). Down-and-out call: call payoff, but only if the barrier was never touched:

$$
H=(S_T-K)^+\,\mathbf{1}_{\{\min_{0\le t\le T}S_t>B\}}.
$$

Down-and-in call: call payoff, but only if the barrier was touched at least once:

$$
H=(S_T-K)^+\,\mathbf{1}_{\{\min_{0\le t\le T}S_t\le B\}}.
$$

And you will see a structuring identity appear: for the same \((K,B,T)\), "vanilla = in + out", because scenarios partition cleanly into "touched" and "not touched":

$$
C_{\text{vanilla}}=C_{\text{down-in}}+C_{\text{down-out}}.
$$

The trap comes from a mismatch between "the true rule" of the product and "what you observe" in the simulation.

In a barrier contract, the rule is: the barrier is monitored continuously. That means if price touches \(B\) even for a fraction of a second, the "hit" event is triggered, and it changes the payoff: knock-out / knock-in.

But in Monte Carlo, you do not watch price continuously. You watch it on a time grid \(t_i\), say 252 points. So you only see snapshots: \(S_{t_0},S_{t_1},...,S_{t_m}\). And something can happen between two snapshots: the path can go below \(B\) inside the step, then come back above before the next date. On your snapshots, everything looks "above \(B\)", so you conclude "no hit"... when in reality, the hit happened.

Direct consequence: you miss hits. So you underestimate the probability of touching the barrier. And if you underestimate hits, you misprice (bias). Typically, for a down-and-out, missing hits makes you believe the option survives more often than it should, so you overvalue it.

And this bias is worse when \(B\) is close to \(S_0\) and when your step \(\Delta t\) is large, grid too coarse.

The classic correction is to put a bit of "continuous" back inside each step: the Brownian bridge. The idea is simple: you condition on the two endpoints you know, \(S_t\) and \(S_{t+\Delta t}\), and you compute the probability that, despite these two points being above \(B\), the path still touched \(B\) between them.

For a down barrier under GBM, when \(S_t>B\) and \(S_{t+\Delta t}>B\), a standard approximation of that probability is:

$$
p_{\text{hit}}\approx\exp\left(
-\frac{2\ln(S_t/B)\ln(S_{t+\Delta t}/B)}{\sigma^2\Delta t}
\right).
$$

Intuitive reading: the farther both points are above \(B\), the larger \(\ln(S/B)\), so the product grows, so the exponential becomes tiny -> hit unlikely. Conversely, if one endpoint is close to \(B\), the probability of touching between the two is not negligible.

In practice in Monte Carlo, you do this: at each step where both endpoints are above \(B\), you compute \(p_{\text{hit}}\), you draw \(U\sim U(0,1)\), and if \(U<p_{\text{hit}}\), you declare "hit between the two". That corrects the bias without exploding the grid size.

## Asians

Third case: Asians. Here the payoff depends on an average over dates \(0<t_1<...<t_m=T\). Arithmetic average:

$$
A=\frac{1}{m}\sum_{i=1}^{m}S_{t_i}.
$$

Asian call:

$$
H=(A-K)^+.
$$

Asian put:

$$
H=(K-A)^+.
$$

Here the mechanics is simple: the average smooths the shakes. The path can tremble, but the average dampens it. So the Asian "sees" a lower effective volatility than a vanilla that only looks at \(S_T\). That's why, all else equal, an Asian often costs less than a comparable vanilla. The flip side is: the payoff truly depends on the path, fixings matter, so general closed forms are rare, and Monte Carlo remains the natural language.

And there is a very clean CQF tool here: the geometric Asian. Define:

$$
G=\exp\left(\frac{1}{m}\sum_{i=1}^{m}\ln S_{t_i}\right).
$$

Under GBM, \(G\) is lognormal, so you get a closed-form price like Black-Scholes with "effective" parameters. In practice, this geometric version mainly serves as a control variate for the arithmetic one: you simulate \(A\) and \(G\) on the same paths, you know the theoretical price of \(G\), and you use that to reduce the variance of the arithmetic Asian estimate. Same logic as everywhere: anchor the mean on a close but known object to calm the noise.

## Lookbacks

Fourth case: lookbacks. Here the payoff depends on an extreme.

Fixed-strike lookback, call on the maximum:

$$
H=\left(\max_{0\le t\le T}S_t-K\right)^+.
$$

Floating-strike lookback, call:

$$
H=S_T-\min_{0\le t\le T}S_t.
$$

The trap is direct: a grid simulation sees \(\max_i S_{t_i}\) and \(\min_i S_{t_i}\). But in continuous time, the true max/min is almost always more extreme than what the grid captures. So naive Monte Carlo produces a discretization bias: it gives a stable price, but stable around a world where extremes are underestimated. Two natural ways to handle it: increase frequency, refine the grid, or use bridge-type corrections to approximate intra-step extremes, often on \(\ln S\), because GBM becomes more Gaussian in that coordinate.

The central message of the lesson is just this: we did not change the world, we changed the payoff.

The framework is still the same risk-neutral recipe: you still price with:

$$
V_0=e^{-rT}\mathbb{E}^Q[H].
$$

So theory does not move. What changes is the shape of \(H\). On a vanilla, \(H\) depends mainly on \(S_T\). On an exotic, \(H\) depends on what happened during the trip: did it touch a barrier, what was the average, what was the max/min, etc. In other words: the payoff "hooks" to the path, not just the endpoint.

And the moment the path matters, you get two big practical problems in Monte Carlo.

First problem: bias. You can be systematically wrong because you observe the path imperfectly. Typically: on barriers or lookbacks, if your grid is too coarse, you miss barrier hits or you underestimate true extremes. The result looks stable, but it is stable around the wrong reality.

Second problem: variance. Even if you have no bias, some payoffs react too brutally to noise. Typically: a digital is "all or nothing" at the strike, so a tiny fluctuation near \(K\) flips the payoff and the average becomes very noisy. You end up with an estimate that converges slowly and huge error bands if you do not increase paths a lot or smooth.

And it becomes even clearer when you go to Greeks, sensitivities.

On a vanilla, bump-and-revalue usually behaves well: if you move \(S_0\) or \(\sigma\) a little, price moves "a little", so the finite difference is stable.

On a digital, it is the opposite: everything concentrates around \(K\). The smallest variation can push scenarios across the threshold, so your "derivative" is mostly noise if the payoff is discontinuous.

On a barrier, same idea but around \(B\): if you are close to the barrier, small changes massively shift hit probability. Sensitivities become large and unstable, and in real markets the hedge is fragile because a gap can cross \(B\) with zero time to react.

On an Asian, the average smooths the path, so Greeks are often softer, but they depend strongly on the fixing schedule: changing one fixing date changes the whole mechanics.

On a lookback, the moment a new max or min appears, you change the "record" driving the payoff. So sensitivity can become strong and irregular, because you are attached to an extreme.

Now the Python part keeps the same structure as previous Monte Carlo lessons, but with four different ways of "reading" a path.

First, simulation under \(Q\). A grid \(t_i\), a step \(\Delta t=T/m\), and the exact GBM log scheme:

$$
S_{t+\Delta t}=S_t\exp\left(\left(r-\frac{1}{2}\sigma^2\right)\Delta t+\sigma\sqrt{\Delta t}\,Z\right),
\qquad Z\sim\mathcal{N}(0,1).
$$

And pricing stays one routine that never changes: compute \(H\) on each path, average, discount:

$$
\widehat{V}_0=e^{-rT}\frac{1}{M}\sum_{j=1}^{M}H^{(j)}.
$$

And the numerical uncertainty scale reads through the standard error:

$$
SE\approx\frac{\operatorname{Std}(e^{-rT}H)}{\sqrt{M}}.
$$

Then you plug the four families, and the difference is only in how you define \(H\): smoothing for digitals, bridge correction for barriers, control variates for Asians, grid refinement / bridge corrections for lookbacks.

And you close with the notation, the same as always: \(S_t\) the price, \(r\) the rate, \(\sigma\) the vol, \(W_t^Q\) the Brownian under \(Q\), \(T\) maturity, \(K\) strike, \(B\) barrier, \(t_i\) grid, \(\Delta t=T/m\), \(H\) payoff, \(V_0=e^{-rT}\mathbb{E}^Q[H]\), \(M\) number of paths, and \(SE\) the Monte Carlo noise scale.
