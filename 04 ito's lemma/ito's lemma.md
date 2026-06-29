Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-4-ito's-lemma

The market only gives you a price. And to go from a price to scenarios... you need a dynamics. So a distribution of \(S_T\).

GBM is exactly that: a "poor" dynamics. Few parameters... but enough to produce a usable law.

And this dynamics is stochastic by definition.

So the moment you transform the price like take a log, move to returns, look at a payoff, you are not doing a "classic" transformation.

You are transforming a noisy object. And if you handle that as if it were standard analysis then inevitably you'll get the drift wrong.

So you'll get the law wrong. And then you'll get everything else wrong.

That's exactly why GBM without Ito's lemma doesn't "hold".

Ito's lemma is the translation rule: it tells you how a function \(f(S_t)\) moves when \(S_t\) moves with noise. It's what explains why \(X_t=\ln(S_t)\) does not have drift \(\mu\) but \(\mu-\frac{1}{2}\sigma^2\). And this correction is not an intuition: it's the mechanics imposed by the term \((dW_t)^2=dt\).

We keep the same base:

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t,\qquad S_0>0.
$$

The goal here is simple: go from \(S_t\) to

$$
X_t=\ln(S_t),
$$

read properly the drift and diffusion of \(X_t\) then verify in simulation that the observed drift of \(X_t\) matches this theoretical drift.

You want to go from \(S_t\) to \(\ln(S_t)\). So you take the object, you transform it... but you don't forget one detail: you are in stochastic calculus. That means that when you do a transformation, you are not doing classic analysis... you are doing a translation.

Here the translation is Ito.

We start from the base:

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t,\qquad S_0>0.
$$

And now you say: ok, I want to look at the log-price:

$$
X_t=\ln(S_t).
$$

In other words, you have a function \(f\) acting on \(S_t\). And that function is just the log:

$$
f(S)=\ln(S).
$$

And there... you don't argue: you differentiate. Because all of Ito is there.

$$
f'(S)=\frac{1}{S},\qquad f''(S)=-\frac{1}{S^2}.
$$

Now you apply the translation rule. Ito tells you exactly how \(X_t=f(S_t)\) moves when \(S_t\) moves with noise:

$$
dX_t=f'(S_t)dS_t+\frac{1}{2}f''(S_t)(dS_t)^2.
$$

So you replace \(dS_t\) by the GBM dynamics.

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t.
$$

And now there is the only place where people mess up: \((dS_t)^2\).

Because in stochastic calculus, noise is not "small". It has a geometry.

And that geometry is:

$$
(dW_t)^2=dt.
$$

So when you square, everything in \(dt^2\) and in \(dt\,dW_t\) collapses... and what survives is the term in \((dW_t)^2\).

So:

$$
(dS_t)^2=(\sigma S_t\,dW_t)^2=\sigma^2S_t^2(dW_t)^2=\sigma^2S_t^2\,dt.
$$

And then you inject everything into Ito, clearly:

$$
dX_t=\frac{1}{S_t}\left(\mu S_t\,dt+\sigma S_t\,dW_t\right)
+\frac{1}{2}\left(-\frac{1}{S_t^2}\right)\left(\sigma^2S_t^2\,dt\right).
$$

You simplify... and you finally read the truth of the log-price:

$$
dX_t=\left(\mu-\frac{1}{2}\sigma^2\right)dt+\sigma\,dW_t.
$$

So the log does not "keep" \(\mu\).

It corrects it.

And that correction comes only from the term \(\frac{1}{2}f''(S_t)(dS_t)^2\).

Just the mechanics of \((dW_t)^2=dt\). Now you can integrate over \([0,t]\), because now you have a simple SDE: constant drift + constant diffusion.

So you accumulate:

$$
X_t=X_0+\left(\mu-\frac{1}{2}\sigma^2\right)t+\sigma W_t,
$$

with

$$
X_0=\ln(S_0).
$$

And there you read the law directly because the decisive point is:

$$
W_t\sim\mathcal{N}(0,t).
$$

So \(X_t\) is Normal and you can read without effort:

$$
\mathbb{E}[X_t]=\ln(S_0)+\left(\mu-\frac{1}{2}\sigma^2\right)t,
$$

$$
\operatorname{Var}(X_t)=\sigma^2t.
$$

And now you understand why the drift contains \(-\frac{1}{2}\sigma^2\).

Because in stochastic calculus, noise is not a "small classic variation".

The key point, again, is:

$$
(dW_t)^2=dt.
$$

So as soon as a function is curved and log is curved the Ito term adds (or removes) a deterministic piece in \(dt\). Here log is concave, so \(f''<0\).

So the correction removes \(-\frac{1}{2}\sigma^2\) from the drift.

Simple interpretation: \(S_t\) moves by multiplication, and log transforms that into addition... but this transformation "pays" a cost because of curvature. Volatility creates a mean term on the log-price, and that term is exactly \(-\frac{1}{2}\sigma^2\). This is not an intuition. It's Ito's mechanics.

Now the Python part. The idea is not just to look at \(S_T\). The idea is to look at \(X_t=\ln(S_t)\) and verify two things:

that \(X_T\) indeed has a mean and a variance consistent with theory and above all that the empirical drift of \(X_t\) is indeed \(\tilde{\mu}=\mu-\frac{1}{2}\sigma^2\).

We reuse exactly the GBM pipeline already used. The pipeline already simulates GBM via log increments, so everything is consistent with the Ito part. We just add a few lines to measure \(X_T\) and estimate \(\tilde{\mu}\).

Right after the parameters, after `nsteps = 252`, you add:

```python
dt = T / nsteps
mu_tilde = mu - 0.5 * sigma**2
```

Right after the theory block, after the existing prints, you add:

```python
print(f"mu_tilde (drift of ln S) = {mu_tilde:.6f}")
```

Inside the Monte Carlo loop, right after `ST = S[:, -1]`, you add:

```python
XT = np.log(ST)
mean_X_emp = XT.mean()
var_X_emp = XT.var(ddof=1)

mean_X_th = mT
var_X_th  = vT
```

Still inside the loop, you add the empirical drift estimate via increments:

```python
X = np.log(S)
dX = X[:, 1:] - X[:, :-1]
mu_tilde_hat = dX.mean() / dt
```

Then you add the prints:

```python
print(f"E[X_T]   = {mean_X_emp:.6f}    (error = {mean_X_emp - mean_X_th:+.6e})")
print(f"Var[X_T] = {var_X_emp:.6f}    (error = {var_X_emp - var_X_th:+.6e})")
print(f"mu_tilde_hat = {mu_tilde_hat:.6f}    (error = {mu_tilde_hat - mu_tilde:+.6e})")
```

Expected reading:

When \(N\) increases, \(\mathbb{E}[X_T]\) moves closer to \(m(T)\).

\(\operatorname{Var}(X_T)\) moves closer to \(v(T)\).

And especially \(\tilde{\mu}\) moves closer to \(\mu-\frac{1}{2}\sigma^2\).
