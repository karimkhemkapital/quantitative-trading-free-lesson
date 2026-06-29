Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Introduction To Econophysics

volatility and risk. they have nothing to do with each other. that had to be stated clearly sooner or later, because if you confuse the two, you read the market with the wrong instrument.

we already know that a market can be very volatile without being especially dangerous. and that, conversely, a market can look calm while being structurally fragile. so the real split is not between "it moves" and "it does not move." it is between movement and rupture.

in the previous lessons, we had already stepped into that idea by talking about diffusion, propagation, uncertainty moving through a system. not in some metaphorical sense. in the physical sense. take a piece of metal. heat one point. you have injected energy somewhere. that energy does not stay localized by magic. it propagates through the material, collision after collision, particle after particle. that is diffusion.

the barest form of it is

$$
\frac{\partial E}{\partial t} = D\nabla^2 E
$$

that equation is not telling some complicated story. it is simply saying how energy spreads through a structure, and that the structure determines how that spreading happens.

the mistake would be to think that temperature is already the danger. but it is not. temperature is just the average level of agitation of particles. it tells you how much things move at the micro level. but a metal does not break because "things move a lot." it breaks because, as energy diffuses, it creates gradients, and therefore internal stresses. one hot zone wants to expand, one cold zone does not follow, and that is how you create a mechanical constraint. so the key point is not \(E\).

it is \(\nabla E\)

it is the difference in energy across the structure.

volatility is the same kind of object as temperature. it is rhythm. it is the amplitude of shocks. it is a measure of "how much it shakes," not of "is it going to break." formally, you can see it as a dispersion

$$
\sigma^2 = E[(X-E[X])^2]
$$

so what does \(\sigma\) tell you? it tells you how a variable fluctuates around its mean. it measures the typical size of deviations. it does not tell you anything about the solidity of the system, its rupture thresholds, or its internal constraints. in other words: volatility describes noise. not failure.

and that is exactly where risk begins.

risk is not "it moves." risk is a conditional probability. probability of what? of a rupture event. not a small harmless -1%. not one more oscillation in a time series. a rupture is a nonlinear event: forced liquidation, inability to exit, gap, cascade, spread widening, impact exploding, drawdown breaking loose, margin failing.

and that probability is conditioned on what? on what actually structures the system: liquidity, leverage, funding, collateral, concentration, margin calls, order-book depth, dependencies between assets, correlations locking up, velocity of money through the system. so if you want to write risk properly, you do not write it as a variance.

you write it like this

$$
\mathrm{risk}=P(\mathrm{rupture}\mid\mathrm{constraints})
$$

that is the minimal mechanics. a rupture probability conditioned on the system's constraints.

and those constraints do not become explosive in a vacuum. they become explosive when the market becomes unreadable. when participants no longer know where they are. when they no longer know which information is reliable, which price is still "real," where liquidity is, who is solvent, who is about to sell, who is already deleveraging. at that point, they stop reacting in calculation mode and switch into defensive mode. that is when the structure tightens.

in other words: there is the mechanics of constraints, and there is the quality of the information circulating inside them.

that is where entropy enters the picture.

in physics, entropy measures a dispersion of states, a loss of readability of the configuration. the higher it is, the harder the system becomes to describe finely. the simplest informational version is

$$
H = -\sum_i p_i \log p_i
$$

the higher \(H\) is, the more uncertainty there is about the state of the system. on a market, this reads very clearly. every price is a message. every tick is an update of the system's state. as long as information circulates cleanly, the market remains readable: you can estimate, you can locate yourself, you can make hypotheses that hold together. as soon as entropy rises, the reading gets blurred, and that is where the trap becomes violent: a market can look calm on the surface, so low realized volatility, while deep down it is already in a high-entropy state. so you read it badly. you underestimate it. you think everything is under control. and it is exactly in that kind of zone that risk becomes active.

because at the end of the day, risk is never "the market moves." risk is "what is the probability that the system breaks, given its structure and given that the readability of that structure is degrading."

said differently, volatility speaks to you about movement. risk speaks to you about whether the system holds under constraint.

and diffusion connects the two, but not in the way people usually say. not in the sense of "the more it diffuses, the more dangerous it is" automatically. what diffuses is not only prices. what diffuses is constraints. one participant sells because they are forced to. that sale moves prices. that move degrades someone else's collateral. that other participant gets a margin call. they sell in turn. liquidity pulls back. impact rises. the spread opens. depth disappears. and what is propagating is no longer an isolated price move, but a fragility advancing step by step.

just like in the metal, except that here what diffuses is not temperature. it is financial stress.

you can almost write it as the propagation of constraint over a network of agents, balance sheets, margins, and order books. there is no need for a giant formula to understand the mechanism. it is enough to see that a local variation can become a global rupture as soon as it encounters a structure that is already tense.

that is why the real question was never:

"how much do I lose if the market moves by X%?"

that is a local sensitivity question. useful, but local.

the real question is:

what is the probability that my system breaks, conditioned on my constraints, the market's constraints, and the informational state of the system?

in other words

$$
\mathrm{risk}=P(\mathrm{rupture}\mid\mathrm{structure},\ \mathrm{constraints},\ \mathrm{entropy})
$$

and then you immediately see why volatility and risk do not coincide.

a very volatile market that is liquid, lightly levered, properly collateralized, with clear information and depth still present, can be relatively low risk.

a low-volatility market that is levered, badly funded, concentrated, with hidden correlations and degraded information, can be very risky.

in the first case, it moves a lot but the structure absorbs it.

in the second case, it moves little but the structure can break.

and that is exactly why using volatility as an automatic proxy for risk is a reading error. volatility does not tell you whether the system has redundancy, depth, or absorption capacity. it does not tell you whether participants are holding positions comfortably or on credit, right at the edge of margin. it does not tell you whether the market is readable or whether everyone is already navigating blind.

volatility only tells you this: here is the observed level of agitation.

risk begins when you ask: if that agitation hits this structure, does it hold?

and from that point on, the reading becomes much cleaner.

if you want to look at noise, you look at a dispersion.

if you want to look at rupture, you look at a conditional probability.

if you want to understand how rupture becomes systemic, you look at the diffusion of constraints.

if you want to understand why participants so often misread that probability, you look at informational entropy, which means the quality of the system's readability.

so the final separation is clean.

volatility is the amplitude of movement.

risk is the probability of rupture, conditioned by structure, its constraints, and the informational state of the market.

and it is precisely because that probability depends on structure and readability, not only on movement, that a market can look calm and already be dangerous.
