Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-1-intro

In a market, you can only buy or sell two kinds of things: either a property claim (equity/ownership), or a contractual commitment (bonds, futures, repos, swaps, options).

An option is simply a contract you enter into that gives you the right to acquire an asset or a property claim at a certain date and at a price fixed in advance.

In practice, the buyer pays to transfer a risk they are exposed to like a price increase or a price drop to the one who sells the option.

They pay what we call a premium to transfer that risk.

The seller, on the other hand, receives a certain premium today, but agrees to carry that risk on their shoulders.

So that's why saying options are just a "leverage tool" is completely wrong even if an option can provide non-linear exposure with limited initial cash.

Because the core of the product is the structured transfer of a conditional risk.

The seller pockets the premium today, but behind that, they carry the payoff risk tomorrow.

And since nobody knows where the price will be at expiration, they can't afford to "wait and see," because otherwise they expose themselves to paying massively in unfavorable scenarios.

So if they sell an option seriously, they must hedge themselves: build a hedge that reduces their risk as the market moves, instead of betting on a direction.

And to build that hedge, you need a minimal model of price movements just enough to translate "the market moves randomly" into something you can compute.

That's where we introduce a simple dynamic, geometric Brownian motion, to describe `(St)` and derive a distribution (a law) for `(St)`.

And it's that distribution that then lets you talk properly about price, premium, and hedging.
