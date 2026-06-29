drift = (r - q - lam * kappa_J - 0.5 * sigma * sigma) * dt

logS = logS + drift + vol_term * Z + lnJ_sum
