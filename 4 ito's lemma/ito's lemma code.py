dt = T / nsteps
mu_tilde = mu - 0.5 * sigma**2

print(f"mu_tilde (drift of ln S) = {mu_tilde:.6f}")

XT = np.log(ST)
mean_X_emp = XT.mean()
var_X_emp = XT.var(ddof=1)

mean_X_th = mT
var_X_th  = vT

X = np.log(S)
dX = X[:, 1:] - X[:, :-1]
mu_tilde_hat = dX.mean() / dt

print(f"E[X_T]   = {mean_X_emp:.6f}    (error = {mean_X_emp - mean_X_th:+.6e})")
print(f"Var[X_T] = {var_X_emp:.6f}    (error = {var_X_emp - var_X_th:+.6e})")
print(f"mu_tilde_hat = {mu_tilde_hat:.6f}    (error = {mu_tilde_hat - mu_tilde:+.6e})")
