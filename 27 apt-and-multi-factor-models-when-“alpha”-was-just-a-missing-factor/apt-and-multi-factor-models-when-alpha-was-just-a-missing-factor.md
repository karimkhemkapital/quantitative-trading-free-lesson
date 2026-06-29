Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# APT and Multi-Factor Models: When "Alpha" Was Just a Missing Factor

with CAPM, we closed a first loop. the market does not pay for "risk" in the abstract. it does not pay for the raw agitation of an asset. it pays for the part of risk that stays attached to the system, the part you cannot make disappear just by diversifying. put differently: what has a price is not the noise specific to one line. it is that line's exposure to a common constraint.

on paper, that is clean. very clean, even.

the problem starts when you look at the facts. you take portfolios, styles, entire baskets, and you see that the CAPM residual does not die out cleanly. something remains. an "alpha." a drift. a premium that keeps living even though, inside a one-factor framework, it should already have been absorbed.

and that is where you have to be very careful with the diagnosis. because that "leftover" can mean two very different things.

either you tell yourself the market is mispriced, irrational, inefficient, and handing out free return to whoever knows where to look. or you take the simpler, drier, more solid hypothesis: your model is too poor. there are missing common forces in the description. what you are calling "alpha" may not be a miracle at all. it may just be systematic risk that has been cut the wrong way.

that is exactly where APT comes in.

the idea is not complicated. CAPM was basically saying: there is one big common direction, the market, and each asset is paid according to how much it loads on that direction. APT says: no, the system is thicker than that. there are several sources of constraint. several common engines. several blocks moving through assets at the same time. and if you forget part of those blocks, then your residual starts talking in place of the model.

in other words, you replace a single-factor structure with a multi-factor one.

you then write the return of asset i as

$$
R_i = \alpha_i + \beta_{i1}F_1 + \beta_{i2}F_2 + \cdots + \beta_{iK}F_K + \epsilon_i
$$

and that expression deserves to be read properly. the \(F_k\) are the factors. not decorative variables. not regression gadgets. they are the common directions carrying systematic risk. growth, inflation, credit spread, curve slope, momentum, value, liquidity, carry, whatever you want depending on the framework you are working in. the point is not that the list is universal. the point is that a factor, here, is a force that cuts across several assets at once.

the \(\beta_{ik}\) are the loadings. the way asset \(i\) reacts to each force. some assets take the same push. others amplify it. others offset it. so \(\beta\) is not a label. it is the exposure geometry of the asset to the common constraint.

and \(\epsilon_i\) is the residual. the local noise. the specific accident. what remains once you have stripped out the systematic part carried by the factors.

we then impose the minimal mechanics

$$
E[\epsilon_i] = 0, \qquad Cov(\epsilon_i, F_k) = 0 \quad \text{for all } k
$$

that means only one thing: the residual must not contain, on average, a forgotten common force. otherwise it is no longer a residual. it is just a misspecified factor hiding inside the noise.

and this is where the link with CAPM remains intact at the core. the real split is not between "high volatility" and "low volatility." the real split is between what can be diversified away and what cannot.

if you hold a broad portfolio, the \(\epsilon_i\) largely offset each other. the stories specific to each line get diluted. local accidents cancel out. but the factors do not vanish that way. if inflation re-accelerates, if liquidity contracts, if duration compresses, if credit spreads tighten or fracture, that is not a small noise disappearing into an average. it is a common constraint. it moves through several portfolios at the same time. it changes the regime.

so APT starts from a very dry idea if systematic risk is properly spanned by several factors, and if the residual is sufficiently diversifiable, then expected return must be a linear function of factor exposures. otherwise, you can build portfolios that neutralize the factors, diversify away the idiosyncratic part, and still keep a certain gain. and at that point, you do not have a "style." you have an arbitrage.

that is why we move from the decomposition equation

$$
R_i = \alpha_i + \sum_{k=1}^{K} \beta_{ik}F_k + \epsilon_i
$$

to the pricing equation

$$
E[R_i] = r_f + \beta_{i1}\lambda_1 + \beta_{i2}\lambda_2 + \cdots + \beta_{iK}\lambda_K
$$

where \(\lambda_k\) is the risk premium of factor \(k\).

that is the core of the lesson.

in CAPM, you had one single risk premium: the market's. here, you break that single block into several prices of risk. each factor carries its own premium. each exposure loads its own constraint. and the expected return of an asset becomes the sum of those loadings weighted by the corresponding prices.

if you write it in excess-return form, it becomes even cleaner.

define

$$
R_{i,ex} = R_i - r_f
$$

and you get

$$
E[R_{i,ex}] = \sum_{k=1}^{K} \beta_{ik}\lambda_k
$$

so all at once, the word "alpha" completely changes status.

in a one-factor model that is too poor, alpha may simply mean: something is missing in the span of systematic risk. you think you are seeing an anomaly. in reality, you are seeing an absent factor. you think you have isolated skill. in reality, you just cut the common forces the wrong way.

and that is where APT is much more disciplining than it first looks. it forces you to ask the right question. not "does this portfolio have alpha?" but "relative to what factor space?" because alpha never exists in a vacuum. alpha is always a residual conditional on a model structure. change the structure, change the factors, change the span, and the residual changes with it.

that is why, in practice, a lot of "alphas" disappear when you enrich the factor base. a portfolio that seemed to beat the market with a nice CAPM residual can become completely ordinary once you add value, momentum, quality, carry, credit, volatility, or liquidity. not because the performance was fake. but because it was not "outside the model": it was simply being carried by engines your first model was not looking at.

the important point here is not to turn factors into a religion. a factor is not a fashion. a factor is not a Pinterest list of trendy exposures. a factor only makes sense if it carries a common constraint and explains a stable part of co-movement. otherwise you are not doing APT. you are doing statistical decoration.

and that is precisely why the multi-factor logic fits naturally into everything we already laid down about regimes, propagation, and constraints. because a factor, deep down, is nothing more than a stable direction through which the system transmits a shock.

if duration compresses everywhere, that is not a line-by-line accident. if credit spreads widen and fragile balance sheets come under pressure, that is not a series of coincidences. if liquidity disappears and the most crowded assets start dropping together, once again that is not a collection of small independent residuals. it is a common force. therefore, a potential factor.

put differently: the factor is the mathematical form of a shared constraint.

and that is where the reading becomes clean. in a CAPM world, everything points back to the market portfolio. in an APT world, the market is no longer the only direction that matters. it becomes a special case inside a wider space. an asset is no longer summarized by one single \(\beta\). it carries a richer exposure signature

$$
\beta_i = (\beta_{i1}, \ldots, \beta_{iK})
$$

and the real question is no longer "is this stock aggressive or defensive?" the real question is: which common constraints is it plugged into, with what intensity, and which of those risks is actually being paid.

that also changes the way you read a portfolio.

if you have a portfolio \(w\), then its exposure to factor \(k\) becomes

$$
\beta_{p,k} = \sum_{i=1}^{N} w_i\beta_{ik}
$$

and its expected excess return is

$$
E[R_{p,ex}] = \sum_{k=1}^{K} \beta_{p,k}\lambda_k
$$

that means a portfolio is no longer just "more or less risky." it is a combination of factor loadings. so an assembly of constraints. you can have two portfolios with the same volatility and completely different mechanics, simply because they do not carry the same factors.

and that is exactly why variance alone is never enough to tell the story of a portfolio. two objects can move just as much, yet not be exposed to the same forces. so they do not break for the same reasons. so they are not being paid for the same thing.

empirically, APT opened the door to the whole modern factor-finance world. Fama-French, Carhart, quality, low vol, profitability, investment, carry, value, momentum: all of that lives in continuity with this idea. but the conceptual core has to stay intact, otherwise you get lost in catalogs. the core is simple: what you call "abnormal" return depends entirely on the factor structure you accepted upstream.

and that matters, because it breaks a very stubborn illusion: thinking that a residual is automatically proof of inefficiency. no. sometimes, yes. often, no. very often, the residual is simply the bill you pay for an incomplete model.

if you want to say it as directly as possible: CAPM put down a correct intuition, but one that was too narrow. it said the market pays systematic risk. APT keeps that idea, but it refuses to reduce the systematic to a single direction.
