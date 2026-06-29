dW_S = sqdt * Z1
dW_v = sqdt * (rho * Z1 + sqrt(1.0 - rho * rho) * Z2)

v_eff = np.maximum(v, 0.0)

v = v + kappa * (theta - v_eff) * dt + xi * np.sqrt(v_eff) * dW_v
v = np.maximum(v, 0.0)

S = S * np.exp((r - q - 0.5 * v_eff) * dt + np.sqrt(v_eff) * dW_S)

disc_payoff = np.exp(-r * T) * payoff
price = disc_payoff.mean()
se = disc_payoff.std(ddof=1) / sqrt(npaths)
