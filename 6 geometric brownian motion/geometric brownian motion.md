Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-6-geometric-brownian-motion

The key point is that the market moves randomly, but not "anyhow".

When I say "stochastic process", I mean something simple: I know I don't know the exact path, but I can describe the family of possible paths.

Like the blue ball in the Insta reels... it can go in every direction, but it stays inside a frame, with rules of motion.

Price is the same: you can't say where it will be tomorrow, but you can say what the space looks like where it is statistically allowed to wander.

And to see that frame, you don't need big theories: you simulate. Very easily with Python. And here we're going to see general and customizable implementations that you can plug into pipelines.

We can start with a small Python code that simulates days at \(+0.50\) or \(-0.50\).

Just set step and the number of paths, and you'll see the tunnel draw itself.

```python
import numpy as np
import matplotlib.pyplot as plt

seed = 42
T = 1.0
nsteps = 252
dt = T / nsteps
n_paths = 80

step = 0.50    # +0.50 / -0.50
p_up = 0.50   # 50/50

rng = np.random.default_rng(seed)

# +step or -step
signs = np.where(rng.random((n_paths, nsteps)) < p_up, 1.0, -1.0)
inc = step * signs

X = np.cumsum(inc, axis=1)
X = np.hstack([np.zeros((n_paths, 1)), X])

t = np.linspace(0.0, T, nsteps + 1)

plt.figure(figsize=(12, 5))
for i in range(n_paths):
    plt.plot(t, X[i], alpha=0.35, linewidth=0.9)

plt.title(f"Random walk with fixed jumps: +/-{step}")
plt.xlabel("t")
plt.ylabel("level (additive)")
plt.tight_layout()
plt.show()
```

That's the base: an unpredictable movement, but when you look at the ensemble, you clearly see there's a "typical" zone where most paths remain.

And now we get to the real subject: volatility.

Volatility is a measure of "how much it moves", but not in a directional sense. It's not "it's going up" or "it's going down". It's just: what is the typical size of variations, up or down.

The problem is that your \(+0.50/-0.50\) model is too rigid, while in real life moves aren't constant. Some days it barely moves, other days it hits hard.

So instead of a fixed jump, you move to a model where the move itself is random: each day you draw a shock from a centered distribution, and you scale it by a parameter.

That parameter that sets the shock scale is volatility.

Concretely, you can keep the exact same simulation structure, but replace \(+0.50\) with a centered Gaussian draw, and control its width with sigma.

Then you'll see the tunnel becomes a "continuous" tunnel, and you directly control how fast it opens.

```python
import numpy as np
import matplotlib.pyplot as plt

seed = 42
T = 1.0
nsteps = 252
dt = T / nsteps
n_paths = 80

sigma = 0.50    # volatility (shock scale per step)

rng = np.random.default_rng(seed)

# centered shocks N(0, sigma^2)
inc = sigma * rng.standard_normal((n_paths, nsteps))

X = np.cumsum(inc, axis=1)
X = np.hstack([np.zeros((n_paths, 1)), X])

t = np.linspace(0.0, T, nsteps + 1)

plt.figure(figsize=(12, 5))
for i in range(n_paths):
    plt.plot(t, X[i], alpha=0.35, linewidth=0.9)

plt.title(f"Gaussian random walk: inc ~ N(0, {sigma}^2)")
plt.xlabel("t")
plt.ylabel("level (additive)")
plt.tight_layout()
plt.show()
```

The role of vol, with zero complicated formulas, is literally the "tunnel opening" button. You set sigma higher, it spreads faster. You set it lower, it stays tight.

But careful: don't believe this system is stable. It isn't. The market changes regime. It compresses, it clusters, it jumps, it grows fat tails, it becomes asymmetric.

So if you use a constant vol in your model, it's an approximation. Useful, but limited. As long as the world looks like your assumption, your noise is "quantifiable". When the world changes, your tunnel becomes wrong.

To make that concrete, we build a GBM "tunnel" with a constant model vol, then we simulate a "real" path where vol changes halfway and we add a jump. The idea is simple: if the path exits the tunnel, that's a regime-break signal, not a directional signal.

```python
import numpy as np
import matplotlib.pyplot as plt


class GBMTunnel:
    def __init__(self, S0: float, mu: float, sigma_model: float, dt: float):
        self.S0 = float(S0)
        self.mu = float(mu)
        self.sigma_model = float(sigma_model)
        self.dt = float(dt)

    def simulate_path(self, n_steps: int, sigma_true=None, jumps=None, seed: int = 42):
        rng = np.random.default_rng(seed)

        if sigma_true is None:
            sigma_true_used = np.full(n_steps, self.sigma_model, dtype=float)
        else:
            sigma_true_used = np.asarray(sigma_true, dtype=float)
            if sigma_true_used.shape[0] != n_steps:
                raise ValueError("sigma_true must have length n_steps")

        Z = rng.standard_normal(n_steps)
        drift = (self.mu - 0.5 * sigma_true_used**2) * self.dt
        diff = sigma_true_used * np.sqrt(self.dt) * Z
        lnret = drift + diff

        if jumps:
            for t, j in jumps.items():
                if 0 <= t < n_steps:
                    lnret[t] += float(j)

        logS = np.log(self.S0) + np.cumsum(lnret)
        S = np.exp(logS)
        return S, lnret, sigma_true_used

    def tunnel_bounds(self, n_steps: int, z: float = 2.58):
        t = np.arange(1, n_steps + 1) * self.dt
        mean = np.log(self.S0) + (self.mu - 0.5 * self.sigma_model**2) * t
        std = self.sigma_model * np.sqrt(t)
        lower = np.exp(mean - z * std)
        upper = np.exp(mean + z * std)
        return lower, upper


# settings
S0 = 100.0
mu = 0.00
sigma_model = 0.20
T = 1.0
n_steps = 252
dt = T / n_steps
z = 2.58
seed = 42

tunnel = GBMTunnel(S0=S0, mu=mu, sigma_model=sigma_model, dt=dt)

# "true" vol that changes (regime)
sigma_true = np.full(n_steps, 0.15)
sigma_true[120:] = 0.35

# jump (one-off shock)
jumps = {170: -0.12}

S, lnret, sigma_used = tunnel.simulate_path(n_steps=n_steps, sigma_true=sigma_true,
                                            jumps=jumps, seed=seed)
lower, upper = tunnel.tunnel_bounds(n_steps=n_steps, z=z)
time = np.arange(1, n_steps + 1) * dt

plt.figure(figsize=(12, 5))
plt.plot(time, S, linewidth=2.0, label="real path (sigma_true + jump)")
plt.plot(time, lower, linewidth=2.0, label="lower bound (tunnel)")
plt.plot(time, upper, linewidth=2.0, label="upper bound (tunnel)")
plt.title("Path vs tunnel (exit = regime break)")
plt.xlabel("t")
plt.ylabel("S_t")
plt.legend()
plt.tight_layout()
plt.show()
```

Here, as long as true vol is compatible with model vol, you stay "inside the world". When vol increases or a jump hits, you can exit.

Now, if you don't want to stay blind, you add sensors.

The first thermometer is rolling realized volatility. It measures "how much it moves" in a local window. Then you compare it to your model vol to see if you're overloaded.

```python
def realized_vol(log_returns: np.ndarray, window: int, dt: float) -> np.ndarray:
    rv = np.full_like(log_returns, np.nan, dtype=float)
    for i in range(window - 1, len(log_returns)):
        w = log_returns[i - window + 1:i + 1]
        rv[i] = np.sqrt(np.var(w, ddof=1) / dt)
    return rv


window = 20
rv = realized_vol(lnret, window=window, dt=dt)
ratio = rv / sigma_model

plt.figure(figsize=(12, 4))
plt.plot(time, ratio, linewidth=2.0)
plt.axhline(1.0, linewidth=2.0)
plt.title("RV / sigma_model (if > 1: tunnel too tight)")
plt.xlabel("t")
plt.ylabel("RV / sigma_model")
plt.tight_layout()
plt.show()
```

Second thermometer: KL divergence between two consecutive windows.

Here you're not just looking at variance, you're looking at whether the distribution shape changes: tails, asymmetry, outliers. If KL rises, it's a signal the shock structure is no longer the same.

```python
def _kl_from_counts(ca: np.ndarray, cb: np.ndarray, eps: float = 1e-12) -> float:
    pa = ca.astype(float) + eps
    pb = cb.astype(float) + eps
    pa /= pa.sum()
    pb /= pb.sum()
    return float(np.sum(pa * np.log(pa / pb)))


def rolling_kl(x: np.ndarray, window: int, step: int = 1, bins: int = 50) -> np.ndarray:
    n = len(x)
    out = np.full(n, np.nan, dtype=float)
    for end in range(2 * window, n + 1, step):
        a = x[end - 2 * window : end - window]
        b = x[end - window : end]
        lo = min(a.min(), b.min())
        hi = max(a.max(), b.max())
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            continue
        edges = np.linspace(lo, hi, bins + 1)
        ca, _ = np.histogram(a, bins=edges)
        cb, _ = np.histogram(b, bins=edges)
        out[end - 1] = _kl_from_counts(ca, cb)
    return out


kl = rolling_kl(lnret, window=30, bins=40)

plt.figure(figsize=(12, 4))
plt.plot(time, kl, linewidth=2.0)
plt.title("rolling KL (if it rises: distribution is mutating)")
plt.xlabel("t")
plt.ylabel("KL")
plt.tight_layout()
plt.show()
```

Third thermometer: CUSUM on variance, to detect transitions, clusters, compressions from a baseline. When it crosses a threshold, you get a "variance transition" alert.

```python
def cusum_variance(r2: np.ndarray, baseline: float, h: float):
    g_pos = np.zeros_like(r2, dtype=float)
    g_neg = np.zeros_like(r2, dtype=float)
    alarms = np.zeros_like(r2, dtype=bool)

    for i in range(1, len(r2)):
        x = r2[i] - baseline
        g_pos[i] = max(0.0, g_pos[i - 1] + x)
        g_neg[i] = min(0.0, g_neg[i - 1] + x)

        if g_pos[i] > h or abs(g_neg[i]) > h:
            alarms[i] = True
            g_pos[i] = 0.0
            g_neg[i] = 0.0
    return g_pos, g_neg, alarms


r2 = lnret**2
baseline = np.nanmean(r2[:80])
h = 8 * baseline

g_pos, g_neg, alarms = cusum_variance(r2, baseline=baseline, h=h)

plt.figure(figsize=(12, 4))
plt.plot(time, g_pos, linewidth=2.0, label="CUSUM+ (variance up)")
plt.plot(time, g_neg, linewidth=2.0, label="CUSUM- (variance down)")
plt.scatter(time[alarms], g_pos[alarms], s=25, label="alarm", zorder=3)
plt.title("CUSUM variance (transitions / clusters / compressions)")
plt.xlabel("t")
plt.ylabel("accumulation")
plt.legend()
plt.tight_layout()
plt.show()
```

Now the chain is clear: the tunnel, vol as its width, the fact the market changes regime, and objective methods to detect when the world exits your frame.

And only then the transition to greeks becomes logical, because greeks are the exact same logic applied to the price of an option.

You can see greeks as gauges plugged into the same machine:

delta: how your option reacts when the underlying moves inside the tunnel.

gamma: how fast delta changes when it moves.

theta: what time takes from you / gives you while price evolves.

vega: direct sensitivity to the tunnel width (vol).

So if you haven't understood "vol = tunnel width", greeks will look like words. If you have, greeks become just sensors: you touch the tunnel, you immediately see what it does to your position.
