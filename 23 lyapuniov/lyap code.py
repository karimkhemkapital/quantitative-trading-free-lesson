import numpy as np

def compute_lyapunov_exponent(signal: np.ndarray, delay: int = 1, dimension: int = 3,
                              eps: float = 1e-6) -> float:
    N = len(signal)
    M = N - (dimension - 1) * delay
    if M <= 1:
        return np.nan

    X = np.array([signal[i:i + M] for i in range(0, dimension * delay, delay)]).T

    dists = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=-1)
    np.fill_diagonal(dists, np.inf)
    nearest = np.argmin(dists, axis=1)

    diverge = []
    for i in range(M - 1):
        j = nearest[i]
        d0 = np.linalg.norm(X[i] - X[j]) + eps
        d1 = np.linalg.norm(X[i + 1] - X[j + 1]) + eps
        log_div = np.log(d1 / d0)
        diverge.append(log_div)

    return float(np.mean(diverge))

dists = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=-1)
np.fill_diagonal(dists, np.inf)
nearest = np.argmin(dists, axis=1)

log_div = np.log(d1 / d0)

return float(np.mean(diverge))
