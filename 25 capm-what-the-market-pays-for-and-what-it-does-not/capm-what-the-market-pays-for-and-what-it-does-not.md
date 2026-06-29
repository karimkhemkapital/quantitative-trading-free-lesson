Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# CAPM What The Market Pays For And What It Does Not

With Markowitz, we already put an important piece on the table. We know how to take a set of risky assets, define an expected return vector $\mu$, a covariance matrix $\Sigma$, then look for weights that organize the trade-off between return and variance. At that stage, we know how to build an efficient portfolio. We know how to move risk around. We know how to spread it. We know how to compress it.

But something is still missing.

Because Markowitz, taken on its own, remains an individual problem. One investor looks at their assets, their parameters, then chooses their point on the efficient frontier. It is clean, but it is still local. It still does not tell us what the market rewards in equilibrium. It does not tell us which part of risk has a price, and which part does not.

That is exactly where CAPM comes in.

The move is simple. We keep the mean-variance logic, then we add a risk-free asset with rate $r_f$. The moment that risk-free asset appears, the geometry changes completely. Before, we were moving along a curved frontier. Now, we can take any risky portfolio $w$, mix it with the risk-free asset, and build an entire line in the return-risk plane.

If $w$ is a risky portfolio such that

$$
\mathbf{1}^{\top}w = 1
$$

and if $y$ is the fraction of capital allocated to that portfolio, then the rest $(1-y)$ goes into the risk-free asset.

The return of the combined portfolio is

$$
R_p = r_f + y(R_w - r_f)
$$

so in expectation

$$
\mathbb{E}[R_p] = r_f + y(\mathbb{E}[R_w] - r_f)
$$

and its risk is

$$
\sigma_p = |y|\sigma_w
$$

That means each risky portfolio $w$ gives rise to a line starting from $r_f$.

Its slope is the excess return per unit of risk. In other words, its Sharpe ratio:

$$
S(w) = \frac{\mathbb{E}[R_w] - r_f}{\sigma_w}
$$

From there, the problem tightens very quickly. We are no longer just looking for "a good portfolio" among others. We are looking for the line that dominates all the others.

So we look for the risky portfolio that maximizes the Sharpe ratio. That portfolio is the tangency portfolio.

In matrix form, its direction is given by

$$
w_T \propto \Sigma^{-1}(\mu - r_f\mathbf{1})
$$

and after normalization so that

$$
\mathbf{1}^{\top}w_T = 1
$$

we get

$$
\widetilde{w}_T =
\frac{\Sigma^{-1}(\mu - r_f\mathbf{1})}
{\mathbf{1}^{\top}\Sigma^{-1}(\mu - r_f\mathbf{1})}
$$

From that point on, everyone ends up facing the same structure. If all investors see the same $(\mu,\Sigma)$ and the same $r_f$, then they also see the same tangency portfolio. The differences between investors no longer concern the risky core of the portfolio. They only concern the sizing. Some hold more of the risk-free asset, others less. Some use leverage, others do not. But the risky block itself is the same.

That is the separation theorem.

And once that separation is there, equilibrium arrives almost by itself. Because if everyone holds the same risky portfolio, then the aggregation of all risky positions held in the economy is precisely the market portfolio. So in equilibrium,

$$
\widetilde{w}_T = w_M
$$

The tangency portfolio becomes the market portfolio.

At that point, the line that starts from $r_f$ and passes through the market becomes the central line of the model. That is the Capital Market Line:

$$
\mathbb{E}[R_p]
= r_f
+ \frac{\mathbb{E}[R_M] - r_f}{\sigma_M}\sigma_p
$$

It says something very clear: for an efficient portfolio, the expected excess return is proportional to its total volatility, with the market Sharpe ratio as the slope.

But that is still only half the story.

Because the real question is not just "how do we price an efficient portfolio?" The real question is: how do we price an individual asset?

And that is where CAPM makes a much finer move.

Take an asset $i$. Its total risk can be split into two parts. One part moves with the market. One part belongs to the asset itself. We can write it like this:

$$
R_i - r_f = \beta_i(R_M - r_f) + \epsilon_i
$$

with

$$
\beta_i = \frac{\mathrm{Cov}(R_i,R_M)}{\mathrm{Var}(R_M)},
\qquad
\mathrm{Cov}(\epsilon_i,R_M)=0
$$

That decomposition is decisive. It says that the excess return of an asset contains a systematic component, carried by $\beta_i$, and a residual component $\epsilon_i$, orthogonal to the market.

And that is where the economic core of CAPM really appears.

The piece $\epsilon_i$ is idiosyncratic risk. The asset's own noise. The local accident. The governance problem. The isolated announcement. The surprise that does not mechanically propagate to the whole system. That component can be diversified away. Once you hold a sufficiently broad portfolio, those residuals largely offset one another. They do not disappear in an absolute sense, but they stop being the dominant risk.

In other words, the market has no reason to keep paying for a risk that anyone can dilute through diversification.

So what the market pays for is not total risk. It is not $\sigma_i$ by itself. It is not "how much this asset moves." What the market pays for is the part of risk that remains tied to the market itself, the part that cannot be removed simply by holding more lines in a portfolio.

That part is beta.

In equilibrium, the specific residual should not carry an average premium. Otherwise, it would be enough to isolate a portfolio with no market exposure but with positive excess return, which would break the logic of mean-variance equilibrium.

So

$$
\mathbb{E}[\epsilon_i] = 0
$$

Taking expectations in the previous decomposition immediately gives

$$
\mathbb{E}[R_i] - r_f
= \beta_i(\mathbb{E}[R_M] - r_f)
$$

That is CAPM.

The whole logic of the model is there, in one line: an asset's risk premium is equal to its beta times the market risk premium.

If $\beta_i=1$, the asset carries the same systematic exposure as the market. So it must offer the same risk premium as the market.

If $\beta_i>1$, the asset amplifies market moves. It carries more systematic risk. So it must offer a higher premium.

If $\beta_i<1$, it moves less than the market on average. Its premium is lower.

If $\beta_i<0$, then we have an asset that partially hedges the market. Its value rises when the market suffers, or at least it moves in the opposite direction. In that case, the required premium can become very small, or even negative, because that asset provides a hedging service.

The relation

$$
\mathbb{E}[R_i]
= r_f + \beta_i(\mathbb{E}[R_M] - r_f)
$$

defines the Security Market Line.

And here, one point needs to be handled carefully, because a lot of people mix up the two lines. The Capital Market Line talks about efficient portfolios and links expected return to total volatility $\sigma_p$. The Security Market Line talks about individual assets, or any portfolio, and links expected return to beta. On one side, we price the efficiency of a complete portfolio. On the other, we price systematic exposure.

That is why a highly volatile stock does not automatically deserve a large premium. If it is very volatile but that volatility is mostly idiosyncratic, and therefore diversifiable, then that agitation has no reason to be paid. And that is exactly where CAPM breaks the naive intuition that "the more it moves, the more it should return." No. The more it moves with the market, the more it should return.

The practical consequence is heavy.

When you look at an asset, you can always measure its variance, its standard deviation, its drawdowns, its kurtosis, its jump structure, whatever you want. But in the CAPM framework, none of those is the central variable for determining its equilibrium risk premium. The central variable is

$$
\beta_i = \frac{\mathrm{Cov}(R_i,R_M)}{\mathrm{Var}(R_M)}
$$

So the question is no longer just: "how unstable is this asset?" The question becomes: "how does this asset load the market portfolio?" "What does it add to the risk that cannot be diversified away?"

That is why CAPM is deeper than a simple regression line sitting in the corner of a spreadsheet. It changes the very object we call "risk." It says: the risk that matters for pricing is not raw dispersion. It is the marginal contribution to the risk of the market portfolio.

We can even rewrite it in another form:

$$
\mathbb{E}[R_i] - r_f
= \frac{\mathrm{Cov}(R_i,R_M)}{\mathrm{Var}(R_M)}
(\mathbb{E}[R_M] - r_f)
$$

That form makes the structure even clearer. The price of risk is not an isolated volatility. It is a covariance. So a co-movement. So a dependence on the aggregate dynamics of the system.

And that is exactly why CAPM became a foundation stone for a huge part of modern finance. Not because it describes reality perfectly. Reality spills far beyond this framework. There are frictions, funding constraints, information asymmetries, jumps, regimes, multiple factors, anomalies that do not fit neatly into a single beta line. But even with all that, CAPM locked in one idea that never really left finance: a diversifiable risk has no reason to be paid the way systematic risk is paid.

And if you want to say it in one simple sentence: Markowitz teaches you how to combine risks. CAPM tells you which of those risks has a price in equilibrium.

That is why people usually start with Markowitz and then move to CAPM. The first organizes the portfolio. The second brings out the equilibrium logic. The first tells you how the mix is built. The second tells you what the market rewards inside that mix.

And the final formula, the one to keep, is this one:

$$
\mathbb{E}[R_i]
= r_f + \beta_i(\mathbb{E}[R_M] - r_f)
$$

Everything else revolves around it.

Because in the end, CAPM always says the same thing: the market does not pay you for carrying noise. It pays you for carrying the part of risk that is still there after the noise has already been diversified away.
