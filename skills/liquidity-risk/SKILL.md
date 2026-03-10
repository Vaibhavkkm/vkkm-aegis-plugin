---
description: Command Spec: `/vkkm:liquidity-risk`
---

# Command Spec: `/vkkm:liquidity-risk`
# VKKM Aegis — Liquidity Risk & Cash Flow Gap Analysis
# Version: 2.0 | Reliability: 8/10
# LCR / NSFR / cash runway analysis — Basel III liquidity framework.

---

## Overview

**Purpose:** Analyse whether an entity has sufficient liquid assets and cash flows
to meet its obligations under both normal and stressed conditions. Covers both
Basel III regulatory liquidity ratios (for financial institutions) and practical
cash runway / gap analysis for all companies.

**Who uses this:** CFOs, treasury teams, auditors, regulators, and investors
assessing whether a company or bank can meet its near-term obligations.

---

## Behavior

### Step 1 — Collect inputs

Accept any of these formats:
- Verbal description of the company's financial position
- Pasted financial data (cash balance, inflows, outflows)
- Uploaded cash flow statement or treasury report

Minimum required inputs:
| Input | Description |
|-------|------------|
| Cash balance | Current cash and cash equivalents |
| Monthly operating inflows | Revenue receipts, expected payments in |
| Monthly operating outflows | Payroll, rent, COGS, debt service |
| Liquid assets (HQLA) | High-quality assets that can be sold in 30 days |
| Debt maturity schedule | When loans / bonds mature |
| Top 5 revenue sources (%) | To assess funding concentration |

For banks / financial institutions — also ask:
- Net cash outflows over next 30 days (stressed)
- Available stable funding sources
- Required stable funding

### Step 2 — Cash Runway Calculation

```
Cash Runway (months) = Cash Balance / Monthly Net Burn Rate
Monthly Net Burn       = Monthly Outflows − Monthly Inflows

Rating thresholds:
  > 18 months  → 🟢 Green (strong)
  12–18 months → 🟡 Amber (adequate)
  6–12 months  → 🟠 Warning (concerning)
  < 6 months   → 🔴 Red (critical)
```

### Step 3 — 12-Month Cash Flow Gap Table

Build month-by-month projection:
```
Gap(t) = Cumulative balance at time t
       = Opening balance + Σ (Inflows − Outflows)_1..t

Flag: Any month where cumulative gap goes negative = liquidity shortfall.
Flag: Three consecutive months of net outflows = deteriorating trend.
```

### Step 4 — LCR Calculation (for banks / regulated entities)

```
LCR = HQLA / Net Cash Outflows (30-day stressed scenario)

Where:
  HQLA (High Quality Liquid Assets) = Level 1 (cash, central bank reserves) +
    Level 2A (government bonds, ≤15% haircut) +
    Level 2B (corporate bonds, ≤50% haircut)
  Net Cash Outflows = Total outflows − min(inflows, 75% of total outflows)

Regulatory minimum: LCR ≥ 100%
```

### Step 5 — NSFR Calculation (for banks)

```
NSFR = Available Stable Funding (ASF) / Required Stable Funding (RSF)

ASF = capital + long-term deposits/borrowings × stability factors
RSF = assets × liquidity weighting factors

Regulatory minimum: NSFR ≥ 100%
```

### Step 6 — Funding Concentration Analysis

Flag any single funding source >25% of total revenue or funding as concentration risk.

### Step 7 — Identify earliest shortfall date and recommend mitigations

### Step 8 — Append financial disclaimer and AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — LIQUIDITY RISK ANALYSIS
Entity: [name/type] | Date: [today]
[📊 ILLUSTRATIVE ESTIMATE / 📊 DATA-GROUNDED]

CASH RUNWAY:
Cash Balance:  [amount]
Monthly Burn:  [amount]
Runway:        [X] months — [🔴/🟠/🟡/🟢 status]

[LCR ANALYSIS — if banking entity:]
HQLA:                [amount]
Net Cash Outflows:   [amount] (30-day stressed)
LCR:                 [X%] — [🔴 BELOW / 🟢 ABOVE] 100% minimum

[NSFR ANALYSIS — if banking entity:]
Available Stable Funding:  [amount]
Required Stable Funding:   [amount]
NSFR:                      [X%] — [🔴 BELOW / 🟢 ABOVE] 100% minimum

CASH FLOW GAP (12-month projection):
| Month | Inflows | Outflows | Net | Cumulative |
|-------|---------|----------|-----|------------|
| M1  | [amount] | [amount] | [+/-] | [amount] |
| M2  | ... | | | |
[Continue through M12]

[⚠️ RISK FLAGS — highlight months with negative net or consecutive outflows]

FUNDING CONCENTRATION:
| Source | % of Revenue/Funding | Risk |
|--------|---------------------|------|
[Top sources listed]

[⚠️ Flag any source > 25%]

EARLIEST SHORTFALL DATE: [Month X / None in 12-month horizon]

RECOMMENDATIONS:
1. [Specific action]
2. [Second action]
3. [Third action]

💰 FINANCIAL DISCLAIMER:
[Standard financial disclaimer]

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [label]
Recommended Next Action: [1 sentence]
— VKKM Aegis
```

---

## Hard Rules

1. **Always calculate cash runway first** — it's the most intuitive metric for any stakeholder.
2. **Flag any month with negative cumulative cash** — this is a hard liquidity event.
3. **Flag funding concentration** if any single source > 25% of revenue/funding.
4. **NSFR and LCR** are mandatory for banking entities — skip for non-financial companies.
5. **For LCR < 100%** → always recommend immediate remediation actions. This is a regulatory breach.
6. **Never project inflows without noting the revenue quality** — secured vs. expected vs. speculative.
7. **Always note the key assumption** behind your 12-month projection (flat revenue, contractual inflows, etc.)
8. **Always append Financial Disclaimer and AEGIS RISK SNAPSHOT.**

---

## Example

**Input:**
> Company: SaaS startup | Cash: €500K | Monthly burn: €85K
> Inflows: M1-M2 €120K/mo, M3-M5 €80K/mo, M6 €200K (renewal)
> Top client: 42% of revenue | No banking entity

**Output:**
```
🛡️ VKKM AEGIS — LIQUIDITY RISK ANALYSIS
Entity: SaaS Startup | Date: 2026-03-06
📊 ILLUSTRATIVE ESTIMATE — Based on user-provided figures and stated assumptions.

CASH RUNWAY:
Cash Balance:  €500,000
Monthly Burn:  €85,000 (gross outflows) − avg inflows
Net Burn:      Variable — see cash flow gap table
Runway:        5.9 months at current burn — 🔴 CRITICAL (below 6-month minimum threshold)

CASH FLOW GAP (12-month projection):
Assumptions: M1-M2 inflows €120K (strong contract month), M3-M5 drop to €80K
(softer pipeline), M6 €200K (renewal collection), remaining months held at €100K avg.

| Month | Inflows | Outflows | Net     | Cumulative |
|-------|---------|----------|---------|------------|
| M1    | €120,000 | €85,000 | +€35,000 | €535,000  |
| M2    | €120,000 | €85,000 | +€35,000 | €570,000  |
| M3    | €80,000  | €120,000 | −€40,000 | €530,000  |
| M4    | €80,000  | €120,000 | −€40,000 | €490,000  |
| M5    | €80,000  | €85,000  | −€5,000  | €485,000  |
| M6    | €200,000 | €85,000  | +€115,000| €600,000  |
| M7    | €100,000 | €85,000  | +€15,000 | €615,000  |
| M8    | €100,000 | €85,000  | +€15,000 | €630,000  |
| M9    | €100,000 | €90,000  | +€10,000 | €640,000  |
| M10   | €100,000 | €90,000  | +€10,000 | €650,000  |
| M11   | €100,000 | €90,000  | +€10,000 | €660,000  |
| M12   | €100,000 | €90,000  | +€10,000 | €670,000  |

⚠️ RISK FLAG: M3–M5 shows three consecutive months of net outflows.
  The cumulative balance reaches a trough of €485,000 in M5.
  No shortfall breach, but the cushion is dangerously thin.
  If top client delays payment: M3 net turns to −€40K → €490K,
  and if M4 renewal is delayed by 30 days, M4 balance could fall below €400K.

FUNDING CONCENTRATION:
| Source | % of Revenue | Risk |
|--------|-------------|------|
| Top client | 42% | 🔴 CRITICAL — above 25% concentration threshold |
| Client 2 | 18% | 🟡 Watch |
| Client 3 | 12% | 🟢 Acceptable |
| Other (6 clients) | 28% | 🟢 Acceptable |

⚠️ Top client at 42% of revenue is a severe single-point-of-failure.
If top client delays payment by just 30 days, M3 shortfall risk becomes very real.
If they churn, 42% revenue loss would require halving the team within 60 days.

EARLIEST SHORTFALL DATE:
No hard shortfall in the 12-month baseline. However, any one of these events
changes the outcome:
  • Top client delays 30 days → M3 net becomes −€80K (instead of −€40K)
  • Top client churns → cash reaches zero in ~M5 without aggressive cost-cutting

RECOMMENDATIONS:
1. 🔴 Establish a €150,000 revolving credit facility before end of M2, as a
   buffer against M3–M5 outflow pressure — this is the single most important action
2. 🔴 Initiate active client diversification: top client must fall below 25%
   of revenue within 12 months — this is an existential concentration risk
3. 🟠 Renegotiate payment terms with top client — move to monthly upfront payment
   or at minimum Net-15 (currently Net-30 or Net-60?)
4. 🟡 Build a formal 6-month minimum cash reserve policy — current 5.9 months
   is borderline; 12 months is the target for a funded SaaS company

💰 FINANCIAL DISCLAIMER:
This cash flow projection is based on stated assumptions about inflows and outflows.
Actual results may differ materially if contract renewals are delayed, revenue pipeline
does not convert, or unexpected costs arise. This is not a substitute for a formal
financial model built by a qualified CFO or financial advisor.

📊 AEGIS RISK SNAPSHOT
Likelihood: 3/5 — No shortfall in baseline, but the margin is thin and top-client
             concentration makes this realistic if one event goes wrong
Impact: 5/5 — Cash exhaustion would require emergency fundraising, deep cuts,
          or insolvency — existential impact
Risk Score: 15/25 — 🔴 Critical
Recommended Next Action: Arrange revolving credit facility within 30 days — well before
M3 outflow pressure begins — this single action removes the liquidity shortfall risk.
— VKKM Aegis
```

---

*Part of VKKM Aegis v5.0.0 — Advanced Finance Risk Management Plugin*
*Framework: Basel III LCR (Article 412 CRR) / NSFR (Article 428a CRR)*
*Python MCP endpoint: POST /liquidity — see mcp_server.py*
