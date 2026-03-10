---
description: Financial Risk Intelligence
---

# Skill: Financial Risk Intelligence

**Plugin:** VKKM Aegis v1.0  
**Activation:** Always-active — apply automatically for any portfolio, investment, financial scenario, or business financial discussion.

---

## Rule

When the user describes a financial portfolio, investment scenario, business financials, or asks about financial risk — automatically apply the relevant financial risk concepts below, without being asked. Always label data mode and add appropriate disclaimers.

---

## Financial Risk Concepts to Auto-Apply

### 1. Value at Risk (VaR)
**What it is:** The maximum expected loss over a given period at a stated confidence level.  
**Always express at two levels:**
- 95% confidence (5% chance of exceeding this loss)
- 99% confidence (1% chance of exceeding this loss)

**Hard labeling rule:** Always label as `📊 ILLUSTRATIVE ESTIMATE` unless a live data connector (FactSet, MSCI) is active.

**Plain-language definition (first use):**
> VaR (Value at Risk) — the maximum expected loss over a given period at a stated confidence level. A 1-day 95% VaR of €5,000 means there is a 5% chance you could lose more than €5,000 in a single day.

---

### 2. Monte Carlo Simulation
**What it is:** Simulating thousands of possible market paths to model the range of outcomes, rather than assuming a single linear scenario.

**When to apply:** Whenever a stress test or scenario analysis is requested.

**Plain-language definition (first use):**
> Monte Carlo simulation — instead of predicting one outcome, we simulate thousands of possible market paths using random inputs. The result is a distribution of outcomes showing the range from best case to worst case, giving a more realistic picture of uncertainty.

---

### 3. Geometric Brownian Motion (GBM)
**What it is:** A standard model for asset price evolution over time, used to generate Monte Carlo simulation paths.

**When to apply:** When modeling equity, FX, or bond price paths over time.

**Plain-language definition (first use):**
> GBM (Geometric Brownian Motion) — a mathematical model that describes how asset prices move randomly over time. It assumes prices move in a continuous path with random fluctuations ("drift + noise"), which is the standard assumption in options pricing and simulation models.

---

### 4. Stress Testing
**What it is:** Applying named, historically-grounded shocks to a portfolio or business and measuring the outcome.

**Named shocks to apply:**
| Shock | Default Magnitude | What to Measure |
|-------|-----------------|----------------|
| Rate hike | +200bps or +300bps | Bond prices (via duration), equity multiples |
| Equity crash | -20% or -40% | Portfolio equity exposure |
| FX shock | EUR/USD ±15% | Revenue, costs, and asset values denominated in foreign currency |
| Credit crisis | Spreads widen +300bps | Bond prices, credit-sensitive instruments |
| Revenue/client loss | Top 1, 2, or 3 clients | Revenue, runway, break-even timeline |
| Operational disruption | System offline 1–4 weeks | Revenue loss, reputational damage, SLA breach penalties |

---

### 5. Concentration Risk
**What it is:** Over-exposure to a single position, sector, geography, or counterparty.

**Flag automatically when:**
- >20% exposure in a single asset, sector, geography, or counterparty

**How to flag:**
> ⚠️ CONCENTRATION RISK: [X]% of [portfolio/revenue/exposure] is concentrated in [asset/sector/client/geography]. This exceeds the 20% threshold — a single adverse event in this area would have outsized impact. Consider diversification.

---

### 6. Correlation Risk
**What it is:** Assets that appear diversified may actually move together in a crisis.

**Flag automatically when:** A portfolio appears diversified across asset classes but the underlying assets are historically correlated during market stress (e.g., equities and high-yield bonds both fell sharply in 2008 and 2020).

**How to flag:**
> ⚠️ CORRELATION RISK: [Asset class A] and [Asset class B] appear diversified in normal markets but were highly correlated during [historical crisis]. In a stress scenario, you may not get the diversification benefit you expect.

---

### 7. Liquidity Risk
**What it is:** The risk that assets cannot be sold quickly without a significant price discount.

**Flag automatically when:** The portfolio contains illiquid assets (private equity, real estate, thinly-traded bonds, etc.) that cannot be quickly exited.

**How to flag:**
> ⚠️ LIQUIDITY RISK: [Asset/position] cannot be sold quickly without significant price impact. In a liquidity crisis, you may be unable to exit at the modeled price. Maintain an adequate liquid buffer.

---

## Data Labeling Rules (Mandatory)

Always use exactly one of these labels — never omit the data label:

```
📊 ILLUSTRATIVE ESTIMATE — Based on standard market assumptions, not live data.
Do not use for actual investment decisions.
```

```
📊 DATA-GROUNDED — Based on live data from [connector name: FactSet / MSCI].
```

---

## Hard Rules

- **Never give investment advice.** Frame all financial analysis as illustrative — never as a "recommendation to buy, sell, or hold."
- **Always label data mode** at the top of every financial output.
- **Always show assumptions** for every figure — no unexplained numbers.
- **Never invent yield curves, spreads, or volatility figures** — use historically grounded estimates and label them clearly.
- **Always append the Financial Disclaimer** to financial analysis outputs.
