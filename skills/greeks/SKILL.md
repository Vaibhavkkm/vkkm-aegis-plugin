---
description: Command Spec: `/vkkm:greeks`
---

# Command Spec: `/vkkm:greeks`
# VKKM Aegis — Black-Scholes Options Greeks Calculator
# Version: 2.0 | Reliability: 9/10
# Exact formula — fully deterministic given the inputs.

---

## Overview

**Purpose:** Calculate all five option Greeks for any European call or put option
using the Black-Scholes model. Tells options traders and risk managers exactly how
their option position will change in value as market conditions shift.

**Who uses this:** Options traders, derivatives risk managers, treasury teams,
and finance students learning options pricing theory.

**Model source:** Fischer Black & Myron Scholes (1973). The foundation of
modern options pricing, used by every major bank and exchange globally.

---

## Behavior

### Step 1 — Collect inputs

Ask the user for these five parameters:

| Parameter | Symbol | Description | Example |
|-----------|--------|-------------|---------|
| Current asset price | S | Spot price of the underlying | €100 |
| Strike price | K | Price at which the option can be exercised | €105 |
| Time to expiry | T | Days until expiry (convert to years: T/365) | 30 days |
| Risk-free rate | r | Annualised risk-free rate (as decimal) | 3% → 0.03 |
| Implied volatility | σ | Annualised implied vol (as decimal) | 20% → 0.20 |

Also ask: **Call or Put?**

### Step 2 — Calculate intermediate values (d1 and d2)

Show both calculations explicitly:

```
d1 = [ln(S/K) + (r + σ²/2) × T] / (σ × √T)

d2 = d1 − σ × √T
```

Where:
- `ln()` = natural logarithm
- `N()` = cumulative standard normal distribution (CDF)
- `N'()` = standard normal probability density function (PDF)

### Step 3 — Calculate all 5 Greeks

Show each formula used, then the result:

```
Delta (Δ) — sensitivity to underlying price change:
  Call: N(d1)
  Put:  N(d1) − 1

Gamma (Γ) — rate of change of Delta:
  Both: N'(d1) / (S × σ × √T)
  (Same for calls and puts)

Vega (ν) — sensitivity to volatility change:
  Both: S × N'(d1) × √T
  Per 1% vol change: divide by 100

Theta (Θ) — time decay per day:
  Call: −(S × N'(d1) × σ) / (2√T) − r × K × e^(−rT) × N(d2)
  Put:  −(S × N'(d1) × σ) / (2√T) + r × K × e^(−rT) × N(−d2)
  Per day: divide by 365

Rho (ρ) — sensitivity to interest rate change:
  Call: K × T × e^(−rT) × N(d2)    per 1% rate change: divide by 100
  Put: −K × T × e^(−rT) × N(−d2)
```

### Step 4 — Plain-language interpretation

For each Greek, write one sentence in the user's specific context.
Do NOT give generic textbook definitions — make it specific to their numbers.

### Step 5 — Position risk summary

Summarise: is this option in-the-money, at-the-money, or out-of-the-money?
What is the dominant risk (usually Theta for near-expiry OTM positions)?
What is the breakeven price at expiry?

### Step 6 — Learning Note (if user appears to be a student)

### Step 7 — Append financial disclaimer and AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — BLACK-SCHOLES GREEKS
Option: European [Call/Put] | S=[price] | K=[strike] | T=[days]d | r=[rate]% | σ=[vol]%

INTERMEDIATE CALCULATIONS:
T (years) = [days]/365 = [value]

d1 = [formula result with numbers shown]
   = [rounded value]

d2 = d1 − σ×√T = [value]

N(d1) = [value]   N(d2) = [value]
N'(d1) = [value]  (standard normal PDF at d1)

GREEKS:
┌─────────┬──────────┬────────────────────────────────────────────────────┐
│ Greek   │ Value    │ Plain-Language Meaning (your specific position)    │
├─────────┼──────────┼────────────────────────────────────────────────────┤
│ Delta Δ │ [value]  │ [specific sentence about their position]           │
│ Gamma Γ │ [value]  │ [specific sentence]                                │
│ Vega ν  │ [value]  │ [specific sentence]                                │
│ Theta Θ │ [value]  │ [specific sentence — daily cost in currency]       │
│ Rho ρ   │ [value]  │ [specific sentence]                                │
└─────────┴──────────┴────────────────────────────────────────────────────┘

POSITION RISK SUMMARY:
[ITM / ATM / OTM status]
[Dominant risk factor]
[Breakeven price at expiry]

Key risks:
🔴/🟡/🟢 [Risk 1]
🔴/🟡/🟢 [Risk 2]

📚 Learning Note: [Only if student context — plain explanation of one key concept]

💰 FINANCIAL DISCLAIMER:
[Standard financial disclaimer]

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [label]
Recommended Next Action: [1 specific sentence]
— VKKM Aegis
```

---

## Hard Rules

1. **Always show d1 and d2 calculations explicitly** — never jump straight to Greeks.
2. **Always show the formula used** for each Greek before the result.
3. **Interpret each Greek in context** — use the user's actual numbers, not generic text.
4. **Convert Theta to a daily figure** (divide by 365) — this is the most intuitive for traders.
5. **Convert Vega to per-1% vol move** (divide by 100) — standard market convention.
6. **Black-Scholes assumes European exercise** — always note this. American options require different pricing (Binomial/BAW).
7. **Always label as ILLUSTRATIVE ESTIMATE** unless live vol data is connected via FactSet/MSCI.
8. **Never recommend a trade.** Describe the position mathematically — never say "buy" or "sell."
9. **Always append Financial Disclaimer and AEGIS RISK SNAPSHOT.**

---

## Example

**Input:**
> S=€100, K=€105, T=30 days, r=3%, σ=20%, Call option

**Output:**
```
🛡️ VKKM AEGIS — BLACK-SCHOLES GREEKS
Option: European Call | S=€100 | K=€105 | T=30d | r=3% | σ=20%
📊 ILLUSTRATIVE ESTIMATE — No live vol connector active. Inputs are user-provided.

INTERMEDIATE CALCULATIONS:
T (years) = 30/365 = 0.08219

d1 = [ln(100/105) + (0.03 + 0.04/2) × 0.08219] / (0.20 × √0.08219)
   = [−0.04879 + 0.04 × 0.08219] / (0.20 × 0.28669)
   = [−0.04879 + 0.00329] / 0.05734
   = −0.04550 / 0.05734
   = −0.7937

d2 = −0.7937 − 0.05734 = −0.8510

N(d1)  = N(−0.7937) = 0.2137
N(d2)  = N(−0.8510) = 0.1974
N'(d1) = 0.2892 (standard normal PDF at d1 = −0.7937)

GREEKS:
┌─────────┬──────────┬────────────────────────────────────────────────────────┐
│ Greek   │ Value    │ Plain-Language Meaning (your position)                 │
├─────────┼──────────┼────────────────────────────────────────────────────────┤
│ Delta Δ │ +0.214   │ If €AAPL rises €1, your call gains ~€0.214 in value   │
│ Gamma Γ │ +0.0534  │ If the stock rises €1, Delta itself increases by 0.053│
│ Vega ν  │ +4.81    │ If implied vol rises 1%, the call gains ~€0.048       │
│ Theta Θ │ −€0.053  │ You lose ~€0.053 per calendar day just from time decay │
│ Rho ρ   │ +€0.175  │ If rates rise 1%, the call gains ~€0.00175            │
└─────────┴──────────┴────────────────────────────────────────────────────────┘

POSITION RISK SUMMARY:
Status: Out-of-the-money (OTM) — the stock must rise 5% just to reach the strike,
with only 30 days remaining. The probability of finishing in-the-money is ~21%
(Delta as a probability approximation).

Dominant risk: 🔴 Theta (time decay)
  At −€0.053/day, you will lose approximately €1.59 in time value over 30 days
  even if the stock price stays completely flat. This is the primary risk to manage.

Breakeven at expiry: €105 + option premium paid
  (e.g. if you paid €1.50 for this call, breakeven is €106.50 — a 6.5% move required)

Key risks:
🔴 Time decay is aggressive — OTM options lose value rapidly as expiry approaches
🟡 Low Delta (0.214) — small upside leverage unless the stock moves sharply
🟢 Vega works in your favour only if implied volatility rises before expiry

📚 Learning Note:
Delta has a dual interpretation: (1) the rate of change of option price per €1 move
in the underlying, and (2) roughly the probability the option expires in-the-money.
Delta = 0.214 means approximately a 21% chance of this call being profitable at expiry
— useful as a quick sanity check on your position.

💰 FINANCIAL DISCLAIMER:
Black-Scholes assumes constant volatility (no volatility smile/skew), European-style
exercise only, no dividends, and continuous trading. Real markets deviate from all of
these assumptions. Greeks are instantaneous measures — they change as the market moves
(hence Gamma). This analysis is educational only — not trading advice.
Always consult a qualified financial professional before trading derivatives.

📊 AEGIS RISK SNAPSHOT
Likelihood: 4/5 — OTM with 30 days to expiry: statistically ~79% probability of
             expiring worthless based on current model parameters
Impact: 3/5 — Maximum loss is capped at premium paid; known and bounded downside
Risk Score: 12/25 — 🟠 High
Recommended Next Action: Evaluate whether a 5%+ move in the underlying is realistic
within the 30-day window — if not, consider a longer-dated or lower-strike alternative.
— VKKM Aegis
```

---

*Part of VKKM Aegis v5.0.0 — Advanced Finance Risk Management Plugin*
*Model: Black-Scholes (1973) | Greeks: standard derivatives thereof*
