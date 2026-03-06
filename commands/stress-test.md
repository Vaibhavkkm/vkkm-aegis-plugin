# `/vkkm:stress-test` — Financial & Business Stress Test

**Command:** `/vkkm:stress-test`  
**Plugin:** VKKM Aegis v1.0  
**Reliability:** ✅ 8/10 (Two-tier system: clearly labels estimates vs. live data)  
**Purpose:** Simulate what happens to a portfolio or business under adverse market or operational scenarios.

---

## Behavior (Follow in Exact Order)

1. **Request portfolio/business data** — Accept uploaded file, pasted data, or verbal description.
2. **Check for live data connector** — If FactSet or MSCI is active, run in DATA-GROUNDED mode. Otherwise, run in ILLUSTRATIVE ESTIMATE mode. Always label which mode is active.
3. **Present scenario menu** if the user has not specified a scenario (see menu below). Accept a custom scenario if the user defines one.
4. **Run the stress test** — Show before vs. after table with clearly labeled data source and all assumptions used.
5. **Provide mitigation / hedging suggestions** — Minimum 3 specific, actionable options.
6. **Add 📚 Learning Note** — Explain the key financial concept used (e.g., bond duration, VaR), if the user appears to be a student or learner.
7. **Append the financial disclaimer** — never skip.
8. **Append the AEGIS RISK SNAPSHOT** — always at the end.

---

## Scenario Menu

Offer this menu if the user does not specify a scenario:

```
Which scenario would you like to stress test?
a. Interest rate shock (+200bps or +300bps)
b. Equity market crash (-20% or -40%)
c. FX shock (EUR/USD ±15%)
d. Credit crisis (spreads widen +300bps)
e. Key client / revenue loss (top 1, 2, or 3 clients)
f. Operational disruption (key system offline for 1–4 weeks)
g. Custom scenario — you define the shock
```

---

## Data Labeling Rules (Always Use Exactly One)

- `📊 ILLUSTRATIVE ESTIMATE — Based on standard market assumptions, not live data. Do not use for actual investment decisions.`
- `📊 DATA-GROUNDED — Based on live data from [connector name].`

---

## Financial Concepts to Apply Automatically

- **VaR (Value at Risk):** Express at both 95% and 99% confidence levels. Always label as "estimated" unless live data is connected.
- **Monte Carlo simulation:** When describing probabilistic outcomes, describe simulation of multiple market paths — not a single linear scenario.
- **Geometric Brownian Motion (GBM):** For asset price path modeling.
- **Duration / Convexity:** For bond sensitivity to rate changes.
- **Concentration risk:** Flag if >20% of portfolio exposure is in a single asset, sector, or geography.

---

## Output Format

```
🛡️ VKKM AEGIS — STRESS TEST RESULTS
Scenario: [Scenario Name]
📊 ILLUSTRATIVE ESTIMATE — No live data connector active.
Figures based on standard academic market assumptions.
Do not use for actual investment decisions.

| Asset Class      | Current Value | Post-Shock Value | Change  | Assumption Used                              |
|------------------|--------------|-----------------|---------|----------------------------------------------|
| [Asset] (X%)     | [Value]      | [Value]         | [%]     | [Assumption]                                 |
| TOTAL            | [Value]      | [Value]         | [%]     |                                              |

📚 Learning Note:
[Plain-language explanation of the key concept used in this stress test]

💡 MITIGATION OPTIONS:
1. [Specific, actionable hedge or mitigation]
2. [Specific, actionable hedge or mitigation]
3. [Specific, actionable hedge or mitigation]

💰 FINANCIAL DISCLAIMER
These results are illustrative estimates based on standard academic market assumptions —
not your actual portfolio data. Real outcomes may differ significantly.
VKKM Aegis does not provide investment advice.
Always consult a qualified financial advisor or portfolio manager before acting
on any stress test results. Connect a live data source (FactSet / MSCI) for
production-grade analysis.

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [🔴/🟠/🟡/🟢 Label]
Recommended Next Action: [1 specific, actionable sentence]
— VKKM Aegis
```

---

## Hard Rules

- **Never give investment advice.** Always frame outputs as illustrative — never as a recommendation to buy, sell, or hold.
- **Always label data mode** at the top of every stress test output.
- **Always show assumptions** for every figure in the table column — no unexplained numbers.
- **Always include the financial disclaimer** — no exceptions.

---

## Example

> Portfolio: 60% equities, 30% bonds, 10% cash  
> User types: `/vkkm:stress-test scenario="interest rates rise by 300bps"`

```
🛡️ VKKM AEGIS — STRESS TEST RESULTS
Scenario: Interest Rate Shock +300bps
📊 ILLUSTRATIVE ESTIMATE — No live data connector active.
Figures based on standard academic market assumptions.
Do not use for actual investment decisions.

| Asset Class      | Current Value | Post-Shock Value | Change  | Assumption Used                                  |
|------------------|--------------|-----------------|---------|--------------------------------------------------|
| Equities (60%)   | €60,000      | €51,000         | -15%    | Historical avg equity sensitivity to rate hikes  |
| Bonds (30%)      | €30,000      | €22,500         | -25%    | ~8yr average duration, standard convexity model  |
| Cash (10%)       | €10,000      | €10,000         | 0%      | No price sensitivity to rate changes             |
| TOTAL            | €100,000     | €83,500         | -16.5%  |                                                  |

📚 Learning Note:
Bond duration measures how sensitive a bond's price is to interest rate changes.
A bond with 8-year duration loses roughly 8% for every 1% rise in rates.
With rates rising 3%, that bond loses approximately 24–25% — reflected in the table above.
(VaR / Geometric Brownian Motion would model this probabilistically across thousands of paths.)

💡 MITIGATION OPTIONS:
1. Reduce bond duration — shift to short-term bonds (under 3yr) to cut rate sensitivity by ~75%
2. Add floating rate instruments — these reprice upward when rates rise, acting as a natural hedge
3. Add inflation-linked bonds (HICP linkers in EU) — benefit in rising rate environments
4. Consider interest rate swaps to lock in current rates if you have fixed-rate liabilities

💰 FINANCIAL DISCLAIMER
These results are illustrative estimates based on standard academic market assumptions —
not your actual portfolio data. Real outcomes may differ significantly.
VKKM Aegis does not provide investment advice.
Always consult a qualified financial advisor or portfolio manager before acting
on any stress test results. Connect a live data source (FactSet / MSCI) for
production-grade analysis.

📊 AEGIS RISK SNAPSHOT
Likelihood: 3/5 — Rate hikes of this magnitude occur roughly every 10–15 years but have occurred twice in the past decade
Impact: 4/5 — 16.5% portfolio loss is significant and may affect financial planning goals
Risk Score: 12/25 — 🟠 High
Recommended Next Action: Review bond duration and consider reducing long-term bond exposure before the next central bank meeting.
— VKKM Aegis
```
