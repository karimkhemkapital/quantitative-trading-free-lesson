Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Markowitz Closing The Return Risk Problem Through Geometry

up to this point, we were talking about propagation, memory, constraint, regime. here, on the surface, the topic looks more classical: several assets, a portfolio, a return / risk trade-off. but if you look at it properly, the real subject is not "buying positions." the real subject is: how do you organize a point inside a space where everything moves together.

and that is exactly where Markowitz comes in.

not as a metaphysical truth about the market. not as some sacred theory. just as a geometric closure of the problem.

you take $N$ risky assets. you denote their returns by a random vector then you keep two objects

$$
\mu = E[R] \in \mathbb{R}^N,
\qquad
\Sigma = Cov(R) \in \mathbb{R}^{N \times N}
$$

$\mu$ is the expected average return level. $\Sigma$ is the co-movement structure, so the way assets vibrate together.

and already, there is an important idea in there: risk is not just "each asset moves." portfolio risk is also about the way those moves combine. in other words, structure matters more than names.

a portfolio, then, is just a weight vector with the budget constraint

$$
\mathbf{1}^\top w = 1
$$

from there, the portfolio becomes a geometric object. its expected return is

$$
\mu_p(w) = w^\top \mu
$$

and its risk in the Markowitz sense is

$$
\sigma_p^2(w) = w^\top \Sigma w,
\qquad
\sigma_p(w) = \sqrt{w^\top \Sigma w}.
$$

and at that point, the mechanics are already there.

you are no longer looking at separate assets. you are looking at a transformation. you send a weight vector into a geometry defined by $\mu$ and $\Sigma$, and it sends back a pair: return on one side, risk on the other.

that is the closure of the problem.

and the word "efficient," deep down, just means one very simple thing: non-dominated.

a portfolio is efficient if nobody does strictly better than it. no higher return at identical risk. no lower risk at identical return. so efficiency here is not a moral judgment, and not a belief either. it is just a frontier property.

to feel the thing properly, the easiest way is to start again with $N=2$.

you have two assets, with weights $(w, 1-w)$. the expected portfolio return becomes

$$
\mu_p(w) = w\mu_1 + (1-w)\mu_2
$$

and the variance

$$
\sigma_p^2(w)
= w^2\sigma_1^2
+ (1-w)^2\sigma_2^2
+ 2w(1-w)\rho_{12}\sigma_1\sigma_2.
$$

and there, the whole intuition of diversification comes from one single place

$$
\rho_{12} < 1.
$$

if correlation is not perfect, then you can build combinations where the portfolio moves less than either asset taken on its own. so diversification is not some magic formula. it is just a geometric effect of non-alignment.

and that reconnects very cleanly with the whole thread we had before: when the regime locks up, when constraints propagate, when everything synchronizes, correlations rise toward 1. and at that point, the diversification margin folds back in.

so Markowitz is not lying. it is just speaking about a world where the covariance structure remains exploitable.

now you move to $N$ assets. same logic, same structure

$$
\mu_p = w^\top \mu,
\qquad
\sigma_p^2 = w^\top \Sigma w.
$$

and the central problem becomes:

for a target return $\bar{\mu}$, which portfolio minimizes variance?

$$
\min_w \; w^\top \Sigma w
\quad \text{s.t.} \quad
w^\top \mu = \bar{\mu},
\qquad
\mathbf{1}^\top w = 1.
$$

that is the core of the efficient frontier.

you are not looking for "the best portfolio" in the absolute sense. you are looking, for each target return, for the least risky combination possible. so you are building a frontier. an envelope. an edge.

in the unconstrained shorting case, the problem closes analytically. you write the Lagrangian

$$
L(w, \lambda_1, \lambda_2)
= w^\top \Sigma w
- \lambda_1(w^\top \mu - \bar{\mu})
- \lambda_2(\mathbf{1}^\top w - 1).
$$

and the first-order condition gives

$$
\nabla_w L = 0
\Rightarrow
2\Sigma w - \lambda_1\mu - \lambda_2\mathbf{1} = 0.
$$

so

$$
\Sigma w = \frac{\lambda_1}{2}\mu + \frac{\lambda_2}{2}\mathbf{1}.
$$

and there, the reading becomes clean and the optimal portfolio lives in the space spanned by only two directions

$$
\Sigma^{-1}\mu
\qquad \text{and} \qquad
\Sigma^{-1}\mathbf{1}.
$$

in other words, even when you have $N$ assets, the optimal structure is still compressed by the geometry of the problem.

to condense that geometry, you define

$$
A = \mathbf{1}^\top\Sigma^{-1}\mathbf{1},
\qquad
B = \mathbf{1}^\top\Sigma^{-1}\mu,
\qquad
C = \mu^\top\Sigma^{-1}\mu,
\qquad
D = AC - B^2.
$$

and as long as $\mu$ is not collinear with $\mathbf{1}$ you have $D>0$, and the family of minimum-variance portfolios is written as

$$
w(\bar{\mu})
= \Sigma^{-1}
\left[
\frac{C-\bar{\mu}B}{D}\mathbf{1}
+ \frac{\bar{\mu}A-B}{D}\mu
\right].
$$

when you plot $(\sigma(\bar{\mu}), \bar{\mu})$, you get the famous hyperbola-type curve. and again, it has to be read properly: the whole curve is not "efficient." the lower branch is dominated. only the upper branch matters.

what does that mean in practice? it means that past a certain point, you can always find another portfolio that does better for the same risk. so efficiency is not "the whole curve." it is just the non-dominated edge.

then you leave the clean world of equations and go back to the real world. that is where you put the constraints back in.

no shorting

$$
w_i \ge 0.
$$

concentration cap, if needed

$$
w_i \le w_{\max}.
$$

and the problem becomes a convex quadratic program

$$
\min_w \; w^\top\Sigma w
\quad \text{s.t.} \quad
w^\top\mu = \bar{\mu},
\qquad
\mathbf{1}^\top w = 1,
\qquad
0 \le w_i \le w_{\max}.
$$

and there, the frontier changes nature.

it folds inward. some target returns simply become impossible. and the optimal portfolios stick to the edges: weights at zero, weights at the cap. they are no longer "fluid" combinations. they are corners of a polytope. geometry under constraint.

up to here, everything is still risky-only. now you add the risk-free asset $r_f$. and that is where there is an important conceptual shift.

before, you were only choosing a risky portfolio.

now, you separate two things: the risky mix, and the leverage.

you define excess returns

$$
\mu_{ex} = \mu - r_f\mathbf{1}.
$$

if $w_R$ are the weights on risky assets, and $w_f$ is the weight on the risk-free asset, then

$$
w_f + \mathbf{1}^\top w_R = 1.
$$

the portfolio return becomes

$$
E[R_p]
= w_f r_f + w_R^\top \mu
= r_f + w_R^\top(\mu - r_f\mathbf{1})
= r_f + w_R^\top \mu_{ex}.
$$

and the risk

$$
\sigma_p = \sqrt{w_R^\top\Sigma w_R}.
$$

and there, the frontier becomes a straight line. more precisely, a line starting from $r_f$ in the risk / return plane. the only question left is: which slope do you choose.

and that slope is the Sharpe ratio

$$
S(w_R)
= \frac{w_R^\top\mu_{ex}}
{\sqrt{w_R^\top\Sigma w_R}}.
$$

the logic is clean: you are no longer just looking for a portfolio. you are looking for the risky direction that gives the maximum slope. the one that converts one unit of risk into the most excess return.

that is the tangency portfolio.

and there is one point that has to stay clean, otherwise the whole reasoning twists: Sharpe is scale-invariant. so the tangency portfolio is first a direction, not a level. if you try to impose at the same time that weights sum to 1 and some arbitrary excess-return gauge, you risk breaking the logic.

the proper reading is

$$
w_T \propto \Sigma^{-1}\mu_{ex}
$$

that is the tangency direction.

if you want to display it as a "100% risky" portfolio, only then do you normalize

$$
\tilde{w}_T
= \frac{\Sigma^{-1}\mu_{ex}}
{\mathbf{1}^\top \Sigma^{-1}\mu_{ex}}.
$$

and from there, the capital allocation line becomes

$$
E[R_p] = r_f + S_T\sigma_p,
\qquad
S_T
= \frac{\tilde{w}_T^\top\mu_{ex}}
{\sqrt{\tilde{w}_T^\top\Sigma\tilde{w}_T}}.
$$

and that line is the real closure of the problem once the risk-free asset is added.

every efficient allocation becomes a mix between two blocks: the risk-free asset and the tangency portfolio. that is two-fund separation. not because it looks elegant on a slide, because the geometry of the problem forces a unique slope.

and there, on the code side, you have to stay inside the same logic. not making plots for the sake of plots. not making it pretty. rebuilding the calculation chain, checking that the frontier exists, then seeing how estimation and constraints distort it.

you start from prices, build log-returns, estimate and annualize them, then define the basic blocks

```python
import numpy as np
import pandas as pd

def estimate_mu_sigma(returns: pd.DataFrame, ann: int = 252):
    mu = returns.mean().values * ann
    Sigma = returns.cov().values * ann
    return mu, Sigma

def port_mu_sigma(w: np.ndarray, mu: np.ndarray, Sigma: np.ndarray):
    mu_p = float(w @ mu)
    sig_p = float(np.sqrt(w @ Sigma @ w))
    return mu_p, sig_p
```

that is just the minimum plumbing. on one side, you extract mean and covariance. on the other, you take a weight vector and read what it is worth in the return / risk space.

then, to build the efficient frontier numerically, you fix a grid of target returns $\bar{\mu}$, and for each point on the grid you solve "minimum variance under constraints."

```python
import cvxpy as cp

def efficient_frontier(mu, Sigma, mu_grid, long_only=False, w_max=None):
    n = len(mu)
    w = cp.Variable(n)
    risk = cp.quad_form(w, Sigma)

    cons_base = [cp.sum(w) == 1]
    if long_only:
        cons_base += [w >= 0]
    if w_max is not None:
        cons_base += [w <= w_max]

    sigs, mus, weights = [], [], []
    for mu_bar in mu_grid:
        cons = cons_base + [w @ mu == mu_bar]
        prob = cp.Problem(cp.Minimize(risk), cons)
        prob.solve(solver=cp.OSQP, verbose=False)

        if w.value is None:
            sigs.append(np.nan)
            mus.append(mu_bar)
            weights.append(None)
            continue

        wv = np.array(w.value).ravel()
        mu_p, sig_p = port_mu_sigma(wv, mu, Sigma)
        sigs.append(sig_p)
        mus.append(mu_p)
        weights.append(wv)

    return np.array(sigs), np.array(mus), weights
```

this block does exactly what the definition says. nothing more. nothing less. for each target return, you ask: what is the smallest variance possible.

and then, for the tangency portfolio, you have two clean routes.

the first one is the closed-form route.

```python
def tangency_portfolio_closed_form(mu, Sigma, r_f):
    n = len(mu)
    mu_ex = mu - r_f * np.ones(n)
    w_raw = np.linalg.solve(Sigma, mu_ex)
    w = w_raw / np.sum(w_raw)
    mu_T, sig_T = port_mu_sigma(w, mu, Sigma)
    S_T = (mu_T - r_f) / sig_T
    return w, mu_T, sig_T, S_T
```

the idea is simple

you take the direction

$$
\Sigma^{-1}\mu_{ex}
$$

then renormalize it for a budget-1 display. then you read its return, its risk, and therefore its slope.

the second route is the numerical one. useful when you put constraints back in like long-only or caps. and here, the conceptual point has to stay very clean: you fix one single gauge.

```python
def tangency_portfolio_qp(mu, Sigma, r_f, long_only=False, w_max=None):
    n = len(mu)
    mu_ex = mu - r_f * np.ones(n)

    w = cp.Variable(n)
    risk = cp.quad_form(w, Sigma)

    # one single gauge: excess return fixed to 1
    cons = [w @ mu_ex == 1]
    if long_only:
        cons += [w >= 0]
    if w_max is not None:
        cons += [w <= w_max]

    prob = cp.Problem(cp.Minimize(risk), cons)
    prob.solve(solver=cp.OSQP, verbose=False)
    if w.value is None:
        return None, np.nan, np.nan, np.nan

    w_raw = np.array(w.value).ravel()
    w_disp = w_raw / np.sum(w_raw)  # optional: budget-1 display

    mu_T, sig_T = port_mu_sigma(w_disp, mu, Sigma)
    S_T = (mu_T - r_f) / sig_T
    return w_disp, mu_T, sig_T, S_T
```

and the CAL is then rebuilt very simply

$$
\mu(\sigma) = r_f + S_T\sigma
$$

and what has to stay in your head here is that the tangency portfolio is not "a magical set of weights." it is a risky direction. leverage tells you how much you put on it, and how much you leave on the risk-free asset. if you mix up the two layers of the problem, you create incoherent constraints and lose the geometric meaning.

to close the lesson properly, a few simple checks matter, but not as decoration.

if $\Sigma$ is not symmetric positive semidefinite, then you are not optimizing a clean object. you are optimizing a numerical illusion.

if the budget constraint does not actually close at

$$
\mathbf{1}^\top w = 1
$$

your portfolio does not exist under the stated definition.

if you switch to long-only, the frontier must fold inward. if it does not move at all, then either your constraints are not binding, or your solver is talking nonsense.

if you compute the unconstrained tangency portfolio, it must be collinear with

$$
\Sigma^{-1}\mu_{ex}
$$

if it is not, you broke scale invariance somewhere.

and above all, the real production check is this one: rebuild $\mu$ and $\Sigma$ over several windows. if the weights swing all over the place, it is not necessarily "the market changing." very often, it is the optimizer violently amplifying the input error, especially through $\mu$.

and that is the most important point if you want to put Markowitz back in its proper place.

Markowitz is a useful block. a very useful one. it gives you a clean geometry of the return / risk trade-off in a world summarized by $(\mu, \Sigma)$. but that world assumes something heavy: that the regime remains readable, that covariance remains exploitable, that the structure is not reconfiguring itself underneath your feet.

as soon as constraint starts propagating, as soon as correlations lock, as soon as the regime stops being "a stable cloud" and becomes a stressed mechanism, the effective geometry changes.

so the right move is not to throw Markowitz away. the right move is to stop treating it as if it were the system itself.

it is a block. not the world.

and that is exactly why the next logical step is not "more mean-variance." the next logical step is the question of how that world deforms when the parameters themselves become unstable.
