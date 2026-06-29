Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Entropy

in the previous lesson, we established a simple point, but one that is too often treated like a metaphor when in fact it is a constraint. the market does not "take" a shock and then return to the same state as if nothing had happened. a shock changes the state of the system. it changes liquidity, inventories, margin constraints, positioning, execution speed, the synchronization of participants. and that modified state does not disappear instantly. it persists.

that is the starting point. as long as that modification persists, it conditions the way the market reacts to the next shock. in the short term, you see it in microstructure. in the medium term, in deleveraging. in the long term, in the rebuilding of liquidity and depth. in other words, the shock does not just leave a trace in price. it leaves a trace in the system's slow variables. and that trace changes the whole set of possible responses.

as long as that trace remains weak, the system absorbs. it dampens. it redistributes pressure. but as constraints accumulate, the space of responses tightens. fewer counterparties remain. less depth. less room to maneuver. less ability to dissipate locally what is coming in. and beyond a certain point, the response is no longer a fluctuation around an equilibrium. it is a regime shift. the market accelerates, gaps, slips, dislocates. that is what it means to cross a critical threshold.

formally, the split runs through this question: are you describing the market as an object without memory, or as a system whose dynamics depend on an internal state?

if you write returns as i.i.d. with constant variance,

$$
r_t \sim \mathrm{i.i.d.}(0,\sigma^2)
$$

you are already imposing something very strong. you are imposing that the law of the system today is the same as tomorrow. you are imposing that risk reduces to a dispersion around a center. it is convenient. it is clean. but it is not neutral. because that representation removes, by construction, the variable that makes a system tip: the evolution of its internal state.

a representation that is more faithful to the idea of persistence is to say that the dynamics depend on a latent state \(X_t\), which is precisely what carries the regime's memory. that state can represent pressure, liquidity, balance-sheet constraints, the synchronization of behavior, the effective density of counterparties. at that point, you write, for example,

$$
dS_t = \mu(S_t,X_t)S_t\,dt + \sigma(S_t,X_t)S_t\,dW_t
$$

with \(X_t\) no longer treated as some side detail, but as the object carrying the memory of the system.

the point here is not to "make the model more complicated." the point is to recognize that in a market that is becoming fragile, what changes is not only the size of fluctuations. what changes is the structure of the absorption mechanisms that maintain stability while things still hold together.

and that is exactly where conventional statistical models miss something when they stay focused exclusively on the center of the distribution. in a Gaussian setting, extremes decay very fast. for a standard normal, asymptotically, via Mills' ratio

$$
P(X>x) \approx \frac{1}{x\sqrt{2\pi}}e^{-x^2/2}, \quad x \to \infty
$$

the implicit reading behind that decay is: large events are "out of norm," so their past absence almost becomes evidence of safety. but that conclusion is not a solid observation. it is a circular inference. you assume stationarity, then use a stationary period to conclude that risk was low.

in practice, a large share of stylized facts contradicts that rapid decay. the observed tails are often thicker. exceedance probabilities look much more like a power law

$$
P(|r|>x) \sim x^{-\alpha}
$$

with \(\alpha\) often on the order of 3, which is sometimes summarized as the "inverse cubic law." the important point here is not to turn this into a slogan like "the Gaussian is false." that is not the issue. the issue is that if you calibrate your intuition of risk on exponential decay, you make invisible the mechanisms that manufacture ruptures.

that is the core of Taleb's critique in The Black Swan. not a critique of science, and not an ideological "Gaussian vs non-Gaussian" debate either. the critique targets a biased use:

confusing simplicity of form with structural validity. the problem is not having a simple law. the problem is erasing, by construction, everything that does not look like the average regime: slow accumulation, homogenization of behavior, correlations rising into regime, silent transitions, liquidity saturation, compression of the space of possible responses.

if your model only looks at the center, it cannot see the progressive construction of fragility.

at this stage, the right question is not psychological. it is mechanical. and that is precisely why physics gives a better guide than "exogenous" narratives. in fluids, Navier-Stokes puts nonlinearity at the center from the outset

$$
\frac{\partial u}{\partial t} + (u\cdot\nabla)u
= -\frac{\nabla p}{\rho} + \nu\Delta u
$$

and the regime depends on a global parameter like the Reynolds number

$$
Re = \frac{UL}{\nu}
$$

when \(Re\) is low, the system dissipates efficiently. it remains stable. it absorbs perturbations without changing its nature. beyond a threshold, the regime changes. instabilities, turbulence, bifurcation. that is not an anomaly. it is a structural property of the system.

the market follows a logic of the same type, with its own dissipation mechanisms: order-book depth, diversity of counterparties, margin constraints, balance-sheet capacity, speed of information propagation, thickness of passive liquidity, elasticity of collateral. as long as that absorption capacity remains sufficient, the system redistributes flows without changing regime. when it contracts, equilibrium becomes fragile. beyond a certain point, the response is no longer linear. price no longer adjusts, it accelerates. it no longer absorbs, it slips. it no longer rebalances, it dislocates.

that is not a "market error." it is the signature of a threshold being crossed.

and that is where the continuity with everything we have already seen in options becomes clear. pricing under the risk-neutral measure imposes price consistency.

typically

$$
V_0 = E^Q[e^{-rT}H(S_T)]
$$

that equation is indispensable. but by itself it says nothing about the stability of the regime generating \(S_t\). it tells you how to price conditionally on a given dynamics. it does not tell you whether that dynamics is changing in nature.

the bridge with the actual dynamics is sensitivity.

Greeks are derivatives, so they are exposure sensors

$$
\Delta = \frac{\partial V}{\partial S},
\quad
\Gamma = \frac{\partial^2 V}{\partial S^2},
\quad
\nu = \frac{\partial V}{\partial \sigma}
$$

and the important point is not only that they measure "how much price changes." in a real book, they induce hedging flows. so they do not remain passive. they feed back.

when convexity dominates, hedging itself becomes a market mechanism. if aggregate exposure is short convexity, meaning short gamma, then hedging is procyclical: it sells when the market goes down and buys when it goes up. so what should have been a local stabilization becomes an amplifier. again, there is nothing mystical there. it is not "the market panics" as an empty phrase. it is a feedback loop.

and that is exactly where the notion of state becomes central again. because what matters is not only the initial move. it is the state of the system onto which that move lands, and the way local loops will amplify or dissipate it. a system that still has depth, little constraint, and still flexible balance sheets absorbs. a system already contracted, already synchronized, already short convexity, does not respond in the same way.

so "modelling correctly" does not mean piling up more and more sophisticated distributions. it means changing the variable of interest.

forget the mean as your compass.

forget standard deviation as your definition of risk.

the right object to estimate is a state of stability.

in other words: the pressure that is accumulating, the contraction of possible responses, the intensification of local loops, the progressive exhaustion of dissipation.

in practice, you read that through testable indicators. not narratives. in the exhaustion of passive orders. in imbalanced aggressions. in the disappearance of counterparties. in the instability of portfolio sensitivities. in the abrupt rise of effective correlations. in the deformation of depth. in the fact that the hedge itself begins to become an amplification agent.

that is where the rupture point sits. not in some magical threshold written in the sky. in the moment when the system stops having enough degrees of freedom to absorb what is hitting it.

from there, the objective is no longer to predict a direction. the objective is to estimate whether the system is still in a zone where its absorption mechanisms are holding, or whether it has already left that zone.

and to adjust exposure accordingly.

not as a function of a narrative scenario.

not as a function of a story told after the fact.

but as a function of the system's measurable capacity to absorb what is coming, and of the way your own tools hedge, execution, leverage, financing interact with the regime's mechanics.

if you want to condense the whole lesson, it almost sits here:

a market does not break because it moves a lot. it breaks when its internal state has changed so much that its absorption mechanisms are no longer enough to dissipate what is coming.
