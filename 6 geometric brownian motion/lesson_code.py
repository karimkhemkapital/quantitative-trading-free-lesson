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
