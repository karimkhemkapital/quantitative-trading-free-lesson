def gbm_ln_params(S0, mu, sigma, T):
    m = np.log(S0) + (mu - 0.5 * sigma**2) * T
    v = sigma**2 * T
    return m, v

def gbm_ST_moments(S0, mu, sigma, T):
    mean = S0 * np.exp(mu * T)
    var = (S0**2) * np.exp(2 * mu * T) * (np.exp(sigma**2 * T) - 1.0)
    return mean, var

def lognormal_pdf(s, m, v):
    s = np.asarray(s)
    pdf = np.zeros_like(s, dtype=float)
    mask = s > 0
    pdf[mask] = (1.0 / (s[mask] * np.sqrt(2*np.pi*v))) * np.exp(
        -(np.log(s[mask]) - m)**2 / (2*v)
    )
    return pdf

def simulate_gbm_paths(S0, mu, sigma, T, nsteps, N, seed=42):
    rng = np.random.default_rng(seed)
    dt = T / nsteps
    Z = rng.standard_normal((N, nsteps))
    increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    S = np.empty((N, nsteps + 1), dtype=float)
    S[:, 0] = S0
    S[:, 1:] = S0 * np.exp(np.cumsum(increments, axis=1))
    return S

S0 = 100.0
mu = 0.08
sigma = 0.02
T = 1.0
nsteps = 252

mT, vT = gbm_ln_params(S0, mu, sigma, T)
mean_th, var_th = gbm_ST_moments(S0, mu, sigma, T)

Ns = [1_000, 10_000, 100_000]
for N in Ns:
    S = simulate_gbm_paths(S0, mu, sigma, T, nsteps, N, seed=42)
    ST = S[:, -1]
    mean_emp = ST.mean()
    var_emp = ST.var(ddof=1)
