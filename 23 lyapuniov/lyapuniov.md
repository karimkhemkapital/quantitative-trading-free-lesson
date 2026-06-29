Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Lyapuniov

in the previous lesson, Lyapunov was used to read one precise thing: the propagation speed of a perturbation. here, we go one layer deeper. we do not stay at the level of the idea anymore, we move to the level of the mechanism. in other words: how do we estimate it, and above all, what does that estimate actually tell us about a market regime.

this code answers one single question:

when an anomaly appears, does the system kill it... or does it make it grow.

and that is where the split is. you are not measuring "the move." you are not measuring "direction." you are measuring propagation.

```python
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
```

the starting point is the signal. not to look at candles. not to tell a story about "it goes up" or "it goes down." here, the signal is used to reconstruct a system.

because a system does not live on a single point \(t\). it lives on a trace. what it has just done already conditions what it can do next. so instead of looking at an isolated value, the code reconstructs a state from several past points. that is the role of delay and dimension.

said differently, we take a line of prices or returns, and we turn it into small local configurations. each configuration is no longer "an instant," it is a short memory. a way to capture the internal position of the system at that moment.

$$
X_t = (x_t, x_{t+\tau}, x_{t+2\tau}, \ldots, x_{t+(m-1)\tau})
$$

what \(X\) does in the code is exactly that. a state-space reconstruction. we leave the flat reading of the series and move into a geometric reading of the dynamics.

then, for each state, we search for another moment in the past where the system was almost in the same state. not identical, otherwise it would be artificial. not completely different either, otherwise the comparison is useless. what we are looking for is a near-twin.

```python
dists = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=-1)
np.fill_diagonal(dists, np.inf)
nearest = np.argmin(dists, axis=1)
```

that is the core of it. we compute all the distances between reconstructed states, then for each one we take its nearest neighbor. so for every local configuration of the system, we recover another point in the past where the structure, the constraint, the internal tension looked similar.

and that is where the test becomes interesting.

you are not simply asking: "do they look alike?"

you are asking: "what happens to their small difference right after?"

at the start, the distance between the two states is \(d_0\). one step later, it is \(d_1\).

$$
d_0 = \lVert X_i - X_j \rVert,
\quad
d_1 = \lVert X_{i+1} - X_{j+1} \rVert
$$

Does the small initial difference stay contained... or does it grow.

if it grows, that means a tiny deviation is enough to make the trajectories diverge. and that is no longer a reading of noise. it is a reading of instability.

in the code, this local divergence is measured like this

```python
log_div = np.log(d1 / d0)
```

why the log? because what we want to capture is not just a raw distance. what we want to capture is a law of amplification. if the system is in a regime where deviations propagate, the growth is not linear in the naive sense. it follows a contamination logic. the logarithm brings that amplification back into a workable scale.

$$
\lambda_{\mathrm{local}} = \log\left(\frac{d_1}{d_0}\right)
$$

if \(d_1 > d_0\), the log is positive: the gap has grown.

if \(d_1 \approx d_0\), the log is close to zero: the gap is stable.

if \(d_1 < d_0\), the log is negative: the gap is contracting.

then the code takes the average of all these local divergences

```python
return float(np.mean(diverge))
```

and that is what the Lyapunov exponent means here in the operational sense of the code. not "the absolute truth" about market chaos. not a pure theoretical exponent coming out of an ideal deterministic system. just a clean, testable proxy to answer a desk-level question:

when two almost identical states appear, do they remain close... or does the regime separate them.

and at that point, the reading in risk language becomes very clean.

if the result is \(>0\), the system amplifies.

a small anomaly does not stay local. it propagates. it takes space. it can become a chain reaction. in this type of regime, you do not even need a large exogenous shock. the structure itself already knows how to manufacture instability from almost nothing.

if the result is \(\approx 0\), the system is on the edge.

it does not really dissipate. it does not really amplify either. it holds, but without margin. this is typically the kind of state where everything still looks calm as long as no extra push arrives. the surface looks neutral, but stability is already no longer solid.

if the result is \(<0\), the system dissipates.

gaps tighten. perturbations are absorbed, spread out, neutralized. that does not mean "no risk." it just means that at that moment, the internal mechanics are still acting like a shock absorber instead of acting like a multiplier.

and that is exactly where the logic of the metric should not be missed: this is not a trend indicator, this is not an oscillator, this is not a price reading in the classical sense. Lyapunov does not tell you where the market is going. it tells you how a perturbation lives inside the regime.
