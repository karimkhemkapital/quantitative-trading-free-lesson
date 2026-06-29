Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-7-the-greeks

Up to this point, we framed the market with a tunnel and vol. So we understood something very simple: you touch the tunnel width... and you change the space of possible scenarios.

Now we take a Black-Scholes option... and we do exactly the same thing, but with an option price. We look at how that price reacts when you touch the parameters.

And that is what Greeks are.

Not "theoretical concepts". Derivatives, so gauges. Sensors.

The goal of this lesson is simple: you derive the Greeks of a Black-Scholes European call, you understand what they measure, and then you do the clean quant work: you verify that your analytic formulas match numerical finite-difference approximations.

We stay in the classic framework. A European call, strike \(K\), maturity \(T\), on an underlying \(S_t\) that follows a GBM under the risk-neutral measure \(Q\), with constant rate \(r\) and constant volatility \(\sigma\).

And under \(Q\), the call price at \(t=0\) is:

$$
C_0=S_0N(d_1)-Ke^{-rT}N(d_2).
$$

with

$$
d_1=\frac{\ln(S_0/K)+\left(r+\frac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}},
\qquad
d_2=d_1-\sigma\sqrt{T}.
$$

Here \(N(\cdot)\) is the standard normal CDF, and \(\varphi(\cdot)\) its density.

And now... you differentiate. And you'll see that everything is mechanical: you change one variable -> the price changes -> the Greek tells you "how fast".

We start with Delta.

Delta is just the sensitivity to spot:

$$
\Delta=\frac{\partial C_0}{\partial S_0}.
$$

You start from the call formula... you differentiate with respect to \(S_0\) without forgetting that \(d_1\) and \(d_2\) also depend on \(S_0\)... and when you do the calculation properly (product rule + chain rule), you land on the ultra-known result:

$$
\Delta=N(d_1).
$$

And you can already "feel" it with no mystique: for a call, the higher spot goes, the more you approach a payoff that looks like the underlying.

So deep ITM -> delta tends to 1.

Deep OTM -> delta tends to 0.

And in between, delta evolves like a risk-neutral probability smoothed through \(d_1\).

Then Gamma.

Gamma is curvature. It's the speed at which Delta changes:

$$
\Gamma=\frac{\partial^2 C_0}{\partial S_0^2}
=\frac{\partial \Delta}{\partial S_0}.
$$

You differentiate \(N(d_1)\) with respect to \(S_0\), again chain rule through \(d_1\), and you get:

$$
\Gamma=\frac{\varphi(d_1)}{S_0\sigma\sqrt{T}}.
$$

Gamma is positive for a call:

positive convexity.

And it is maximal around at-the-money... because that's where Delta moves the fastest.

Deep ITM or deep OTM, Delta becomes flat... so Gamma drops.

Now Vega.

Here you touch the "tunnel button", \(\sigma\). Vega is:

$$
\text{Vega}=\frac{\partial C_0}{\partial \sigma}.
$$

You differentiate the price with respect to \(\sigma\), it enters \(d_1\), \(d_2\), and dispersion, and the standard result is:

$$
\text{Vega}=S_0\varphi(d_1)\sqrt{T}.
$$

Simple reading: the higher \(\sigma\) is, the wider the tunnel.

And since a call is convex, widening the tunnel increases value.

Vega is largest near ATM... because that's where convexity "matters" the most.

Then Theta.

Theta is sensitivity to time:

$$
\Theta=\frac{\partial C_0}{\partial T}.
$$

Here it's heavier because \(T\) is everywhere: in \(e^{-rT}\), in \(d_1\), \(d_2\), in \(T\).

But the standard form for a European call is:

$$
\Theta=-\frac{S_0\varphi(d_1)\sigma}{2\sqrt{T}}-rKe^{-rT}N(d_2).
$$

And you clearly see the two pieces:

the pure time decay: the first term, often negative for a long call.

the rate/discount term: the second, linked to strike discounting.

In practice: a long call generally has negative Theta. If nothing moves, time eats value.

And finally Rho.

Rho is sensitivity to the rate \(r\):

$$
\rho=\frac{\partial C_0}{\partial r}.
$$

You differentiate... and you get:

$$
\rho=KTe^{-rT}N(d_2).
$$

Direct interpretation: if \(r\) rises, \(Ke^{-rT}\) falls, so the call becomes more valuable. So call Rho is positive.

Ok.

And here... we do what every clean quant does: we verify numerically.

We fix a test point:

$$
S_0=100,\qquad K=100,\qquad r=0.03,\qquad \sigma=0.20,\qquad T=1.
$$

You code a Black-Scholes call function, then your analytic Greeks, then you compare with finite differences.

The point is not to "find an approximation". The point is to prove your derivatives are correct.

Delta with centered finite difference:

$$
\Delta_{FD}\approx\frac{C(S_0+h)-C(S_0-h)}{2h}.
$$

Gamma with centered second derivative:

$$
\Gamma_{FD}\approx\frac{C(S_0+h)-2C(S_0)+C(S_0-h)}{h^2}.
$$

Vega centered in \(\sigma\):

$$
\text{Vega}_{FD}\approx\frac{C(\sigma+h)-C(\sigma-h)}{2h}.
$$

Theta with backward difference, to match time decay:

$$
\Theta_{FD}\approx\frac{C(T-h)-C(T)}{-h},\qquad T-h>0.
$$

Rho centered in \(r\):

$$
\rho_{FD}\approx\frac{C(r+h)-C(r-h)}{2h}.
$$

And now the point many people ignore: choosing \(h\).

\(h\) too large -> discretization error: you approximate the derivative badly.

\(h\) too small -> numerical errors: rounding, cancellation.

So you test several \(h\), you look at absolute/relative error, and you choose a compromise.

Because this is not aesthetics: if your Greeks are wrong, your hedge is wrong.

And if your hedge is wrong... you take a risk you think you're not taking.
