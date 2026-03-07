# Command Spec: `/vkkm:credit-risk`
# VKKM Aegis — Credit Risk Assessment (PD, EAD, LGD, Expected Loss)
# Version: 2.0 | Reliability: 8.5/10
# Basel II/III credit risk framework — industry-standard methodology.

---

## Overview

**Purpose:** Calculate the key credit risk metrics used by banks, lenders, and
institutional investors to quantify and price their exposure to a borrower or
counterparty under the Basel framework.

**Who uses this:** Credit analysts, loan officers, credit committees, risk managers
assessing a borrower before extending credit or pricing a credit instrument.

**Framework source:** Basel II (2004), Basel III (2010/2017 revision) — the global
standard for credit risk capital under Pillar 1.

---

## Behavior

### Step 1 — Collect inputs

| Input | Description | Example |
|-------|------------|---------|
| Borrower financial data | Balance sheet, P&L, or Altman Z-Score already calculated | Z'-Score = 1.6 |
| Credit rating (if available) | External rating (S&P, Moody's, Fitch) | BB, Ba2 |
| Loan / exposure details | Amount, type (term loan, revolving, guarantee) | €500,000 term loan |
| Collateral | Type, estimated value, seniority | €200,000 property, senior secured |
| Industry | Sector for default rate benchmarking | Manufacturing |

### Step 2 — Estimate PD (Probability of Default)

Use whichever data is available, in priority order:

1. **Altman Z-Score → PD mapping** (if financial data is available):

| Z'/Z Score | Estimated 1-Year PD |
|-----------|---------------------|
| > 2.90 / > 2.99 | < 2% (safe zone) |
| 2.50–2.90 / 2.50–2.99 | 2–5% |
| 1.80–2.50 | 5–10% |
| 1.23–1.80 | 10–20% |
| < 1.23 / < 1.81 | 20–40%+ (distress zone) |

2. **Credit rating → PD mapping** (if rating available):
   Use standard Moody's/S&P 1-year cumulative default rate tables.
   Example: BB/Ba2 → ~1.5% PD, B/B2 → ~5% PD, CCC → ~20%+ PD

3. **Industry default rate** (if limited data):
   Use sector-average annual default rates as a floor estimate.

Always flag if using an estimate vs. a data-grounded figure.

### Step 3 — Calculate EAD (Exposure at Default)

```
EAD = Drawn balance + (Undrawn commitment × Credit Conversion Factor)

For term loans (fully drawn): EAD = Loan amount
For revolving credit: EAD = Drawn + (Limit − Drawn) × CCF
  Where CCF (Basel) ≈ 75% for uncommitted revolving facilities
```

### Step 4 — Estimate LGD (Loss Given Default)

```
LGD = 1 − Recovery Rate

Recovery Rate = (Collateral Value × Haircut) / EAD

Standard Basel collateral haircuts (stressed scenarios):
  Senior secured (property): 40–60% of market value
  Senior secured (financial collateral): 80–90%
  Senior unsecured: 40–50% recovery (LGD ≈ 50–60%)
  Subordinated / junior: 15–30% recovery (LGD ≈ 70–85%)
  Unsecured personal loans: LGD ≈ 75–85%
```

Warn if LGD > 75% — this is a very high-risk exposure level.

### Step 5 — Calculate Expected Loss (EL) and Unexpected Loss (UL)

```
Expected Loss (EL) = PD × EAD × LGD
  (The average loss you expect to realise over time — should be priced into interest spread)

Unexpected Loss (UL) = EAD × LGD × √[PD × (1 − PD)]
  (The volatility of losses around EL — capital must be held against this)

Minimum credit spread to break even on EL alone:
  Required spread (bps) = (EL / EAD) × 10,000
```

### Step 6 — Provide recommendation

- **Approve:** EL < 2% of exposure, LGD < 50%, Z-Score in safe/grey zone
- **Conditional:** EL 2–7%, or one metric is poor but others compensate
- **Reject / Reprice:** EL > 7%, LGD > 75%, Z-Score in distress zone

### Step 7 — Append financial and due diligence disclaimers, and AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — CREDIT RISK ASSESSMENT
Borrower: [Name/Type] | Exposure: [amount] | Facility: [type]
Date: [today]
[📊 ILLUSTRATIVE ESTIMATE / 📊 DATA-GROUNDED]

METRIC CALCULATIONS:

PD Estimation:
  Method: [Z-Score / Credit Rating / Industry Benchmark]
  Estimated PD: [X%] (1-year)
  Basis: [explanation of how PD was derived]
  ⚠️ [Caveat if estimated rather than bureau data]

EAD (Exposure at Default):
  [Show calculation]
  EAD = [amount]

LGD (Loss Given Default):
  Collateral: [type, value, seniority]
  Recovery rate: [X%] ([calculation shown])
  LGD = [X%]
  [⚠️ Warning if LGD > 75%]

EXPECTED LOSS:
  EL = PD × EAD × LGD
  EL = [PD] × [EAD] × [LGD]
  EL = [amount] ([X%] of exposure)

UNEXPECTED LOSS:
  UL = EAD × LGD × √[PD×(1−PD)]
  UL = [amount]

MINIMUM BREAK-EVEN SPREAD:
  Required spread = [X] basis points ([X]% above funding cost)

SUMMARY TABLE:
| Metric | Value | Signal |
|--------|-------|--------|
| PD | [X%] | [risk emoji] |
| EAD | [amount] | — |
| LGD | [X%] | [risk emoji] |
| Expected Loss | [amount] ([X%] of loan) | [risk emoji] |
| Unexpected Loss | [amount] | [risk emoji] |

RECOMMENDATION: [🟢 APPROVE / 🟡 CONDITIONAL / 🔴 DO NOT APPROVE AT CURRENT TERMS]

CONDITIONS (if conditional or reject):
1. [Specific condition]
2. [Second condition]

💰 FINANCIAL DISCLAIMER:
[Standard financial + due diligence disclaimer]

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [label]
Recommended Next Action: [1 specific sentence]
— VKKM Aegis
```

---

## Hard Rules

1. **Never state a PD as precise** unless it comes from a credit bureau or rating agency. Always say "estimated."
2. **Always show EL = PD × EAD × LGD** with numbers — never give just a conclusion.
3. **Always show UL**. Capital must be held against UL, not EL — this distinction is essential for banks.
4. **Always calculate the minimum break-even spread.** A credit decision without spread context is incomplete.
5. **Flag if LGD > 75%** — this means collateral is providing almost no protection.
6. **Distress Zone Z-Score → PD ≥ 12%** — never underestimate this mapping.
7. **Never give a "go" recommendation on a Z-Score in distress zone** without significant compensating factors.
8. **Always append Financial, Due Diligence disclaimers, and AEGIS RISK SNAPSHOT.**

---

## Example

**Input:**
> Borrower Z-Score: 1.6 (distress zone), Loan: €500,000 term loan,
> Collateral: €200,000 property, Senior secured

**Output:**
```
🛡️ VKKM AEGIS — CREDIT RISK ASSESSMENT
Borrower: [Private Company] | Exposure: €500,000 | Facility: Senior Secured Term Loan
Date: 2026-03-06
📊 ILLUSTRATIVE ESTIMATE — PD derived from Z-Score mapping, not credit bureau data.

METRIC CALCULATIONS:

PD Estimation:
  Method: Altman Z'-Score → PD mapping
  Z'-Score: 1.6 → Distress Zone (below 1.81 threshold)
  Estimated PD: ~13.5% (1-year)
  Basis: Altman's research shows firms in the distress zone historically experience
         10–20% annual default rates. 13.5% is the midpoint estimate.
  ⚠️ This is a statistical estimate. Use a credit bureau (Creditreform, Dun & Bradstreet)
     for a precise PD with payment history data.

EAD (Exposure at Default):
  Facility: Term loan, assumed fully drawn
  EAD = €500,000

LGD (Loss Given Default):
  Collateral: €200,000 residential property, senior secured
  Recovery rate = €200,000 × 40% stressed haircut / €500,000 = 16%
  LGD = 1 − 16% = 84%
  ⚠️ LGD of 84% is critically high — the collateral covers only 16% of exposure
     even in a reasonably optimistic stressed recovery scenario.

EXPECTED LOSS:
  EL = PD × EAD × LGD
  EL = 0.135 × €500,000 × 0.84
  EL = €56,700 (11.3% of loan value)

UNEXPECTED LOSS:
  UL = EAD × LGD × √[PD×(1−PD)]
  UL = €500,000 × 0.84 × √[0.135 × 0.865]
  UL = €420,000 × 0.3415
  UL = €143,430

MINIMUM BREAK-EVEN SPREAD:
  Required spread = (€56,700 / €500,000) × 10,000 = 1,134 bps
  Interpretation: You need to charge 11.34% ABOVE your cost of funds just to
  break even on expected losses. This is unviable at standard commercial rates.

SUMMARY TABLE:
| Metric | Value | Signal |
|--------|-------|--------|
| PD | ~13.5% (estimated) | 🔴 Very High |
| EAD | €500,000 | — |
| LGD | 84% | 🔴 Critical |
| Expected Loss | €56,700 (11.3% of loan) | 🔴 Critical |
| Unexpected Loss | €143,430 | 🔴 Critical |

RECOMMENDATION: 🔴 DO NOT APPROVE AT CURRENT TERMS

CONDITIONS FOR RECONSIDERATION:
1. Additional collateral required — target LGD below 50% (needs ~€350K in high-quality collateral)
2. Personal director guarantee — adds qualitative mitigation not in the quantitative model
3. Reduce loan to €200,000 maximum to align with collateral coverage
4. Monthly financial covenant — P&L and cash flow reporting to track Z-Score improvement
5. Price at break-even: minimum 1,134bps over cost of funds — commercially unviable at this rate,
   which itself signals this credit should not be extended at any commercial price

💰 FINANCIAL DISCLAIMER:
PD and LGD estimates are statistical approximations based on the data provided.
Formal credit decisions require a full underwriting process by qualified credit
professionals with access to bureau data, full audited accounts, and director
guarantees assessment. This analysis is a screening tool only — not a credit decision.
Always commission a formal credit assessment from qualified professionals before
extending credit over €50,000.

🔍 DUE DILIGENCE DISCLAIMER:
These estimates are based on limited financial inputs. A proper credit review would
include: 2+ years audited accounts, management accounts, cash flow projections,
industry peer analysis, director background checks, and bureau data.

📊 AEGIS RISK SNAPSHOT
Likelihood: 4/5 — Z'-Score in distress zone; 13.5% PD means roughly 1 in 7 chance
             of default within 12 months based on historical data
Impact: 5/5 — €56,700 expected loss equates to 11.3% of loan; UL of €143K requires
          significant capital allocation; reputational risk from a bad credit decision
Risk Score: 20/25 — 🔴 Critical
Recommended Next Action: Decline at current terms. If relationship value justifies
further consideration, require €350K in additional quality collateral before new assessment.
— VKKM Aegis
```

---

*Part of VKKM Aegis v2.0 — Advanced Finance Risk Management Plugin*
*Framework: Basel II/III Credit Risk — IRB Approach*
*Python MCP endpoint: POST /credit-risk — see mcp_server.py*
