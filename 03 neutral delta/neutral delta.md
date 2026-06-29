Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# lesson-3-neutral-delta

Any option sale is a premium collected now against a risk that can hit later.
And this premium is only earned "for real" if the scenario that triggers the payoff does not happen, or gets neutralized but nobody can guarantee that this scenario won't happen.

The seller receives certain cash today, but they carry an exposure that can become very large tomorrow; if nothing is done behind it, it's a position that can spiral by construction.

The underlying moves. And as soon as it moves, delta moves too, so if nothing is adjusted, the exposure drifts by itself.

The only way to keep the exposure "clean" is to adjust continuously with the underlying: delta-neutral in dynamics.

Example:

Total delta of the options = -0.25 -> you need +0.25 of the underlying to compensate.

Spot moves -> delta becomes -0.18 or -0.35.

So the hedge re-aligns: you reduce or you increase the quantity of the underlying.

The goal is not to catch the up move or the down move.

The goal is to keep the exposure controlled while time passes and the market moves.

The premium is only defended if the risk is kept under control the whole way through.

Without delta-neutral, selling an option amounts to taking a direction without admitting it.

And that direction becomes dependent on things that change all the time: volatility, liquidity, flow, regime.

None of these things leaves an exposure "stable" if you don't hedge.

An unhedged seller doesn't have a strategy: they have exposure to randomness.

The real subject is not "performance", it's "is the position being held".

A pro position doesn't drift: it re-aligns.

As long as the balance is maintained, the premium looks like insurance income with no directional bet.

As soon as the balance breaks, it's no longer a structured sale, it's an open risk take.

That's what separates a hedged position from an unstable position.

And that's what decides whether an options strategy stands up or not.

## What is being neutralized?

Goal: maintain total

$$
\Delta \approx 0,
$$

where:

$$
\Delta_{\text{total}} = \Delta_{\text{options}} + \text{hedge\_units}.
$$

We offset the option's delta with an opposite position in the underlying asset.

```python
def bs_price_greeks(S: float, K: float, T: float, sigma: float, r: float, q: float,
                    is_call: bool) -> Dict[str, float]:
    if T <= 0:
        if is_call:
            price = max(S - K, 0.0)
            delta = 1.0 if S > K else 0.0 if S < K else 0.5
        else:
            price = max(K - S, 0.0)
            delta = -1.0 if S < K else 0.0 if S > K else -0.5
        return {"price": price, "delta": delta, "gamma": 0.0, "vega": 0.0,
                "theta": 0.0, "rho": 0.0}

    d1 = _d1(S, K, T, sigma, r, q)
    d2 = _d2(d1, sigma, T)
    Nd1 = norm_cdf(d1); Nd2 = norm_cdf(d2)
    df_r = math.exp(-r * T); df_q = math.exp(-q * T)

    if is_call:
        price = df_q * S * Nd1 - df_r * K * Nd2
        delta = df_q * Nd1
    else:
        price = df_r * K * norm_cdf(-d2) - df_q * S * norm_cdf(-d1)
        delta = -df_q * norm_cdf(-d1)

    nd1 = norm_pdf(d1)
    gamma = df_q * nd1 / (S * sigma * math.sqrt(T))
    vega = S * df_q * nd1 * math.sqrt(T)
    theta = (
        (-S * df_q * nd1 * sigma / (2 * math.sqrt(T)) - r * K * df_r * Nd2
         + q * S * df_q * Nd1)
        if is_call
        else (-S * df_q * nd1 * sigma / (2 * math.sqrt(T))
              + r * K * df_r * norm_cdf(-d2) - q * S * df_q * norm_cdf(-d1))
    )
    return {"price": float(price), "delta": float(delta), "gamma": float(gamma),
            "vega": float(vega), "theta": float(theta), "rho": float(r)}


class ShortStraddle:
    def __init__(self, S0: float, K: float, iv: float, qty: float, expiry_steps: int):
        self.call = OptionSpec(True, K, iv, -abs(qty), expiry_steps)
        self.put = OptionSpec(False, K, iv, -abs(qty), expiry_steps)

    def greeks(self, S: float, T_years: float, params: BSParams) -> Dict[str, float]:
        g_call = bs_price_greeks(S, self.call.strike, T_years, self.call.iv, params.r,
                                 params.q, True)
        g_put = bs_price_greeks(S, self.put.strike, T_years, self.put.iv, params.r,
                                params.q, False)
        return {k: self.call.qty * g_call[k] + self.put.qty * g_put[k] for k in
                g_call.keys()}
```

## What controller enforces neutrality?

Goal: determine how many units of the underlying to trade in order to target
\(\Delta_{\text{total}}=0\), and when to rebalance.

Rule:

$$
\text{Hedge target} = -\Delta_{\text{options}}.
$$

Trigger threshold:

Rebalancing only occurs if

$$
|\Delta_{\text{total}}| > \text{threshold}.
$$

This threshold is adaptive, a function of \(|\Gamma|\) (gamma) and recent variance to avoid over-hedging during noise.

```python
class DeltaHedger:
    def __init__(self, cfg: HedgeConfig, cost: CostModel):
        self.cfg = cfg
        self.cost = cost
        self.hedge_units = 0.0

    def adaptive_threshold(self, gamma: float, spot: float, ret_var: float) -> float:
        base = self.cfg.delta_threshold_base
        adj = base / (1.0 + self.cfg.gamma_sensitivity * abs(gamma) * spot
                      + self.cfg.var_sensitivity * math.sqrt(max(ret_var, 1e-12)))
        return float(min(self.cfg.max_threshold, max(self.cfg.min_threshold, adj)))

    def trade_to_target(self, target_delta_units: float, price: float) -> Tuple[float,
                                                                               float]:
        trade_units = target_delta_units - self.hedge_units
        trade_units = float(np.clip(trade_units, -self.cfg.max_trade_size,
                                    self.cfg.max_trade_size))
        notional = abs(trade_units) * price
        fee_cost = abs(trade_units) * self.cost.fee_per_share
        slip_cost = notional * (self.cost.slippage_bps * 1e-4)
        spread_cost = notional * (self.cost.spread_bps * 1e-4)
        trade_cost = fee_cost + slip_cost + spread_cost
        self.hedge_units += trade_units
        return trade_units, trade_cost
```

## Where is neutrality applied in the execution flow?

Two moments:

- At the start (instantaneous neutralization)
- At each step (conditional rebalancing)

## 3.1 Initial hedge (setting \(\Delta_{\text{total}}=0\))

Goal: start neutral. Compute \(\Delta_{\text{options}}\) and take \(-\Delta_{\text{options}}\) in the underlying.

```python
T0 = expiry_steps / steps_per_year
total_delta = struct.greeks(S0, T0, bs_params)["delta"]
trade_units, trade_cost = hedger.trade_to_target(-total_delta, S0)
```

## 3.2 Dynamic rebalancing (if deviation > threshold)

Goal: if the spot price has moved, \(\Delta_{\text{options}}\) changes.

We compute \(\Delta_{\text{total}}\) and act only if the deviation exceeds the threshold.
