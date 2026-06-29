Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# ARCH/GARCH: Variance Does Not Disappear, It Propagates

up to this point, we mostly worked with equilibrium objects: allocation, pricing, exposures, factors. but the moment you come back down to observed return series, you run into a much more brutal fact.

returns often look almost uncorrelated in level. their magnitude, on the other hand, is not.

you take a series \(R_t\). you compute the autocorrelations of \(R_t\). very often, you get a structure like

$$
Corr(R_t, R_{t-k}) \approx 0, \qquad Corr(R_t^2, R_{t-k}^2) > 0
$$

that means something very simple.

the sign of a move is hard to predict. but the intensity of the regime leaves a trace. a large shock is often followed by other large shocks. a calm phase is often followed by other calm phases. the market does not necessarily keep much memory in direction. it does keep memory in dispersion.

that is exactly what ARCH/GARCH writes down properly.

not an "average volatility" fixed once and for all. a conditional variance that moves through time and depends on what has already happened. in other words: the noise itself is heteroskedastic.

so we start with the minimal structure

$$
R_t = \mu_t + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t
$$

with

$$
E[z_t] = 0, \qquad Var(z_t) = 1, \qquad \sigma_t^2 = Var(\epsilon_t \mid \mathcal F_{t-1})
$$

\(\mathcal F_{t-1}\) is simply the information available up to time \(t-1\). so the key point is right there: variance at date \(t\) is no longer a fixed number. it becomes an internal state of the system.

ARCH starts from that idea in the most direct way possible. you say: today's variance depends on squared past shocks. if yesterday was violent, today has a good chance of staying tense. in an ARCH(q), you write

$$
\sigma_t^2 = \omega + \alpha_1\epsilon_{t-1}^2 + \alpha_2\epsilon_{t-2}^2 + \cdots + \alpha_q\epsilon_{t-q}^2
$$

with

$$
\omega > 0, \qquad \alpha_i \ge 0
$$

the mechanical reading is clean. \(\omega\) is the floor. the irreducible level of variance. the \(\alpha_i\) are the transmission coefficients from old shocks into present variance. the larger an \(\alpha_i\), the more strongly a past shock leaves an imprint.

but pure ARCH hits a limit quickly. to reproduce long persistence, it needs many lags. so we compress the memory. that is exactly where GARCH comes in.

in a GARCH(1,1), you write

$$
\sigma_t^2 = \omega + \alpha\epsilon_{t-1}^2 + \beta\sigma_{t-1}^2
$$

with

$$
\omega > 0, \qquad \alpha \ge 0, \qquad \beta \ge 0
$$

and at that point, the model becomes really readable.

the term

$$
\alpha\epsilon_{t-1}^2
$$

is reactivity. the term

$$
\beta\sigma_{t-1}^2
$$

is inertia. the memory of the previous tension state. if the system was already nervous, it does not become calm again in one candle just because you want it to stop.

so \(\alpha\) is reactivity, \(\beta\) is persistence and the sum \(\alpha+\beta\) is almost the whole story.

if \(\alpha+\beta\) is small, variance absorbs shocks quickly and then comes back down. the system dissipates fast.

if \(\alpha+\beta\) gets close to 1, tension stays attached for a long time. the shock is over, but its imprint remains in the structure.

and if you want the model to be covariance-stationary, you need to impose

$$
\alpha + \beta < 1
$$

in that case, the unconditional variance exists and is

$$
E[\sigma_t^2] = \frac{\omega}{1 - \alpha - \beta}
$$

that formula matters more than it first seems to. it says the average variance level is not just \(\omega\). it gets inflated by the whole persistence of the system. a small floor can produce a high average variance if the memory \(\alpha+\beta\) is strong.

so here, you really need to see the shift in the idea.

with homoskedastic noise, you are basically saying: the system takes hits, but every hit is drawn in the same dispersion climate.

with GARCH, you are saying something else. each hit modifies the climate itself. the system does not just take shocks. it keeps the trace of their intensity inside its variance state.

that is why the model fits volatility clustering so well. it is not trying to predict tomorrow's sign. it is trying to write the dispersion regime into which tomorrow will fall.

if you take a large shock at \(t-1\), meaning a large

$$
\epsilon_{t-1}^2
$$

then

$$
\sigma_t^2
$$

goes up. and because it enters the next equation through

$$
\beta\sigma_{t-1}^2
$$

you generate propagation. not infinite propagation if \(\alpha+\beta<1\) but a slow decay. a tail.

that is exactly what we observe in markets: violence does not disappear cleanly. it reverberates.

on the estimation side, the logic stays clean. you assume a law for \(z_t\), often Gaussian to start with, sometimes Student-t to handle heavier tails, then you maximize the conditional log-likelihood. in the Gaussian case,

$$
\ell(\theta) = -\frac{1}{2}\sum_{t=1}^{T}\left[\log(2\pi) + \log(\sigma_t^2) + \frac{\epsilon_t^2}{\sigma_t^2}\right]
$$

with \(\theta=(\omega,\alpha,\beta,\mu)\) or an enriched version if you put a dynamics on the mean.

the structure of that likelihood matters. a GARCH model is not just trying to make residuals small. it has to explain when variance should be high and when it should fall back. if it misses that latent state, the penalty shows up immediately in the term

$$
\log(\sigma_t^2)
$$

and in the ratio

$$
\frac{\epsilon_t^2}{\sigma_t^2}
$$

in practice, there are four checks that matter.

the first: \(\omega>0\), \(\alpha\ge0\), \(\beta\ge0\). otherwise your conditional variance can become absurd.

the second: \(\alpha+\beta<1\) if you want proper stationarity.

the third: once the model is estimated, the standardized residuals

$$
z_t = \frac{\epsilon_t}{\sigma_t}
$$

should no longer keep autocorrelation in their squares. otherwise, you have not captured all the heteroskedasticity.

the fourth: if the tails remain too heavy under normality, you often switch to a Student law. otherwise, you underprice the remaining violence.

and here, the link with everything we set up before becomes clean.

ARCH/GARCH does not give you "risk" in the total sense. it gives you a local state of tension. an estimate of conditional dispersion at time \(t\). so a much more useful piece of information for sizing, leverage, margin control, short-horizon VaR, or scenario calibration.

for example, if you want to build a one-day VaR under conditional normality, you write

$$
VaR_{\alpha,t+1} = -\left(\mu_{t+1} + q_\alpha\sigma_{t+1}\right)
$$

where \(q_\alpha\) is the quantile of the chosen law for \(z_t\). if you move to Student-t, you just replace the quantile.

that is not "the truth about the future." it is a conditional slice of risk given the variance regime estimated now.

and that is why GARCH became so successful: it captures a very robust stylized fact with a short mechanism. no need to invent a whole story. the model just says: shocks modify variance, and variance has inertia.

on the Python side, the logic is exactly the same. you take a return series, estimate a simple mean or set it to zero depending on the framework, then let the model fit \(\omega,\alpha,\beta\)

```python
import numpy as np
import pandas as pd
from arch import arch_model

def fit_garch_11(returns: pd.Series, mean="Constant", dist="t"):
    r = pd.Series(returns).dropna().astype(float)
    am = arch_model(r, mean=mean, vol="GARCH", p=1, q=1, dist=dist)
    res = am.fit(disp="off")
    out = {
        "params": res.params,
        "cond_vol": res.conditional_volatility,
        "std_resid": res.std_resid,
        "loglik": res.loglikelihood,
    }
    return res, out

def forecast_next_vol(res, horizon=1):
    fc = res.forecast(horizon=horizon)
    var_next = fc.variance.iloc[-1, 0]
    return float(np.sqrt(var_next))
```

the reading of the fit is direct. if \(\alpha\) is high, the market reacts strongly to recent shocks. if \(\beta\) is high, it keeps the memory of its tension state for a long time. if \(\alpha+\beta\) sticks close to 1, you are in a very persistent variance regime.

then you run the useful check: look at the squares of the standardized residuals. if they still keep structure, your model is too poor.

```python
def acf_lag1(x):
    x = np.asarray(pd.Series(x).dropna(), float)
    if len(x) < 2:
        return np.nan
    x0 = x[:-1] - x[:-1].mean()
    x1 = x[1:] - x[1:].mean()
    den = np.sqrt((x0**2).sum() * (x1**2).sum())
    return float((x0 @ x1) / den) if den > 0 else np.nan
```

the simple check is to compare the autocorrelation of squared returns before and after standardization. before, it often exists. after a good GARCH, it should shrink sharply.

in the end, the lesson fits in one line: a market shock does not just modify price. it also modifies the dispersion regime in which future prices will move.

and that is exactly why a market can look calm again on the surface while conditional variance is still loaded underneath. what GARCH gives you is not a direction. it is the system's tension state at the moment you look at it.
