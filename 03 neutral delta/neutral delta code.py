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

T0 = expiry_steps / steps_per_year
total_delta = struct.greeks(S0, T0, bs_params)["delta"]
trade_units, trade_cost = hedger.trade_to_target(-total_delta, S0)
