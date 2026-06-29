Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-5-the-risk-neutral-world-black-scholes-pricing

Now we move to the pricing step of this option, because that is literally the money we get paid in exchange for providing risk protection.

For a European call with strike \(K\) and maturity \(T\), the payoff is:

$$
(S_T-K)^+ = \max(S_T-K,0).
$$

So the question becomes purely mechanical: what is the price today of a payoff that happens in the future?

The Black-Scholes framework answers with one rule: the price of a payoff is a discounted expectation. But not under the real-world measure, the one where you write \(\mu\). Under a special measure: the risk-neutral measure, denoted \(Q\).

And the reason we need that is simple: we need a measure where discounted prices behave "cleanly", so pricing is compatible with no-arbitrage. No market direction. No opinion.

Concretely, that means two things.

We keep the same uncertainty, the same noise, so the same volatility \(\sigma\).

But we change the drift: instead of the real drift \(\mu\), unobservable and useless for pricing, we use the risk-free rate \(r\).

Saying "the drift becomes \(r\)" is the same as choosing the cash account as the unit of measure. Once you do that, discounted prices become martingales under an associated measure \(Q\).

So the pricing model starts from the dynamics under \(Q\):

$$
dS_t = rS_t\,dt + \sigma S_t\,dW_t,\qquad S_0>0.
$$

Same GBM as before, except \(\mu\) is replaced by \(r\). And that's the whole point: the price does not depend on what you believe about \(\mu\). It depends on \(r\) and \(\sigma\).

Now we state the pricing rule:

$$
C_0=e^{-rT}\mathbb{E}^Q\left[(S_T-K)^+\right].
$$

That is the central sentence: price equals the average payoff under \(Q\), discounted at rate \(r\).

"Black-Scholes" is exactly this package: GBM under \(Q\) + discounted expectation + European payoff.

Now we redo the Ito mechanics from Lesson 4, but under \(Q\).

We want the log, because it turns the multiplicative GBM into something linear.

$$
X_t=\ln(S_t).
$$

So we are looking at a function of \(S_t\), with:

$$
f(S)=\ln(S).
$$

Derivatives are mechanical:

$$
f'(S)=\frac{1}{S},\qquad f''(S)=-\frac{1}{S^2}.
$$

Ito's lemma gives the translation rule:

$$
dX_t=f'(S_t)dS_t+\frac{1}{2}f''(S_t)(dS_t)^2.
$$

Under \(Q\), we plug the risk-neutral GBM:

$$
dS_t=rS_t\,dt+\sigma S_t\,dW_t.
$$

The only non-trivial part is the square term. In stochastic calculus, the key identity is:

$$
(dW_t)^2=dt.
$$

So:

$$
(dS_t)^2=(\sigma S_t\,dW_t)^2=\sigma^2S_t^2\,dt.
$$

Now inject everything into Ito and simplify.

You get the log-price dynamics under \(Q\):

$$
dX_t=\left(r-\frac{1}{2}\sigma^2\right)dt+\sigma\,dW_t.
$$

So drift and diffusion for the log are:

$$
\tilde{\mu}=r-\frac{1}{2}\sigma^2,\qquad \tilde{\sigma}=\sigma.
$$

Now you integrate over \([0,T]\):

$$
X_T=X_0+\left(r-\frac{1}{2}\sigma^2\right)T+\sigma W_T,
$$

with:

$$
X_0=\ln(S_0).
$$

And the decisive fact:

$$
W_T\sim\mathcal{N}(0,T).
$$

So:

$$
\ln(S_T)\sim\mathcal{N}\left(\ln(S_0)+\left(r-\frac{1}{2}\sigma^2\right)T,\ \sigma^2T\right).
$$

Which means \(S_T\) is log-normal under \(Q\).

And that's exactly what you need to compute the expectation of a European payoff.

Now we apply the pricing rule again:

$$
C_0=e^{-rT}\mathbb{E}^Q\left[(S_T-K)^+\right].
$$

Because \(S_T\) is log-normal under \(Q\), this expectation has a closed form.

The standard Black-Scholes formula for a European call is:

$$
C_0=S_0N(d_1)-Ke^{-rT}N(d_2).
$$

Where \(N(\cdot)\) is the standard normal CDF, and:

$$
d_1=\frac{\ln(S_0/K)+\left(r+\frac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}},\qquad
d_2=d_1-\sigma\sqrt{T}.
$$

And you can read the objects directly.

Under \(Q\), the probability the option finishes in the money is:

$$
N(d_2)=\mathbb{P}^Q(S_T>K).
$$

And the call delta in Black-Scholes is:

$$
\Delta_{\text{call}}=N(d_1).
$$

So the formula is not a prediction. It's a replication writing: a piece of underlying minus discounted cash.

Role of \(r\):

It discounts the strike via \(Ke^{-rT}\). It enters \(d_1\) and \(d_2\), so it affects the risk-neutral in-the-money probability.

Role of \(\sigma\):

It controls the dispersion of \(S_T\) because the call payoff is convex. More dispersion increases the call's value. \(\mu\) does not appear because pricing is done under \(Q\).

The price depends on \(r\) and \(\sigma\).

Same method as always: theory -> simulation -> comparison.

Under \(Q\), you simulate with \(r\) instead of \(\mu\). Exponential scheme:

$$
S_{t+\Delta t}=S_t\exp\left(\left(r-\frac{1}{2}\sigma^2\right)\Delta t+\sigma\sqrt{\Delta t}\,Z\right),
\qquad Z\sim\mathcal{N}(0,1).
$$

And if you only want \(S_T\), you can simulate the terminal law directly:

$$
S_T=S_0\exp\left(\left(r-\frac{1}{2}\sigma^2\right)T+\sigma\sqrt{T}\,Z\right),
\qquad Z\sim\mathcal{N}(0,1).
$$

Payoff:

$$
\text{payoff}=\max(S_T-K,0).
$$

Monte Carlo estimator:

$$
\widehat{C}_{MC}=e^{-rT}\frac{1}{N}\sum_{i=1}^{N}\max(S_T^{(i)}-K,0).
$$

Standard error:

$$
SE=\frac{\operatorname{Std}\left(e^{-rT}\max(S_T-K,0)\right)}{\sqrt{N}}.
$$

Expected reading: as \(N\) increases, \(\widehat{C}_{MC}\) converges to the Black-Scholes price and \(SE\) shrinks like \(1/\sqrt{N}\).
