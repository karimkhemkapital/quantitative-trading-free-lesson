Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# FX Smile Dynamics From Delta Space To Sticky Strike Vs Sticky Delta

now, the important point is not to read this code as "a small tool to play around with an FX smile." here, each function holds one precise piece of market mechanics. if you get one convention wrong, you do not get it wrong "a little bit." you change the strike corresponding to a quote, which means you change the surface, which means you change the price, which means you change the hedge.

the first block, `fx_forward`, sets the right numeraire immediately

$$
F(0,T) = S_0 e^{(r_d-r_f)T}
$$

it looks basic, but in FX this is really the starting point. the forward is not some accessory of the model. it is spot carried by the rate differential. so as soon as you work in delta, moneyness, ATM, or smile interpolation, you always come back to it.

then `gk_d1d2`, `gk_call`, and `gk_put` are just Garman-Kohlhagen written cleanly. nothing exotic there. but you have to see what the code is saying: the spot term is multiplied by \(e^{-r_fT}\), the strike term by \(e^{-r_dT}\). in other words, the code keeps exactly the reading "foreign as dividend yield." if you lose that, you fall back into a fake equity Black-Scholes pasted onto FX, and you are already pricing with the wrong currency in your head.

the deltas then are not there just to make things "more complete." they are there because in FX the quote itself depends on the delta convention.

$$
\Delta^{\mathrm{call}}_{\mathrm{spot}} = e^{-r_fT}N(d_1)
$$

`delta_spot_call` codes this.

$$
\Delta^{\mathrm{call}}_{\mathrm{fwd}} = N(d_1)
$$

`delta_fwd_call` codes this.

that is exactly where the FX trap lives. a "25-delta call" is not a strike. it is a condition on \(d_1\), which means a condition that depends on the chosen convention. if you change the convention, you change the strike associated with the quote, even if the vol displayed on the ticket looks like it is "the same."

that is why the two functions `strike_from_fwd_delta_call` and `strike_from_fwd_delta_put` are the real bridge of the code. they take a delta quote, which is a market object, and transform it into a strike, which is a model object you can actually price with. for the forward-delta call, you impose

$$
N(d_1)=\Delta
$$

so

$$
d_1 = N^{-1}(\Delta)
$$

then you rewrite

$$
d_1 =
\frac{\ln(F/K)+\frac{1}{2}\sigma^2T}{\sigma\sqrt{T}}
$$

and isolate \(K\)

$$
K = F\exp\left(-\sigma\sqrt{T}d_1+\frac{1}{2}\sigma^2T\right)
$$

that is exactly what this line does

```python
return F * exp(-sig * sqrt(T) * d1 + 0.5 * sig * sig * T)
```

the put does the same thing, but with the sign convention of put delta. and that is where you need to stay mentally clean: a market "25-delta put" often means "put with absolute delta 0.25," while the true put delta is negative. so `strike_from_fwd_delta_put` is not a redundancy. it is the correct translation of a desk quote into a model strike.

then `sig_25c` and `sig_25p` reconstruct the wings from ATM, RR, and BF

$$
\sigma_{25c} = \sigma_{\mathrm{ATM}} + BF25 + \frac{1}{2}RR25
$$

$$
\sigma_{25p} = \sigma_{\mathrm{ATM}} + BF25 - \frac{1}{2}RR25
$$

that is the core of FX market language. you do not build the smile by setting ten arbitrary strikes. you start from the three numbers the desk actually quotes, then map them back into strikes through the delta convention.

when you do

```python
K_25c = strike_from_fwd_delta_call(S0, rd, rf, T, sig_25c, 0.25)
K_25p = strike_from_fwd_delta_put(S0, rd, rf, T, sig_25p, 0.25)
K_ATM = F0
```

you are building the three anchors of the one-maturity smile. one put wing, one ATM, one call wing. then `build_smile_interp` takes those three points and constructs a function \(\sigma(K)\) by interpolating in log-moneyness

$$
k = \ln(K/F)
$$

that too is the right space to work in, because in FX the forward moves with carry and with spot, so if you interpolate directly in raw strike, you can quickly lose the relative reading of the smile.

the small subtlety in the code is here: `build_smile_interp(F, K_pts, sig_pts)` "locks" the forward \(F\) inside the function `sigma_of_K`. so later when you call `price_with_smile(S, F, sigma_smile, K)`, in reality \(F\) is not directly used inside that function. it was already absorbed when building `sigma_smile`. in other words, the surface is not just "a list of vols." it is already a smile anchored relative to a given forward.

and that is exactly why the sticky strike versus sticky delta test has real content.

in the sticky strike case, you keep the same function \(\sigma(K)\) in strike space. so when spot moves, your booked strike \(K_{\mathrm{track}}\) keeps the same vol. the price changes because spot moved, not because the strike vol moved. that is what this does

```python
P_stickyK = price_with_smile(S1, F1, sigma_smile_0, K_track)
```

you price with the new spot \(S_1\), but the old smile anchored on the old strikes.

in the sticky delta case, you do something else. you say: the market quotes in delta have not changed. so the \(25\Delta\) call remains the same vol quote, the \(25\Delta\) put remains the same vol quote, the ATM remains the same ATM quote. but since spot has moved, the strikes corresponding to those deltas are no longer the same. so you rebuild a new smile in strike space from the same delta quotes, but with the new forward \(F_1\). that is what these lines do

```python
K1_25c = strike_from_fwd_delta_call(S1, rd, rf, T, sig_25c, 0.25)
K1_25p = strike_from_fwd_delta_put(S1, rd, rf, T, sig_25p, 0.25)
K1_ATM = F1
sigma_smile_1 = build_smile_interp(
    F1,
    [K1_25p, K1_ATM, K1_25c],
    [sig_25p, sig_ATM, sig_25c],
)
```

and then you price the same booked option, meaning the same fixed strike \(K_{\mathrm{track}}\), but under a smile that has shifted in strike because it stayed fixed in delta space.

that is exactly the point of the lesson. smile move is not some vague phrase. it is a concrete price difference on a given strike when you compare two surface dynamics rules.

it puts a number on that difference. that term is the part of PnL that does not come from pure spot, and not from a "constant" vol either, but from the rule according to which the smile moves when spot moves. in other words: surface PnL.

the parity check at the end is not there to look nice. it simply verifies that, for a given strike, your call and put reconstructed on the smile do satisfy

$$
C - P = S_0 e^{-r_fT} - K e^{-r_dT}
$$

if that breaks, you do not have "a slightly weird smile." you have a pricing consistency problem.

what you should see in the output is fairly clean at the initial point, your trade has a price \(P_0\).

after a spot shock, sticky strike and sticky delta give two different prices.

the difference between the two is not noise. it is the materialization of the fact that your surface does not have the same dynamics under the two rules.

and in FX that point is central because the market already lives in delta buckets. so if your internal model is implicitly reasoning in sticky strike while your book, your quotes, and your risk management are read in sticky delta, you can very quickly tell yourself the wrong story about your hedge.

that is also why, in this lesson, the passage "delta -> strike" is not a technical detail. it is the real bridge between market language and model language. as long as you stay in ATM/RR/BF quotes, you are in desk world. the moment you want to price one specific option, you need to reconstruct strikes. and the moment spot moves, you need to decide whether those anchor strikes stay fixed or not. the whole smile dynamics starts there.

if you want to summarize the logic of the lesson in one line, it is almost this:

in FX, the surface is not only a function of \((K,T)\); in actual market practice, it is first organized in \((\Delta,T)\), and the whole dynamic difficulty comes from the fact that a fixed strike does not have a fixed delta when spot moves.
