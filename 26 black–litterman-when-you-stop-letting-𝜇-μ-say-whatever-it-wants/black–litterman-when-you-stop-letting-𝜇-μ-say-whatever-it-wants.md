Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Black-Litterman When You Stop Letting $\mu$ Say Whatever It Wants

With Markowitz, then with CAPM, we already closed a first loop. Markowitz set up the allocation problem. CAPM set up the equilibrium anchor through the market portfolio. So now, the point of friction is not hard to see anymore: the moment you want to go back to an actual allocation, the thing that breaks the portfolio is almost never $\Sigma$. Covariance moves, yes, it is imperfect, yes, but it can be estimated, regularized, constrained. The real problem is $\mu$. That is the variable that injects the most fragility into the machine.

And that is where a lot of people get trapped without even noticing it. Because on paper, mean-variance optimization looks clean. You plug in an expected return estimator, a covariance matrix, you solve, you get weights. It looks like precision. Except in practice, if your estimate of $\mu$ moves even a little, the weights can fly all over the place. So the optimizer does not "reveal" a portfolio. It amplifies the slightest error you allowed into $\mu$. It takes an estimate that was already fragile, then pushes it to its most extreme version.

Black-Litterman starts exactly there.

Not as a decorative patch on top of Markowitz. Not as an elegant opinion you add to make the whole thing look nicer. It is a discipline imposed on $\mu$. A way of saying: instead of treating expected return as a number given once and for all, we are going to treat it as an uncertain object that gets updated properly. So instead of starting from a raw empirical mean and pretending it tells the truth, we start from an observable equilibrium anchor, then we add views as controlled deformations, with an explicit confidence level.

That is the core of the model.

If you accept mean-variance logic in equilibrium, then you do not get to look at the market portfolio as just any random vector of weights. It necessarily implies a return structure that makes it coherent.

That is exactly the structure Black-Litterman reconstructs.

$$
R \in \mathbb{R}^{N}
$$

is the vector of returns of the risky assets, $\Sigma$ the covariance matrix, $r_f$ the risk-free rate, and $w_M$ the observed market weights with

$$
\mathbf{1}^{\top}w_M = 1
$$

The market return is

$$
R_M = w_M^{\top}R
$$

its mean is

$$
\mu_M = \mathbb{E}[R_M]
$$

and its variance is

$$
\sigma_M^2 = w_M^{\top}\Sigma w_M
$$

From there, we define an aggregate price of risk through

$$
\lambda = \frac{\mu_M - r_f}{w_M^{\top}\Sigma w_M}
$$

This quantity tells you how much excess return the market demands per unit of aggregate variance. And once you have that, you can reconstruct the implied returns consistent with the market portfolio:

$$
\pi = r_f\mathbf{1} + \lambda\Sigma w_M
$$

That equation is much more important than it looks. $\Sigma w_M$ is the marginal contribution of each asset to the risk of the market portfolio. $\lambda$ turns that risk into a required premium. And $\pi$ is not "the truth" about future returns. It is the equilibrium prior. In other words, the set of returns you are allowed to take as a starting point if you want to remain coherent with the fact that $w_M$ is observed in the world.

So Black-Litterman begins by refusing a very common mistake: believing that you can invent $\mu$ freely without paying the price of that invention.

Then we add views. But again, there is no room for blur here. A view, in this framework, is not "I like this asset" or "I feel this one is going up." A view is a linear constraint on expected returns, so it has to be written properly.

If you have $K$ views, you stack them in a matrix

$$
P \in \mathbb{R}^{K \times N}
$$

and a vector

$$
q \in \mathbb{R}^{K}
$$

then you write

$$
P\mu = q + \epsilon,
\qquad
\epsilon \sim \mathcal{N}(0,\Omega)
$$

And there, $\Omega$ becomes the decisive piece. Because that is what separates an intuition from an actual model. If you say your view is very strong, $\Omega$ is small. If you say it is fragile, $\Omega$ is large. So you no longer get to have a "strong" opinion without writing that strength into the variance of the opinion. In other words, confidence is no longer a word. It becomes a parameter.

That is why Black-Litterman is clean. It forces coherence between what you believe and how strongly you claim to believe it.

The Bayesian form of the model then locks everything else into place. We put a prior on $\mu$, centered on $\pi$:

$$
\mu \sim \mathcal{N}(\pi,\tau\Sigma)
$$

where $\tau>0$ controls the rigidity of the prior. Small $\tau$, the prior is stiff, so the market keeps a lot of weight. Large $\tau$, the prior becomes more flexible, so the views can deform it more easily.

Then we combine the prior and the views, and we get the posterior mean:

$$
\mu_{BL}
= \left[(\tau\Sigma)^{-1} + P^{\top}\Omega^{-1}P\right]^{-1}
\left[(\tau\Sigma)^{-1}\pi + P^{\top}\Omega^{-1}q\right]
$$

That is the center of the lesson.

There is no magic here either. What this formula says is simply that $\mu_{BL}$ is a weighted average between what the market implies and what your views impose. If $\Omega \to \infty$, your views have almost no force, so you fall back toward $\pi$. If $\Omega \to 0$, you are almost forcing the model to satisfy $P\mu \approx q$, and $\tau$ decides how much you allow the market prior to be bent in the first place.

In other words, Black-Litterman does not eliminate judgment. It puts it under constraint.

Once you have $\mu_{BL}$, you go back to a standard mean-variance logic. Except that this time, you are not throwing a raw, nervous, hysterical $\mu$ into the optimizer. You are feeding it a stabilized $\mu$. So the weights stop being the violent projection of a fragile estimate. They become the consequence of a slow equilibrium, corrected by views whose confidence has been explicitly priced in.

In a simple version, the risky direction is written as

$$
w_{BL} \propto \Sigma^{-1}(\mu_{BL} - r_f\mathbf{1})
$$

and if you want a fully invested constraint, you then normalize to get

$$
\mathbf{1}^{\top}w = 1
$$

Or you move to a quadratic program if you want to add more realistic constraints.

What really matters here is that the gain of Black-Litterman is not some magical promise of outperformance. The gain is control. You know where your prior comes from. You know how your views deformed it. You know what level of confidence you injected. And above all, you are no longer letting an unstable estimate of $\mu$ run the whole allocation as if it were a truth.

If you want to say it more directly: Markowitz becomes dangerous when $\mu$ talks too loudly. Black-Litterman lowers its volume, ties it back to the market, then lets it speak again, but under supervision.

On the Python side, the logic is exactly the same. There is no need to add drama. You build the blocks in the natural order of the reasoning: estimate $\Sigma$, define $w_M$, reconstruct $\pi$, encode $P$, $q$, $\Omega$, compute $\mu_{BL}$, then compare the resulting allocation with the one you would get from a plain empirical $\mu$.

```python
import numpy as np


def implied_equilibrium_returns(Sigma, w_m, rf, mu_m):
    Sigma = np.asarray(Sigma, float)
    w_m = np.asarray(w_m, float).reshape(-1, 1)
    ones = np.ones((Sigma.shape[0], 1))

    sigma_m2 = float(w_m.T @ Sigma @ w_m)
    lam = (mu_m - rf) / sigma_m2 if sigma_m2 > 0 else np.nan
    pi = rf * ones + lam * (Sigma @ w_m)

    return pi.ravel(), lam


def black_litterman_posterior(Sigma, pi, P, q, Omega, tau=0.02):
    Sigma = np.asarray(Sigma, float)
    pi = np.asarray(pi, float).reshape(-1, 1)
    P = np.asarray(P, float)
    q = np.asarray(q, float).reshape(-1, 1)
    Omega = np.asarray(Omega, float)

    inv_tauSigma = np.linalg.inv(tau * Sigma)
    A = inv_tauSigma + P.T @ np.linalg.inv(Omega) @ P
    b = inv_tauSigma @ pi + P.T @ np.linalg.inv(Omega) @ q

    mu_bl = np.linalg.solve(A, b)
    return mu_bl.ravel()


def mv_direction(Sigma, mu, rf):
    Sigma = np.asarray(Sigma, float)
    mu = np.asarray(mu, float).reshape(-1, 1)
    ones = np.ones((Sigma.shape[0], 1))

    w = np.linalg.solve(Sigma, mu - rf * ones)
    w = w.ravel()

    return w / w.sum()
```

The code tells the exact same story as the equations. First, you reconstruct $\pi$, which means the implied equilibrium returns. Then you take your views. Then you do the Bayesian update. Only after that do you go back to allocation.

And the views themselves can be written without any drama. A relative view such as "asset A should outperform asset B by 2%" becomes a row of $P$ with $+1$ on A, $-1$ on B, and $q_k=0.02$. An absolute view such as "asset C should return 8%" becomes a row with $1$ on C and $q=0.08$.

```python
N = 6
a, b, c = 0, 1, 2

P = np.zeros((2, N))
P[0, a] = 1.0
P[0, b] = -1.0   # mu_a - mu_b = 2%

P[1, c] = 1.0    # mu_c = 8%

q = np.array([0.02, 0.08])

Omega = np.diag([0.02**2, 0.03**2])
```

What matters here is not the example itself. It is the discipline it imposes. A view has to have a form. A confidence level has to have a variance. An allocation has to be linked to an observable prior. Otherwise, you do not have a model. You just have a preference wrapped in formalism.

And that is why Black-Litterman fits so naturally after CAPM. CAPM gave you the market portfolio as the central equilibrium object. Black-Litterman takes that exact anchor, then says: good, now that we have this equilibrium, how do we deform it without losing control? How do we add information without letting noise take power? How do we correct the market without going back to an empirical $\mu$ that explodes the moment the sample shifts a little?

The answer is precisely this prior $\pi$, these views $(P,q)$, this confidence matrix $\Omega$, and this parameter $\tau$ that controls how rigid the whole structure is.

So if we sum it up without flattening the substance: Markowitz optimizes with a $\mu$ it assumes is given. Black-Litterman starts by saying that $\mu$ is not given at all. It is fragile. It is uncertain. So first you tie it to a slow structure, the market, and only then do you allow controlled deformations.

