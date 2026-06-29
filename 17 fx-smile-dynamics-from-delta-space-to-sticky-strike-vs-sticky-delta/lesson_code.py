return F * exp(-sig * sqrt(T) * d1 + 0.5 * sig * sig * T)

K_25c = strike_from_fwd_delta_call(S0, rd, rf, T, sig_25c, 0.25)
K_25p = strike_from_fwd_delta_put(S0, rd, rf, T, sig_25p, 0.25)
K_ATM = F0

P_stickyK = price_with_smile(S1, F1, sigma_smile_0, K_track)

K1_25c = strike_from_fwd_delta_call(S1, rd, rf, T, sig_25c, 0.25)
K1_25p = strike_from_fwd_delta_put(S1, rd, rf, T, sig_25p, 0.25)
K1_ATM = F1
sigma_smile_1 = build_smile_interp(
    F1,
    [K1_25p, K1_ATM, K1_25c],
    [sig_25p, sig_ATM, sig_25c],
)
