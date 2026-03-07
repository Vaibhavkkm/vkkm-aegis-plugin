# Skill: Options Theory (Black-Scholes & Greeks)
# VKKM Aegis — Always-Active Skill (auto-apply when relevant)
# Version: 2.0

## Rule

Automatically apply these models whenever the user's situation involves:
- Options pricing or valuation
- Options portfolio risk management
- Derivatives P&L sensitivity
- Treasury hedging with options
- Any question about Delta hedging, implied volatility, or time decay

Always label outputs as ILLUSTRATIVE ESTIMATE unless live implied volatility
is connected via FactSet or MSCI.

---

## Black-Scholes Model (1973)

### Core Formula — European Options:

```
Given inputs:
  S  = Current asset price (spot price)
  K  = Strike price
  T  = Time to expiry in YEARS (days/365)
  r  = Risk-free rate (annualised, as decimal — e.g. 3% = 0.03)
  σ  = Implied volatility (annualised, as decimal — e.g. 20% = 0.20)

Intermediate calculations:
  d1 = [ln(S/K) + (r + σ²/2) × T] / (σ × √T)
  d2 = d1 − σ × √T

Option prices:
  Call price  = S × N(d1) − K × e^(−rT) × N(d2)
  Put price   = K × e^(−rT) × N(−d2) − S × N(d1) − 1)

Where:
  N()  = Cumulative standard normal distribution (Φ)
  N'() = Standard normal probability density function
         N'(x) = (1/√2π) × e^(−x²/2)
  e^() = Natural exponential function
```

---

## The Five Greeks — Full Formulas

### Delta (Δ) — Price Sensitivity to Underlying

```
Call Delta: Δ = N(d1)            → always between 0 and +1
Put Delta:  Δ = N(d1) − 1        → always between −1 and 0

Plain-language:
  Delta = option price change per €1/$1 move in the underlying.
  Delta ≈ probability the option expires in-the-money (approximate).
  Delta = 0.5 → ATM (at-the-money) option.
  Delta → 1.0 → deep ITM; Delta → 0 → deep OTM.
```

### Gamma (Γ) — Delta Sensitivity (Convexity)

```
Gamma (same for calls and puts):
  Γ = N'(d1) / (S × σ × √T)

Plain-language:
  Gamma tells you how much Delta changes per €1 move in the underlying.
  High Gamma = Delta changes rapidly → harder to hedge.
  Gamma is highest for ATM options near expiry (most convexity, most risk).
  Long options → positive Gamma (position benefits from large moves).
  Short options → negative Gamma (dangerous in volatile markets).
```

### Vega (ν) — Volatility Sensitivity

```
Vega (same for calls and puts):
  ν = S × N'(d1) × √T

Market convention: divide by 100 for PnL per 1% vol change.

Plain-language:
  Vega = option price change per 1% move in implied volatility.
  High Vega → position is very sensitive to volatility changes (vol risk).
  Long options → positive Vega (benefit if vol rises).
  Short options → negative Vega (hurt if vol spikes — short gamma/vega).
  Vega is largest for long-dated, ATM options.
```

### Theta (Θ) — Time Decay

```
Call Theta:
  Θ = −(S × N'(d1) × σ) / (2√T) − r × K × e^(−rT) × N(d2)

Put Theta:
  Θ = −(S × N'(d1) × σ) / (2√T) + r × K × e^(−rT) × N(−d2)

Market convention: divide by 365 for daily time decay in currency.

Plain-language:
  Theta = daily cost of holding an option (time decay).
  Long options → negative Theta (you pay time decay every day).
  Short options → positive Theta (you collect time decay — the "seller's edge").
  Theta accelerates as expiry approaches → most dangerous for OTM buyers.
  OTM call expiring in 30 days loses value RAPIDLY — model this always.
```

### Rho (ρ) — Interest Rate Sensitivity

```
Call Rho:  ρ = K × T × e^(−rT) × N(d2)    ÷ 100 for per 1% rate change
Put Rho:   ρ = −K × T × e^(−rT) × N(−d2)

Plain-language:
  Rho = option price change per 1% move in the risk-free interest rate.
  Calls: positive Rho (benefit from rate rises — higher cost of carry).
  Puts: negative Rho (hurt by rate rises).
  Rho is generally the least important Greek for short-dated options.
  More important for long-dated LEAPS and rate-sensitive underlyings.
```

---

## Standard Normal Distribution Reference

For manual calculation:

| d value | N(d) | N'(d) |
|---------|------|-------|
| −2.00 | 0.0228 | 0.0540 |
| −1.50 | 0.0668 | 0.1295 |
| −1.00 | 0.1587 | 0.2420 |
| −0.80 | 0.2119 | 0.2897 |
| −0.50 | 0.3085 | 0.3521 |
|  0.00 | 0.5000 | 0.3989 |
| +0.50 | 0.6915 | 0.3521 |
| +1.00 | 0.8413 | 0.2420 |
| +1.50 | 0.9332 | 0.1295 |
| +2.00 | 0.9772 | 0.0540 |

---

## Key Options Concepts (Auto-Define on First Use)

- **ITM (In-the-Money):** Call with S > K, or Put with S < K → has intrinsic value
- **OTM (Out-of-the-Money):** Call with S < K, or Put with S > K → only time value
- **ATM (At-the-Money):** S ≈ K → maximum time value and Gamma
- **Intrinsic Value:** For calls = max(S−K, 0); For puts = max(K−S, 0)
- **Time Value:** Option price − intrinsic value. Diminishes to zero at expiry.
- **Implied Volatility (IV):** The market's expectation of future volatility — derived by solving Black-Scholes backwards from the market price.
- **Put-Call Parity:** C − P = S × e^(−qT) − K × e^(−rT) — must hold for European options without arbitrage.
- **Volatility Smile / Skew:** Markets price OTM puts at higher IV than ATM — Black-Scholes does not account for this.

---

## Black-Scholes Limitations (Always Note)

1. **Constant volatility assumed** — real markets have volatility smile/skew. Black-Scholes underprices tail risk.
2. **European exercise only** — American options require Binomial or BAW models.
3. **No dividends** — standard BS. Merton model needed for dividend-paying underlyings.
4. **Continuous trading assumed** — real markets have gaps, circuit breakers.
5. **Log-normal returns assumed** — real returns are fat-tailed (leptokurtic).

---

## Hard Rules for Options Outputs

1. Always show d1 and d2 calculations explicitly — never jump to the Greeks.
2. Present Theta as a per-day figure (divide formula output by 365).
3. Present Vega as a per-1% vol move figure (divide formula output by 100).
4. Always note if Black-Scholes is appropriate (European, no dividend) or if a different model is needed.
5. Never recommend a trade — describe position risk analytically only.
6. For OTM options near expiry: always flag Theta as the dominant risk.
7. Delta can be used as an approximate ITM probability — note this is an approximation.
