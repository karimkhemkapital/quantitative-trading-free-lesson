Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Hysteresis And Path Dependence

we just saw that risk is not something you read as a level, but as a dynamic. a flow circulates, deforms, gets blocked, saturates. and above all, a system can return to "normal" on the surface while still remaining marked underneath. that is exactly where classical metrics get trapped: they look at the level, not the trace. they look at amplitude, not constraint.

so here, the move is simple. three building blocks, but the right ones. entropy for readability. hurst for memory. lyapunov for the propagation speed of that memory. and at the end, not a prediction, not a scenario, not a "signal" in the naive sense. just a regime state.

the first block is Shannon. the question is simple: does the market's message remain structured, or does it become disorganized to the point of losing readability.

the formula is

$$
H = -\sum_i p_i \log p_i
$$

if a few states dominate, the signal keeps a structure. if everything becomes uniform, nothing stands out anymore, so readability collapses. and this matters to say properly.

it does not measure "how much it moves." it measures whether what is moving still means something.

```python
import numpy as np

def _shannon_entropy(x: np.ndarray, bins: int = 30, normalize: bool = True) -> float:
    x = np.asarray(x, dtype=float)
    if np.allclose(np.std(x), 0):
        x = x + 1e-12 * np.random.randn(*x.shape)  # avoid zero variance
    counts, _ = np.histogram(x, bins=bins)
    p = counts / counts.sum()
    p = p[p > 0]  # avoid log(0)
    H = -np.sum(p * np.log2(p))
    if not normalize:
        return float(H)
    Hmax = np.log2(len(counts))
    return float(H / Hmax) if Hmax > 0 else np.nan
```

this block takes a series, splits it into bins, turns the frequencies into probabilities, then computes Shannon entropy. the normalization brings the score back between 0 and 1.

close to 0, the signal remains structured.

close to 1, it becomes disorganized.

the second block is Hurst. here, the subject is no longer readability. the subject is the trace. did the shock just pass through the system, or does it leave an active memory behind. that is exactly where risk becomes conditional, because we are no longer looking at noise around a center. we are looking at a marked system, where the path matters.

```python
def _hurst_exponent_rs(x: np.ndarray, min_window: int = 16) -> float:
    x = np.asarray(x, dtype=float)
    x = x - np.mean(x)
    N = len(x)
    max_window = N // 2
    sizes = np.floor(
        np.logspace(np.log10(min_window), np.log10(max_window), num=10)
    ).astype(int)

    RS = []
    for w in sizes:
        if w < 2:
            continue
        n_seg = N // w
        rs_vals = []
        for i in range(n_seg):
            seg = x[i*w:(i+1)*w]
            Y = np.cumsum(seg - np.mean(seg))
            R = np.max(Y) - np.min(Y)
            S = np.std(seg)
            if S > 0:
                rs_vals.append(R / S)
        if rs_vals:
            RS.append((w, np.mean(rs_vals)))

    if not RS:
        return np.nan
    w_arr, rs_arr = zip(*RS)
    H, _ = np.polyfit(np.log(w_arr), np.log(rs_arr), 1)
    return float(H)
```

this block estimates the Hurst exponent through the \(R/S\) ratio. the reading stays clean. close to 0.5, weak long memory. above that, persistence: the past keeps weighing on the present. so the system keeps a trace. and that trace is exactly what makes a shock not simply "pass." it changes the state of the regime.

the third block is Lyapunov. here, the subject is no longer "is there a trace?" the subject becomes: how fast does a small perturbation propagate through the system. in other words, do two states that start very close remain close, or do they separate fast? that is exactly the propagation speed of memory.

the basic form is

$$
|\delta X_t| \approx |\delta X_0|e^{\lambda t}
$$

if \(\lambda>0\), a small initial difference diverges fast: the perturbation propagates and amplifies.

if \(\lambda \approx 0\), the system stays neutral.

if \(\lambda<0\), there is contraction instead, so dissipation.

on a market series, the estimate remains numerical and local. so the point here is not to output "the true exponent of the world," but a propagation proxy.

```python
def _lyapunov_exponent(x: np.ndarray,
                       emb_dim: int = 3,
                       lag: int = 1,
                       horizon: int = 10,
                       min_separation: int = 20) -> float:
    x = np.asarray(x, dtype=float)
    n = len(x) - (emb_dim - 1) * lag
    if n <= horizon + 2:
        return np.nan

    # state-space reconstruction
    X = np.column_stack([x[i:i+n] for i in range(0, emb_dim * lag, lag)])

    pairs = []
    for i in range(len(X) - horizon):
        d = np.linalg.norm(X - X[i], axis=1)
        d[i] = np.inf

        lo = max(0, i - min_separation)
        hi = min(len(X), i + min_separation + 1)
        d[lo:hi] = np.inf  # avoid trivial temporal neighbors

        j = np.argmin(d)
        if np.isfinite(d[j]) and j < len(X) - horizon:
            pairs.append((i, j))

    if len(pairs) < 5:
        return np.nan

    mean_log_div = []
    for k in range(horizon):
        vals = []
        for i, j in pairs:
            dist = np.linalg.norm(X[i + k] - X[j + k])
            if dist > 0:
                vals.append(np.log(dist))
        if vals:
            mean_log_div.append(np.mean(vals))
        else:
            mean_log_div.append(np.nan)

    mean_log_div = np.asarray(mean_log_div)
    t = np.arange(len(mean_log_div))
    mask = np.isfinite(mean_log_div)
    if mask.sum() < 3:
        return np.nan

    slope, _ = np.polyfit(t[mask], mean_log_div[mask], 1)
    return float(slope)
```

this block first reconstructs a small state space from the series. the idea is simple: instead of looking at an isolated point, we look at a local configuration of the system. then, for each state, a nearby neighbor is searched, but not a trivial neighbor stuck right next to it in time, otherwise we would be cheating with the immediate continuity of the series. once the pairs are found, their average separation is tracked over a few future steps. if that separation grows fast, the slope is positive, so Lyapunov rises. and that is where the reading becomes clear: the memory is not only present, it propagates fast.

and this is where the interesting part starts, because these three blocks do not have much value if they stay isolated. the whole point is to connect them.

```python
def detect_risk_factors(returns: np.ndarray,
                        bins: int = 30,
                        emb_dim: int = 3,
                        lag: int = 1,
                        horizon: int = 10) -> dict:
    H_ent = _shannon_entropy(returns, bins=bins, normalize=True)
    hurst = _hurst_exponent_rs(returns)
    lyap = _lyapunov_exponent(returns, emb_dim=emb_dim, lag=lag, horizon=horizon)

    risk_flag = "latent"
    if hurst > 0.5 and H_ent > 0.9 and lyap > 0:
        risk_flag = "structural_time_bomb"
    elif hurst > 0.5 and H_ent > 0.9:
        risk_flag = "chaotic_memory"
    elif lyap > 0:
        risk_flag = "propagating_instability"

    return {
        "entropy": H_ent,
        "hurst": hurst,
        "lyapunov": lyap,
        "risk_flag": risk_flag
    }
```

if Hurst is high, there is a trace.

if entropy is high, the signal becomes unreadable.

if Lyapunov is positive, the perturbation propagates fast.

and when all three show up together, we are no longer in a market that is just "agitated." we are in a system under constraint: active memory, information chaos, and rapid propagation of the perturbation. in other words, risk no longer needs to be announced. it is already inside the structure.

"latent" keeps the most sober idea: nothing has clearly tipped yet, but that does not mean risk is absent. it just means none of the three dimensions has crossed a strong enough threshold yet to signal a clear change of state.

"propagating_instability" says something else: the system is not necessarily unreadable yet, or loaded with long memory, but a small perturbation is transmitted fast. the propagation channel is already active.

"chaotic_memory" describes a dirtier state. the system keeps a trace, but inside an environment that has become unreadable. in other words, the past keeps weighing on the present, but inside an informational space that is blurring out. it is not simply noise, and it is not simply memory. it is memory inside noise.

and "structural_time_bomb" is the critical combination. persistent memory, high entropy, positive propagation. at that point, the system already carries the conditions for a rupture, even if price has not printed the final move yet. that is exactly the kind of state where the surface can still look "normal," while underneath the law of the system has already started changing.

and there, it reconnects cleanly with the previous thread. in the earlier lessons, the cut was already there: risk is not the level of the move, it is the moment when the system stops dissipating and starts propagating. here, that shift becomes measurable.

entropy tells whether the market remains readable.

hurst tells whether the shock leaves a trace.

lyapunov tells how fast that trace is transmitted and deployed.

and when all three deform together, this is no longer just noise. it is already a rupture mechanism being built in real time.
