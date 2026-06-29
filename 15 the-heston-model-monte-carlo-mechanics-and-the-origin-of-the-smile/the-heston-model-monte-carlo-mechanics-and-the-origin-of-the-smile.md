Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# The Heston Model Monte Carlo Mechanics And The Origin Of The Smile

now, the important point is not to read this code as "one way among others to run a Monte Carlo." here, every line exists because a precise part of the Heston model has to survive discretization.

the first block, `bs_call`, is not there to reprice Heston. it is there to make the reverse bridge: you simulate under Heston, you get a call price, then you go back through Black-Scholes to extract an implied vol. in other words, Heston gives you a price, and Black-Scholes is only used as a thermometer to re-express that price in surface language. without that, you do not "see" the smile. you only have a list of prices.

then `implied_vol_call` does exactly what it is supposed to do: a robust inversion by bisection. the point is not to be fast. the point is to be stable. the price of a Black-Scholes call is increasing in \(\sigma\), so as long as your input price is reasonable, bisection gives you a clean implied vol without making things up.

the heart of the subject is obviously `heston_mc_call`. and there, the first thing to look at is how you build the two correlated Brownian motions. in the model, you have

$$
dW_t^S dW_t^v = \rho\,dt.
$$

once you discretize, that means you cannot draw two independent Gaussians and hope to "recover" the correlation by magic. you have to build it. that is exactly what this does

```python
dW_S = sqdt * Z1
dW_v = sqdt * (rho * Z1 + sqrt(1.0 - rho * rho) * Z2)
```

if \(Z1\) and \(Z2\) are independent standard normals, then \(dW_S\) and \(dW_v\) do have the right correlation \(\rho\). and that is where the leverage effect really enters the simulation. if \(\rho < 0\), a downward shock on spot tends to come with an upward shock on variance. that is not a market comment. it is already coded into the mechanics of the Brownian increments.

then you have the most important line from a numerical point of view

```python
v_eff = np.maximum(v, 0.0)
```

that is the minimal guardrail. in the continuous world, the CIR dynamics carries a positivity structure. on a machine, if you use naive Euler, nothing prevents \(v\) from becoming negative because of discretized noise. and the moment \(v < 0\), you no longer have a defined \(v\). so the pipeline does not "degrade" gently. it breaks. `v_eff` simply says: for the drift and the noise, I use the positive part. that is the logic of full truncation.

the variance update

```python
v = v + kappa * (theta - v_eff) * dt + xi * np.sqrt(v_eff) * dW_v
v = np.maximum(v, 0.0)
```

has to be read exactly like the continuous equation, but in discrete form. the term \(\kappa(\theta-v_t)dt\) pulls the variance back toward \(\theta\).

$$
\xi \sqrt{v_t}\,dW_t^v
$$

the term shakes it. and the final `np.maximum(v, 0.0)` prevents one violent step from sending you into absurd territory. that is not "the mathematical truth of the model." it is a clean numerical repair to keep the engine alive.

the spot update

```python
S = S * np.exp((r - q - 0.5 * v_eff) * dt + np.sqrt(v_eff) * dW_S)
```

uses the log-Euler structure. the only difference from Black-Scholes is that here the instantaneous variance is no longer constant. it changes along the path. at each step, spot moves forward with the current variance \(v_{\mathrm{eff}}\). so if variance explodes after a shock, the following spot moves mechanically become more nervous. that is exactly how the smile is born in the simulation: not because it was drawn, but because volatility itself has its own life.

when you get to the end of the Monte Carlo, you discount the payoff, take the mean, and also recover a standard error estimator

```python
disc_payoff = np.exp(-r * T) * payoff
price = disc_payoff.mean()
se = disc_payoff.std(ddof=1) / sqrt(npaths)
```

that also has to stay clean in your head: the MC price is not "the price." it is a noisy estimator of the price. so when you compare two smiles or two parameter sets, if you do not keep at least some control over `se`, you can easily mistake simulation noise for an economic effect.

then the ATM block and the `K_list` block do exactly the most useful test at the start: you price several strikes at fixed maturity, then go back to implied vol to read the smile. that is where the model really starts to speak. not when you stare at the parameters in isolation. not when you look at the SDE written on paper. the model starts to speak at the moment when, from the same dynamics, you extract different implied vols across strike.

and that is where the comparison with local vol becomes clean. under local vol, you start from a surface and reconstruct a diffusion that matches it exactly at \(t=0\). under Heston, you start from a parametric diffusion and look at what surface it produces. so it is not the same philosophy at all.

in one case, the surface is the input and the dynamics is the output.

in the other, the dynamics is the input and the surface is the output.

and that changes everything. with local vol, you get exact vanilla fit, but a very constrained smile dynamics. with Heston, you do not have enough degrees of freedom to match the entire surface perfectly, but you get a volatility dynamics that already has economic content: mean reversion, vol-of-vol, leverage effect.

that is why the parameters read like a grammar of the surface.

if you increase \(v_0\), you do not "raise vol everywhere" in a uniform way. you mainly raise the short-end level, because the process starts higher.

if you increase \(\theta\), you mainly lift the long-end level, because it is the mean-reversion target of the variance.

if you increase \(\kappa\), you do not create smile. you accelerate the speed at which the market "forgets" \(v_0\) and comes back toward \(\theta\).

if you increase \(\xi\), you inject more randomness into the variance itself. so the terminal distribution picks up more convexity, and the smile deepens.

if you make \(\rho\) more negative, you reinforce asymmetry: spot down moves and variance up moves answer each other more strongly, so the left side becomes more expensive and the skew steepens.

in other words, a Heston surface does not come from interpolation. it comes from a mechanism. and that is exactly why even an imperfect fit can be more useful than a perfect fit, once you start looking at payoffs that depend on the way vol moves along the path.

there is also a simple check you can keep so you do not get trapped by your own code. you recalled that

$$
E[v_t \mid v_0] = \theta + (v_0-\theta)e^{-\kappa t}.
$$

that is not just a pretty formula. it is a test. if you simulate many paths of \(v_t\) and their average does not roughly look like that, it is not Heston that is at fault. it is your scheme.

same thing if you make \(\xi\) very small. variance becomes almost deterministic. at that point, the smile should collapse. if it does not collapse in your code, you did not discover some deep phenomenon. you just have a simulation or implied-vol inversion problem.

same logic for \(\rho\). if you move from \(\rho=-0.8\) to \(\rho=-0.1\), the slope of the skew should flatten significantly. if almost nothing changes, you need to look at either your MC noise, your strike grid, or the number of paths.

and that is where the real practical issue appears: in production, Heston is not calibrated like this. Monte Carlo is useful to understand, to sanity-check, to price exotics, to feel the parameters. but if you want to fit a vanilla surface quickly and cleanly, you are not going to launch fifty thousand paths for each strike and maturity at every iteration of an optimization. that would be far too slow. that is exactly why the characteristic function changes everything: European pricing is reduced to one-dimensional integrals, so pricing becomes fast enough for calibration.

but pedagogically, starting from Monte Carlo has real value. because until you have seen that the smile comes out of a variance that moves with its own noise source, the semi-closed Heston formula can quickly become a purely technical object. whereas here you see the mechanism before you see the numerical acceleration.

if you want to push the experiment without breaking the skeleton, the cleanest move is exactly what your text suggests: one parameter at a time, same seed, same strike grid, same maturity, and you only look at what changes. it matters to keep the seed fixed at the beginning, because otherwise part of what you think you are reading as a "parameter effect" is only different MC noise from one experiment to the next.

and when you read the outputs, you have to read them with discipline.

if Feller \(2\kappa\theta \ge \xi^2\) is violated, that does not mean "forbidden model." it means variance can hit zero and your simulation has to stay numerically clean.

$$
\sqrt{v_0}
$$

if ATM IV is close to \(\sqrt{v_0}\) at very short maturities, that is coherent.

if the list of implied vols on `K_list` goes down as \(K\) goes up for \(\rho < 0\), you are indeed reading an equity-like skew. if you increase \(\xi\) and the wings move farther away from ATM, you are indeed reading the vol-of-vol effect.

and if you extend maturity, you should see more and more of the role of \(\theta\) and \(\kappa\), not only that of \(v_0\).

so the lesson holds together very simply, under local vol, you imposed the surface and reconstructed a diffusion.

under Heston, you impose a two-factor diffusion spot plus variance and look at the surface it produces.

you lose the exact point-by-point fit.

you gain a smile dynamics.

and that shift is exactly what matters. because from the moment volatility itself becomes a state factor, the surface is no longer a static object that you glue back on. it becomes the visible projection of a system with two sources of risk.
