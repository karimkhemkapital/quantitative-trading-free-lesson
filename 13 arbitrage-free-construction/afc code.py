import numpy as np
import numpy as np

def static_noarb_checks_discrete(K, C, tol=1e-10):
    K = np.asarray(K, dtype=float)
    C = np.asarray(C, dtype=float)

    order = np.argsort(K)
    K = K[order]
    C = C[order]

    # monotonicity: C decreasing in K
    mono_ok = np.all(np.diff(C) <= tol)

    # discrete convexity on non-uniform grid
    slopes = np.diff(C) / np.diff(K)   # expected <= 0
    convex_ok = np.all(np.diff(slopes) >= -tol)

    return {
        "mono_ok": bool(mono_ok),
        "convex_ok": bool(convex_ok),
        "min_slope": float(np.min(slopes)),
        "max_slope": float(np.max(slopes)),
        "min_slope_diff": float(np.min(np.diff(slopes))) if len(slopes) > 1 else np.nan,
    }

def calendar_check(price_fn, K_grid, T_grid, F_fn, DF_fn, tol=1e-10):
    out = []
    for K in K_grid:
        prices = [price_fn(K, T, F_fn(T), DF_fn(T)) for T in T_grid]
        ok = all(prices[i+1] >= prices[i] - tol for i in range(len(prices)-1))
        out.append({"K": float(K), "ok": bool(ok), "prices": prices})
    return out
