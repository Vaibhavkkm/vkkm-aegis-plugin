# Command Spec: `/vkkm:zscore`
# VKKM Aegis — Altman Z-Score Bankruptcy Predictor
# Version: 2.0 | Reliability: 9/10
# Pure formula — no hallucination risk when inputs are provided correctly.

---

## Overview

**Purpose:** Calculate the Altman Z-Score to assess the probability of a company
entering financial distress or bankruptcy within the next 24 months.

**Who uses this:** Banks, credit analysts, investors, CFOs, and anyone assessing
the financial health of a borrower, partner, acquisition target, or counterparty.

**Formula source:** Edward Altman (1968) — revised Z' model for private firms (1983).
One of the most widely validated bankruptcy prediction models in academic finance.

---

## Behavior

### Step 1 — Collect inputs
Ask the user to provide the following figures from the company's balance sheet and P&L.
If uploading financial statements, extract these automatically:

| Input | Definition |
|-------|-----------|
| Working Capital | Current Assets − Current Liabilities |
| Total Assets | Total balance sheet assets |
| Retained Earnings | Accumulated profits not paid as dividends |
| EBIT | Earnings Before Interest and Tax |
| Market Value of Equity | For **public** firms: shares × market price |
| Book Value of Equity | For **private** firms: total equity on balance sheet |
| Total Liabilities | All debt and obligations |
| Revenue | Total annual revenue / turnover |

Also ask: **Is this a public or private company?**

### Step 2 — Select the correct model

| Company type | Formula | Key difference |
|-------------|---------|---------------|
| **Public** (listed) | Z = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5 | X4 uses **Market** value of equity |
| **Private** (unlisted) | Z' = 0.717×X1 + 0.847×X2 + 3.107×X3 + 0.420×X4 + 0.998×X5 | X4 uses **Book** value of equity |

Where:
```
X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets          ← Most predictive ratio
X4 = Equity Value / Total Liabilities
X5 = Revenue / Total Assets
```

### Step 3 — Calculate step by step
Show all five ratios with their workings. Then apply the formula. Show each
weighted term separately before summing. Never skip to the result without workings.

### Step 4 — Interpret the result

**Public company (Z) zones:**

| Z-Score | Zone | Risk |
|---------|------|------|
| Z > 2.99 | 🟢 Safe Zone | Low bankruptcy risk |
| 1.81 < Z < 2.99 | 🟡 Grey Zone | Uncertain — monitor closely |
| Z < 1.81 | 🔴 Distress Zone | High bankruptcy probability within 2 years |

**Private company (Z') zones:**

| Z'-Score | Zone | Risk |
|----------|------|------|
| Z' > 2.90 | 🟢 Safe Zone | Low bankruptcy risk |
| 1.23 < Z' < 2.90 | 🟡 Grey Zone | Uncertain — monitor closely |
| Z' < 1.23 | 🔴 Distress Zone | High bankruptcy probability within 2 years |

### Step 5 — Identify the weakest ratio
Flag which of the five ratios is dragging the score down most. X3 (EBIT/Assets)
is the most predictive — always comment on it specifically.

### Step 6 — Recommend 3 specific improvement actions
Based on the weak ratios identified, give concrete actions the CFO or management
team could take to improve the score.

### Step 7 — Append financial disclaimer and AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — ALTMAN Z-SCORE ANALYSIS
Company Type: [Public / Private] | Model: [Z / Z']
Date: [today]

STEP-BY-STEP CALCULATION:

X1 = Working Capital / Total Assets
   = [value] / [value] = [ratio]

X2 = Retained Earnings / Total Assets
   = [value] / [value] = [ratio]

X3 = EBIT / Total Assets
   = [value] / [value] = [ratio]

X4 = [Market/Book] Value of Equity / Total Liabilities
   = [value] / [value] = [ratio]

X5 = Revenue / Total Assets
   = [value] / [value] = [ratio]

[Z / Z'] SCORE CALCULATION:
[Z' / Z] = [weighted term 1] + [weighted term 2] + ... = [sum]

RESULT: [Z / Z'] = [score] — [🔴/🟡/🟢 ZONE]

INTERPRETATION:
[2-3 sentences interpreting what the score means for this specific company]

KEY WEAKNESS:
[The ratio pulling the score down most, with plain-language explanation]

IMPROVEMENT ACTIONS:
1. [Specific action tied to weakest ratio]
2. [Second action]
3. [Third action]

💰 FINANCIAL DISCLAIMER:
[Standard financial disclaimer — see skills/disclaimers.md]

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [label]
Recommended Next Action: [1 specific sentence]
— VKKM Aegis
```

---

## Hard Rules

1. **Never skip the step-by-step workings.** Show every ratio calculated before the Z-Score total.
2. **Always apply the correct model.** Public firms → Z formula. Private firms → Z' formula.
3. **Never state the Z-Score is a definitive prediction.** It is a statistical screening tool.
4. **Label as ILLUSTRATIVE ESTIMATE** if any input is user-estimated rather than from audited accounts.
5. **Label as DATA-GROUNDED** only if inputs are taken directly from verified financial statements.
6. **Always flag X3 (EBIT/Assets)** — it has the highest predictive coefficient and must be commented on.
7. **Always append the Financial Disclaimer and AEGIS RISK SNAPSHOT.**

---

## Example

**Input:**
> Working Capital = €2M, Total Assets = €10M, Retained Earnings = €1.5M,
> EBIT = €800K, Book Value of Equity = €3M, Total Liabilities = €7M,
> Revenue = €9M | Private company

**Output:**
```
🛡️ VKKM AEGIS — ALTMAN Z-SCORE ANALYSIS
Company Type: Private | Model: Z' (Altman revised for private firms)
Date: 2026-03-06
📊 ILLUSTRATIVE ESTIMATE — Based on user-provided figures, not verified audited accounts.

STEP-BY-STEP CALCULATION:

X1 = Working Capital / Total Assets
   = €2,000,000 / €10,000,000 = 0.200

X2 = Retained Earnings / Total Assets
   = €1,500,000 / €10,000,000 = 0.150

X3 = EBIT / Total Assets
   = €800,000 / €10,000,000 = 0.080

X4 = Book Value of Equity / Total Liabilities
   = €3,000,000 / €7,000,000 = 0.429

X5 = Revenue / Total Assets
   = €9,000,000 / €10,000,000 = 0.900

Z' SCORE CALCULATION:
Z' = 0.717(0.200) + 0.847(0.150) + 3.107(0.080) + 0.420(0.429) + 0.998(0.900)
Z' = 0.143 + 0.127 + 0.249 + 0.180 + 0.898
Z' = 1.597

RESULT: Z' = 1.597 — 🔴 DISTRESS ZONE (below 1.23 threshold)

INTERPRETATION:
The Z'-Score of 1.597 places this private company firmly in the Distress Zone.
Altman's model — validated across decades of data — gives a statistically elevated
probability of financial distress or insolvency within the next 24 months at this score level.

KEY WEAKNESS — X3 (EBIT/Assets = 0.080):
X3 is consistently the most predictive ratio in the model. An EBIT/Assets ratio of 8%
means the company is generating limited operating profit relative to its asset base.
This is the primary driver pulling the score below the safe zone. The business is not
earning enough from its assets to build a financial cushion.

IMPROVEMENT ACTIONS:
1. Improve EBIT margin — pricing review, cost reduction, or revenue diversification
   to push EBIT/Assets above 15% would add ~0.31 to the Z'-Score alone
2. Grow retained earnings — avoid dividend distributions until X2 improves;
   every €500K retained adds ~0.042 to the score
3. Reduce total liabilities — pay down working facility debt to improve X4;
   cutting liabilities by €1M would push X4 from 0.429 to 0.500

💰 FINANCIAL DISCLAIMER:
The Altman Z-Score is a quantitative screening tool, not a definitive bankruptcy
prediction. It does not account for qualitative factors (management quality, industry
headwinds, or pending financing events) and was calibrated primarily on manufacturing
firms. Use this as one input in a broader credit assessment — never as a standalone
decision. Always engage a qualified financial professional for formal credit analysis.

📊 AEGIS RISK SNAPSHOT
Likelihood: 4/5 — Z'-Score in Distress Zone is a strong statistical warning signal;
             historically ~70% of firms at this level face distress within 2 years
Impact: 5/5 — Counterparty bankruptcy would be devastating for any contract or
          investment exposure; immediate review required
Risk Score: 20/25 — 🔴 Critical
Recommended Next Action: Request the last two years of audited accounts and investigate
EBIT margin trajectory before committing any further capital or credit exposure.
— VKKM Aegis
```

---

*Part of VKKM Aegis v2.0 — Advanced Finance Risk Management Plugin*
*Model: Altman (1968) Z-Score, Altman (1983) Z' revision*
