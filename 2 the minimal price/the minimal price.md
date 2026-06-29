Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-2-the-minimal-price-dynamics-gbm-model

A risk transfer, a premium paid to move a convexity.

That's why I insist that option trading is in no way a directional bet, and assume that the market will never give you the exact info of what will happen tomorrow.

Our role, especially if we position ourselves on options, is mainly going to be to manage convexity and do everything to keep the premium intact, whether the market goes up or down.

Basically the only reliable info the market gives you is a price.

So to go from one price to another, or from a favorable scenario to an unfavorable one inside this convexity, well you always need "a dynamic", in the physical sense of the term, and so if there is a dynamic, then we must necessarily have a distribution of this price that we will call \(S_t\).

So we choose a deliberately poor dynamic because it puts the minimum of parameters to produce a usable distribution.

This geometric Brownian motion is perfect for this exercise because it reduces this dynamic to one sentence:

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t,\qquad S_0 > 0.
$$

This equation says that the price \(S_t\) changes with very small variations \(dS_t\), and that this change decomposes into two pieces.

The first,

$$
\mu S_t\,dt
$$

is a regular drift: proportional to the price and proportional to time, weighted by \(\mu\).

The second,

$$
\sigma S_t\,dW_t
$$

is a random shock proportional to the price, with intensity \(\sigma\), carried by the noise \(dW_t\).

And

$$
S_0 > 0
$$

just says that the starting price is positive, so we can take its logarithm without any problem.

The price moves in multiplied percentages, and the logarithm transforms these percentages into additions.

We therefore set

$$
X_t = \ln(S_t),
$$

which just comes down to saying that \(X_t\) is the log of the price, the logarithm of \(S_t\). From there, the objective to parameterize the dynamic is to write how \(X_t\) moves.

For that, we apply Ito's lemma to the function \(f(S)=\ln(S)\):

$$
f'(S)=\frac{1}{S},\qquad f''(S)=-\frac{1}{S^2}.
$$

Ito then says that if \(X_t=f(S_t)\), we have

$$
dX_t = f'(S_t)dS_t + \frac{1}{2}f''(S_t)(dS_t)^2.
$$

This writing only says that there is a "transport" term \(f'(S_t)dS_t\) and a correction term due to curvature \(f''\), because noise does not behave like an ordinary variation.

We replace \(dS_t\), by what we fixed at the start,

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t.
$$

Then we must write \((dS_t)^2\). In this calculation, what matters is that \((dW_t)^2=dt\) and that the terms in \(dt^2\) or \(dt\,dW_t\) are negligible at infinitesimal order.

So

$$
(dS_t)^2 = (\sigma S_t\,dW_t)^2 = \sigma^2 S_t^2(dW_t)^2 = \sigma^2 S_t^2\,dt.
$$

Injecting everything, we obtain a dynamics for the log-price:

$$
dX_t = \left(\mu-\frac{1}{2}\sigma^2\right)dt + \sigma\,dW_t.
$$

The log-price advances with a constant trend \(\mu-\frac{1}{2}\sigma^2\) multiplied by \(dt\) and it undergoes a noise of size \(\sigma\) multiplied by \(dW_t\).

And we can go even lower in the scale:

$$
dX_t = a\,dt + b\,dW_t
$$

with

$$
a=\mu-\frac{1}{2}\sigma^2,\qquad b=\sigma,
$$

which comes down to saying that \(X_t\) is the sum of a deterministic term and a random term.

We then cumulate on \([0,t]\), which comes down to writing the same relation over a finite duration:

$$
X_t = X_0 + \left(\mu-\frac{1}{2}\sigma^2\right)t + \sigma W_t,
$$

and

$$
X_0 = \ln(S_0)
$$

just says that the initial log-price is the logarithm of the initial price.

The decisive point is that \(W_t\) is normal:

$$
W_t \sim \mathcal{N}(0,t).
$$

This writing says that the noise cumulated over a duration \(t\) is a normal with mean 0 and variance \(t\). So \(X_t\), which is a constant plus a constant times \(t\) plus \(\sigma W_t\), is also normal.

In other words,

$$
\ln(S_t)=X_t \sim \mathcal{N}(m(t),v(t)),
$$

where

$$
m(t)=\ln(S_0)+\left(\mu-\frac{1}{2}\sigma^2\right)t,\qquad v(t)=\sigma^2t.
$$

These two equalities give the mean and the dispersion of the log-price: the mean is \(\ln(S_0)\) plus the drift accumulated on \(t\) and the dispersion, in the sense of variance, is \(\sigma^2t\).

We then go back to the price, because an option pays on \(S_T\), not on \(\ln(S_T)\).

And the return to the price is an identity:

$$
S_t = \exp(\ln S_t)=\exp(X_t).
$$

This line says that the price is the exponential of the log-price.

So, if the log-price is normal, the price is log-normal, so we can even write \(S_t\) explicitly:

$$
S_t = S_0\exp\left(\left(\mu-\frac{1}{2}\sigma^2\right)t+\sigma W_t\right),
$$

which says that the price is the initial price multiplied by an exponential composed of a drift and a noise.

And from there, we obtain the two sentences that matter for the mean dynamics and the dispersion:

$$
\mathbb{E}[S_t] = S_0e^{\mu t},
$$

which says that the mean of the price grows exponentially at rate \(\mu\) and

$$
\operatorname{Var}(S_t) = S_0^2e^{2\mu t}\left(e^{\sigma^2t}-1\right),
$$

which says that dispersion grows like an exponential, and that it accelerates with \(\sigma^2t\).

For our Python simulation we can take the GBM dynamics, simulate \(S_t\), on \(t\in[0,T]\), extract \(S_T\), then verify two things:

that

$$
X_T = \ln(S_T)
$$

is indeed Normal with parameters \(m(T),v(T)\), that \(S_T\) is indeed log-normal, and that its moments \(\mathbb{E}[S_T]\) and \(\operatorname{Var}(S_T)\) match the theory.

We first import the tools:

numpy for logs, exponentials and normal generation.

matplotlib to plot histograms and trajectories.

Theoretical parameters: \(m(T),v(T)\) and moments of \(S_T\).

```python
def gbm_ln_params(S0, mu, sigma, T):
    m = np.log(S0) + (mu - 0.5 * sigma**2) * T
    v = sigma**2 * T
    return m, v
```

This function encodes exactly what has just been shown:

$$
X_T=\ln(S_T)\sim\mathcal{N}(m(T),v(T)),
$$

$$
m(T)=\ln(S_0)+\left(\mu-\frac{1}{2}\sigma^2\right)T,\qquad v(T)=\sigma^2T.
$$

It therefore returns the theoretical mean and variance of the log-price at maturity.

```python
def gbm_ST_moments(S0, mu, sigma, T):
    mean = S0 * np.exp(mu * T)
    var = (S0**2) * np.exp(2 * mu * T) * (np.exp(sigma**2 * T) - 1.0)
    return mean, var
```

This second function returns the two closed moments of the log-normal:

$$
\mathbb{E}[S_T]=S_0e^{\mu T},
$$

$$
\operatorname{Var}(S_T)=S_0^2e^{2\mu T}\left(e^{\sigma^2T}-1\right).
$$

Log-normal density, to overlay theory and histogram:

```python
def lognormal_pdf(s, m, v):
    s = np.asarray(s)
    pdf = np.zeros_like(s, dtype=float)
    mask = s > 0
    pdf[mask] = (1.0 / (s[mask] * np.sqrt(2*np.pi*v))) * np.exp(
        -(np.log(s[mask]) - m)**2 / (2*v)
    )
    return pdf
```

This function builds the theoretical density of \(S_T\) using \(m\) and \(v\) of the log:

$$
f_{S_T}(s)=\frac{1}{s\sqrt{2\pi v}}\exp\left(-\frac{(\ln s-m)^2}{2v}\right),\qquad s>0.
$$

The mask \(s>0\) is mandatory: no density for \(s\le 0\).

GBM simulation: construction by increments of the log.

```python
def simulate_gbm_paths(S0, mu, sigma, T, nsteps, N, seed=42):
    rng = np.random.default_rng(seed)
    dt = T / nsteps
    Z = rng.standard_normal((N, nsteps))
    increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    S = np.empty((N, nsteps + 1), dtype=float)
    S[:, 0] = S0
    S[:, 1:] = S0 * np.exp(np.cumsum(increments, axis=1))
    return S
```

This function simulates \(N\) discrete trajectories, over `nsteps` time steps.

`dt = T/nsteps`: a time step.

`Z`: a matrix of i.i.d. Gaussian shocks:

$$
Z \sim \mathcal{N}(0,1).
$$

The central point is increments:

$$
\Delta X = \left(\mu-\frac{1}{2}\sigma^2\right)dt+\sigma\sqrt{dt}\,Z.
$$

It is exactly the discretization of:

$$
dX_t = \left(\mu-\frac{1}{2}\sigma^2\right)dt+\sigma dW_t.
$$

Then `np.cumsum(increments, axis=1)` does the cumulative sum:

$$
X_{t_k}-X_0=\sum_{j=1}^{k}\Delta X_j.
$$

Finally `S0 * exp(cumsum)` reconstructs the price:

$$
S_{t_k}=S_0\exp\left(\sum_{j=1}^{k}\Delta X_j\right).
$$

So the simulation does not "hack" \(S\) directly: it accumulates the log then exponentiates, which is the right structure for GBM.

Main block: theory then Monte Carlo.

```python
S0 = 100.0
mu = 0.08
sigma = 0.02
T = 1.0
nsteps = 252
```

`S0`: initial price.

`\mu`: drift.

`\sigma`: volatility.

`T`: horizon.

`252 steps`: daily discretization, type trading days.

```python
mT, vT = gbm_ln_params(S0, mu, sigma, T)
mean_th, var_th = gbm_ST_moments(S0, mu, sigma, T)
```

Here are computed:

parameters of the normal of \(\ln(S_T)\) and theoretical mean/variance of \(S_T\).

Then Monte Carlo comparison:

```python
Ns = [1_000, 10_000, 100_000]
for N in Ns:
    S = simulate_gbm_paths(S0, mu, sigma, T, nsteps, N, seed=42)
    ST = S[:, -1]
    mean_emp = ST.mean()
    var_emp = ST.var(ddof=1)
```

`ST = S[:, -1]`: last column, therefore \(S_T\).

`mean_emp`: empirical mean.

`var_emp`: empirical variance, with `ddof=1` for sample variance.

Printing the errors shows the convergence: when \(N\) increases, the simulation-theory gap shrinks.
