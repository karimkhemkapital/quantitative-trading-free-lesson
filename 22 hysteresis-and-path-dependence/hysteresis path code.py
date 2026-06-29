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
