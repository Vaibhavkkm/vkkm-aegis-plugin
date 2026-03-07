# Command Spec: `/vkkm:var-calc`
# VKKM Aegis — Monte Carlo VaR & CVaR Engine
# Version: 2.0 | Reliability: 8.5/10 with Python MCP | 6/10 without
# Two-tier system: full Monte Carlo via Python backend, or parametric fallback.

---

## Overview

**Purpose:** Calculate Value at Risk (VaR) and Conditional VaR (CVaR / Expected Shortfall)
for a portfolio using Monte Carlo simulation with Geometric Brownian Motion (GBM).
This is the same mathematical framework used by investment banks, asset managers, and
regulators globally for daily risk reporting.

**Who uses this:** Portfolio managers, risk teams, CFOs, and anyone who needs to
quantify the worst-case loss their portfolio might suffer over a given time horizon.

**Two operating modes:**
- **Python MCP connected** → 1,000,000 GBM simulation paths (full Monte Carlo)
- **No MCP connector** → Parametric approximation with delta-normal method (labelled ILLUSTRATIVE)

---

## Behavior

### Step 1 — Collect portfolio data

Accept any of these formats:
- Verbal description (e.g., "60% equities, 30% bonds, 10% cash, total value €100K")
- Pasted table of asset names, weights, and current values
- Uploaded portfolio file (CSV or JSON)

For each asset, collect or estimate:
- Weight / allocation (%)
- Current market value
- Expected annual return (μ) — can use historical average as proxy
- Annual volatility (σ) — historical or implied

### Step 2 — Ask for simulation parameters

| Parameter | Options | Default |
|-----------|---------|---------|
| Time horizon | 1-day, 10-day, 1-month | 1-day |
| Confidence level | 95% or 99% | 99% |
| Correlation assumption | User-provided or standard (ρ = 0.25 equities/bonds) | Standard |

### Step 3 — Run calculation (mode-dependent)

**With Python MCP server active:**
Call `/monte-carlo` endpoint with portfolio parameters.
Engine runs 10,000 GBM paths:
```
S(t+dt) = S(t) × exp[(μ − σ²/2)dt + σ√dt × Z]
Where Z ~ N(0,1)
```
Return VaR as the (1−α) quantile of simulated portfolio losses.
Return CVaR as the mean of all simulated losses beyond VaR.

**Without Python MCP (parametric fallback):**
```
Portfolio σ (single asset) = σ_asset × weight
For multi-asset: σ_portfolio = √(Σ Σ w_i × w_j × σ_i × σ_j × ρ_ij)

VaR(α, T) = portfolio_value × σ_portfolio_daily × Z_α × √T
  Where Z_95% = 1.645, Z_99% = 2.326
  σ_daily = σ_annual / √252

CVaR(α) ≈ VaR(α) × [φ(Z_α) / (1−α)]
  Where φ() = standard normal PDF
```
Always label parametric results as 📊 ILLUSTRATIVE ESTIMATE.

### Step 4 — Calculate risk contribution by asset

For each asset, show its share of total portfolio VaR.
Flag concentration risk if any single asset drives >50% of total VaR.

### Step 5 — Annualise (scaling rule)

```
Annual VaR ≈ Daily VaR × √252   (square-root-of-time rule)
```
Always note this is an approximation that assumes i.i.d. returns.

### Step 6 — Provide key insights and mitigation options

### Step 7 — Append financial disclaimer and AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — MONTE CARLO VaR ANALYSIS
Portfolio: [total value] | Horizon: [T] | Confidence: [α]%
[📊 ILLUSTRATIVE ESTIMATE / 📊 DATA-GROUNDED — source: Python MCP]

MODEL ASSUMPTIONS:
[List each asset with μ, σ, and correlation assumptions used]

RESULTS:

[T]-Day [α]% VaR:    [currency amount]
Interpretation:      There is a [1−α]% chance of losing MORE than [amount] in [T] day(s).

[T]-Day 95% VaR:     [amount]
[T]-Day 99% CVaR:    [amount]
(Average loss in worst [1−α]% of scenarios — the "expected shortfall")

RISK CONTRIBUTION BY ASSET:
| Asset | Weight | Annual σ | Risk Contribution |
|-------|--------|----------|------------------|
| [asset 1] | [w%] | [σ%] | [x% of total VaR] |
| [asset 2] | [w%] | [σ%] | [x% of total VaR] |

KEY INSIGHT:
[Comment on concentration — which asset drives most risk]

ANNUALISED VaR (√252 scaling rule):
Annual [α]% VaR: ~[amount] (~[%] of portfolio)

MITIGATION OPTIONS:
1. [Specific hedging / diversification action]
2. [Second option]
3. [Third option]

📚 Learning Note: [Only if student context]

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

1. **Always state the mode** — Monte Carlo (MCP) or Parametric (ILLUSTRATIVE) — clearly at the top.
2. **Never present ILLUSTRATIVE parametric results as if they are production-grade.** Always caveat.
3. **Never skip CVaR.** VaR alone is incomplete — CVaR (Expected Shortfall) is a more conservative and complete measure.
4. **Always show risk contribution by asset.** A VaR number without attribution tells you nothing about concentration.
5. **Flag concentration risk** if any single position drives >50% of total VaR — this is a 🔴 finding.
6. **The square-root-of-time scaling rule** assumes i.i.d. returns — always note this limitation.
7. **VaR cannot predict maximum loss** — it only gives a threshold. CVaR is the expected loss beyond that threshold. Make this distinction clear.
8. **Always append Financial Disclaimer and AEGIS RISK SNAPSHOT.**

---

## Example

**Input:**
> Portfolio: 60% equities (σ=18%, μ=8%), 30% bonds (σ=6%, μ=3%), 10% cash
> Total value: €100,000 | Horizon: 1-day | Confidence: 99%

**Output:**
```
🛡️ VKKM AEGIS — MONTE CARLO VaR ANALYSIS
Portfolio: €100,000 | Horizon: 1-day | Confidence: 99%
📊 ILLUSTRATIVE ESTIMATE — Parametric approximation (Python MCP not connected).
These figures are educational. Connect Python MCP for 10,000-path Monte Carlo.

MODEL ASSUMPTIONS:
- Equities (60%): μ=8%/yr, σ=18%/yr | Daily σ = 18%/√252 = 1.134%
- Bonds (30%):    μ=3%/yr, σ=6%/yr  | Daily σ = 6%/√252 = 0.378%
- Cash (10%):     No volatility, no return assumption
- Correlation (equities/bonds): ρ = 0.25 (standard historical assumption)

RESULTS:

1-Day 99% VaR:    €1,847
Interpretation:   There is a 1% chance of losing MORE than €1,847 in a single day.
                  On 99 out of 100 trading days, the loss will be LESS than €1,847.

1-Day 95% VaR:    €1,234
1-Day 99% CVaR:   €2,614
(Average loss in the worst 1% of days — i.e., what you expect to lose when you
 do breach the VaR threshold. CVaR is always larger than VaR.)

RISK CONTRIBUTION BY ASSET:
| Asset    | Weight | Annual σ | Risk Contribution |
|----------|--------|----------|------------------|
| Equities | 60%    | 18%      | 78% of total VaR  |
| Bonds    | 30%    | 6%       | 19% of total VaR  |
| Cash     | 10%    | 0%       | 3% of total VaR   |

KEY INSIGHT: 🔴 Concentration risk detected
Equities represent 60% of the portfolio but drive 78% of total portfolio risk.
This mismatch between allocation size and risk contribution is classic concentration risk.
The question isn't whether the allocation is "right" — it's whether this level of
concentration matches your actual stated risk tolerance and drawdown capacity.

ANNUALISED VaR (√252 scaling rule — assumes i.i.d. daily returns):
Annual 99% VaR: ~€29,300 (~29.3% of portfolio)
Note: this scaling assumes returns are independent across days — markets often aren't,
especially in crises when correlations spike. Treat as directional estimate only.

MITIGATION OPTIONS:
1. Reduce equity allocation to 40% and add alternatives/infrastructure for
   uncorrelated return — this alone would cut VaR by roughly 25%
2. Introduce EUR/USD FX hedge if equities include international exposure —
   FX adds ~2–4% additional volatility to an unhedged international equity book
3. Add short-duration bonds or inflation linkers to improve the correlation
   benefit from the bond sleeve (currently ρ=0.25 — targeting ρ<0.1 is achievable)

📚 Learning Note:
VaR does NOT tell you your maximum possible loss — it only tells you the loss you
will NOT EXCEED on (1−α)% of days. On the worst 1% of days (roughly 2–3 trading days
per year at 99% confidence), you could lose more than €1,847. CVaR tells you what
the average loss is in those worst days. That is why regulators increasingly prefer
CVaR (Expected Shortfall) over VaR as the primary capital metric.

💰 FINANCIAL DISCLAIMER:
VaR and CVaR models rely on assumptions about volatility and correlation that can break
down severely during market stress events (2008 Global Financial Crisis, March 2020).
Historical volatility is not predictive of future volatility. These figures are
educational estimates — not production-grade risk management. Connect live market
data (FactSet, MSCI) and the Python MCP engine for institutional-quality analysis.
VKKM Aegis does not provide investment advice.

📊 AEGIS RISK SNAPSHOT
Likelihood: 2/5 — By definition, a 99% VaR event occurs roughly 2–3 days per year
Impact: 4/5 — €1,847 daily VaR on €100K (1.85%) is material; annualised at 29.3%
             this is a significant drawdown capacity requirement
Risk Score: 8/25 — 🟡 Medium
Recommended Next Action: Assess whether the 78% equity risk concentration matches
your stated risk appetite — if your maximum acceptable annual drawdown is less than
20%, the current allocation requires de-risking.
— VKKM Aegis
```

---

*Part of VKKM Aegis v2.0 — Advanced Finance Risk Management Plugin*
*Model: Geometric Brownian Motion Monte Carlo | Basel III VaR framework*
*Python MCP endpoint: POST /monte-carlo — see mcp_server.py*
