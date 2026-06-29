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

def acf_lag1(x):
    x = np.asarray(pd.Series(x).dropna(), float)
    if len(x) < 2:
        return np.nan
    x0 = x[:-1] - x[:-1].mean()
    x1 = x[1:] - x[1:].mean()
    den = np.sqrt((x0**2).sum() * (x1**2).sum())
    return float((x0 @ x1) / den) if den > 0 else np.nan
