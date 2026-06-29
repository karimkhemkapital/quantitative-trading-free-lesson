Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Jump Diffusion Models

now, the important point is not to read this code as "just another Monte Carlo." here, each block exists because a precise piece of the jump-diffusion mechanics has to be kept clean. otherwise you can very quickly get prices that look plausible... but with the wrong dynamics under \(Q\).

the first block, `bs_call`, is not there to price the model in its place. it is there to rebuild the reverse path. the jump model gives you prices. then you go back through Black-Scholes to extract an implied vol and put those prices back into surface language. it is exactly the same logic as in the previous lesson with Heston: as long as you stay at the level of prices, you do not really "see" the shape produced by the model. you see it when you rewrite everything as \(\sigma_{\mathrm{impl}}(K,T)\).

`implied_vol_call` then does the simplest and safest possible job: inversion by bisection. the point is not to be fast. the point is to be stable. the price of a BS call is increasing in \(\sigma\), so if your price is coherent, bisection gives you back a clean implied vol. again, no magic here: just a robust inversion.

the real heart of the subject is `jd_mc_terminal`. that is where you write the jump-diffusion dynamics in discrete form, and you need to see that everything is already sitting inside this line

```python
drift = (r - q - lam * kappa_J - 0.5 * sigma * sigma) * dt
```

that is the line carrying the risk-neutral correction. if you forget the term \(-\lambda\kappa_J\), your process is no longer properly compensated under \(Q\). at that point, you can still produce paths, you can still produce payoffs, but your expectation of \(S_T\) will no longer match

$$
E_Q[S_T] = S_0 e^{(r-q)T}.
$$

and that is exactly why the martingale check at the end of the code is not cosmetic. if \(E[S_T]\) does not roughly match the target, the problem does not come from "the style of the smile." it comes from the compensated drift, which means the core of the model.

then, inside `jd_mc_terminal`, you evolve in log space

```python
logS = logS + drift + vol_term * Z + lnJ_sum
```

and that is the right way to do it. the diffusion becomes additive in log, and the jumps too, because if a jump multiplies \(S\) by \(J\), then in log space you add \(\ln J\). that is exactly the update

$$
\ln S_{t+\Delta t}
= \ln S_t
+ \left(r-q-\lambda\kappa_J-\frac{1}{2}\sigma^2\right)\Delta t
+ \sigma\sqrt{\Delta t}\,Z
+ \sum_{k=1}^{N} Y_k.
$$

so here the code is not inventing anything. it is just rewriting the theoretical update in a numerically clean form. that is also why it is more stable to add the \(Y_k\) in log space than to multiply a sequence of \(J_k\) directly on spot.

the role of `sample_jump_logsum` in this architecture is clean: `jd_mc_terminal` does not want to know whether the jumps come from Merton, Kou, or something else. it only wants one block that returns

$$
\sum_{k=1}^{N} Y_k
$$

on each path and at each time step. in other words, the diffusion-plus-Poisson engine is generic, and the specific jump law is delegated to the sampler. that is a good split, because you can change the jump law without rewriting the whole simulator.

under Merton, `merton_kappa` codes directly

$$
\kappa_J = E[e^Y - 1] = e^{\mu_J + \frac{1}{2}\sigma_J^2} - 1.
$$

that is the average jump compensation. and `sample_merton_lnJ_sum` does exactly what it should do: it first draws a number of jumps

$$
N \sim \mathrm{Poisson}(\lambda\Delta t),
$$

then if \(N > 0\), it adds up \(N\) normal variables with mean \(\mu_J\) and standard deviation \(\delta\). in other words, it simulates the cumulative log-jump over the step directly. if you want to feel the model, this is where it happens: increasing \(\lambda\) makes jumps more frequent. increasing \(\delta\) makes them more violent. making \(\mu_J\) more negative pushes the average jump mass downward.

under Kou, the logic is the same, but the law of \(Y=\ln J\) becomes asymmetric. `kou_kappa` rewrites

$$
E[e^Y] =
p\frac{\eta_1}{\eta_1-1}
+ (1-p)\frac{\eta_2}{\eta_2+1}
$$

$$
\kappa_J = E[e^Y] - 1.
$$

and `sample_kou_Y` makes the key point of the model explicit: first you choose whether the jump is up or down, then you draw its size from an exponential on one side or the other. so here asymmetry is not a side effect. it is in the law itself. if you decrease \(\eta_2\), the left tail becomes heavier. if you decrease \(p\), you make down jumps relatively more likely. in both cases, you build a steeper skew.

that is exactly where the difference between Merton and Kou becomes conceptually visible.

Merton gives you lognormal jumps. that creates a lot of curvature, a lot of wing, especially on the short end. but unless you put a strong bias into \(\mu_J\), you stay relatively "symmetric."

Kou gives you asymmetry much more directly, because you can control the frequency and the thickness of the up and down tails separately. so if your subject is a heavy left wing and a very steep short-term skew, Kou gives you that lever more cleanly.

if IV BS is flat, good.

if IV Merton bends the wings much more than BS, that is normal: jumps add mass into the tails.

if IV Kou rises much more on low strikes than on high strikes, that is normal too: the downside asymmetry is stronger.

if \(E[S_T]\) Merton or \(E[S_T]\) Kou drifts too far away from the target \(S_0e^{(r-q)T}\), the first suspect is not calibration. it is the drift compensation.

and if you refine the time step and the prices do not stabilize, then again, the problem is numerical before it is economic.

there is also one important thing to see in the structure of the model: here, jumps create immediate tail mass, but they do not create memory. that is exactly the difference versus Heston. in Heston, variance itself is a state variable that mean reverts, so a vol shock can contaminate the rest of the path. in a pure jump-diffusion, you can have a violent event at time \(t\), but the model does not naturally give you a persistent volatility "after-effect." a jump happens, then it is gone. so you recover the front-end smile very well, but not necessarily volatility clustering.

that is why the difference with the earlier models reads cleanly.

under local vol, you imposed the surface and reconstructed a diffusion that matches it.

under Heston, you imposed a persistent variance dynamics and looked at the surface it produces.

here, with jump-diffusion, you add another source of shape: discrete events that abruptly change the level of the underlying.

and that shift matters, because it explains why some very short-dated surfaces are almost impossible to read with a pure diffusion. a diffusion, even a rich one, remains continuous. so at very short maturities it struggles to generate large instant convexity without becoming artificial. a jump model can do it immediately, because a single jump is enough to move an OTM option.

if you want to read the sensitivities properly, you have to read them as mechanism tests, not as arbitrary parameter tweaks.

increasing \(\lambda\) means increasing the frequency of discontinuous risk. so the wings rise.

increasing \(\delta\) in Merton means widening the dispersion of jump sizes. so the extremes get more expensive.

making \(\mu_J\) more negative means shifting jump mass downward. so the skew becomes more negative.

under Kou, decreasing \(\eta_2\) means thickening the left tail. so OTM puts become even more expensive.

decreasing \(p\) means making down jumps more frequent relative to up jumps. so you get the same skew effect.

in other words, the surface coming out of a jump-diffusion does not come from interpolation. it comes from a structure of rare but brutal shocks. that is why the model speaks especially well on the wings and on the short end.

and the final point of the lesson is fairly clean.

in a pure diffusion, uncertainty accumulates continuously.

in a jump-diffusion, part of the uncertainty comes from punctual events, with probability \(\lambda T\) at first order.

that difference in scale is exactly what explains why jumps mark the front-end so strongly. when \(T\) is small, diffusion has not yet had much time to accumulate, but the possibility of a jump is already there. so even at very short maturities, the wings can already be expensive.
