# Skill: Credit Risk Models
# VKKM Aegis — Always-Active Skill (auto-apply when relevant)
# Version: 2.0

## Rule

Automatically apply these models whenever the user's situation involves:
- Assessing a borrower, counterparty, or debtor
- Making credit decisions or loan approvals
- Pricing credit risk (loan spreads, credit derivatives)
- Reviewing financial health of a company

Always label outputs as ILLUSTRATIVE ESTIMATE (model-based) or DATA-GROUNDED
(when bureau or rating data is available).

---

## Altman Z-Score Models

### Public Company Model (Altman 1968):

```
Z = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5

X1 = Working Capital / Total Assets
X2 = Retained Earnings / Total Assets
X3 = EBIT / Total Assets                ← Most predictive ratio
X4 = Market Value of Equity / Total Liabilities
X5 = Revenue / Total Assets

Zones:  Z > 2.99 → 🟢 Safe
        1.81 < Z < 2.99 → 🟡 Grey Zone
        Z < 1.81 → 🔴 Distress (elevated bankruptcy risk)
```

### Private Company Model (Altman 1983 — Z' revision):

```
Z' = 0.717×X1 + 0.847×X2 + 3.107×X3 + 0.420×X4 + 0.998×X5

X4 = Book Value of Equity / Total Liabilities  (no market price needed)

Zones:  Z' > 2.90 → 🟢 Safe
        1.23 < Z' < 2.90 → 🟡 Grey Zone
        Z' < 1.23 → 🔴 Distress
```

### Z-Score → PD Mapping (approximate):

| Z'/Z Score | Estimated 1-Year PD |
|-----------|---------------------|
| > 2.90 / > 2.99 | < 2% |
| 2.50–2.90 | 2–5% |
| 1.80–2.50 | 5–10% |
| 1.23–1.80 | 10–20% |
| < 1.23 / < 1.81 | 20–40%+ |

Always caveat: this mapping is statistical, not precise. Use credit bureau data for formal PD.

---

## Basel Credit Risk Framework

### The Core Credit Risk Equation:

```
Expected Loss (EL) = PD × EAD × LGD

Where:
  PD  = Probability of Default — likelihood of default within 1 year
  EAD = Exposure at Default — total drawn balance at time of default
  LGD = Loss Given Default — % of EAD that is lost after recovery

Unexpected Loss (UL) = EAD × LGD × √[PD × (1 − PD)]
  Capital is held against UL — not EL.
  EL is priced into the credit spread.
```

### EAD Calculation:

```
For term loans (fully drawn):
  EAD = Loan amount

For revolving credit / committed facilities:
  EAD = Drawn balance + (Undrawn commitment × CCF)
  CCF (Credit Conversion Factor) = 75% for uncommitted lines (Basel standard)
```

### LGD Estimation by Collateral Type:

| Collateral Type | Recovery Rate | LGD |
|----------------|--------------|-----|
| Cash / government securities | 95–100% | 0–5% |
| Senior secured (financial collateral) | 80–90% | 10–20% |
| Senior secured (commercial property) | 50–60% | 40–50% |
| Senior secured (residential property, stressed) | 35–50% | 50–65% |
| Senior unsecured | 40–50% | 50–60% |
| Subordinated / junior debt | 15–30% | 70–85% |
| Unsecured consumer | 10–20% | 80–90% |

### Credit Rating → PD Mapping (Moody's / S&P historical averages):

| Rating | Moody's | 1-Year PD |
|--------|---------|-----------|
| Investment grade | Aaa–Baa3 | < 0.5% |
| BB+ / Ba1 | Sub-investment | ~0.5–1.5% |
| BB / Ba2 | Sub-investment | ~1.5–2.5% |
| B / B2 | Sub-investment | ~3–7% |
| CCC+ or below | Speculative | 10–30%+ |
| Distress zone (Z-Score) | Unrated | 12–25% |

### Minimum Break-Even Credit Spread:

```
Required spread (bps) = (EL / EAD) × 10,000

Example: EL = €56,700 on €500,000 EAD
  = (56,700 / 500,000) × 10,000 = 1,134 bps (11.34% over funding cost)
```

---

## Industry Default Rate Benchmarks (annual, approximate)

Use as floor PD estimate when no financial data is available:

| Sector | Historical Default Rate |
|--------|------------------------|
| Technology / SaaS | 1–3% |
| Manufacturing | 2–4% |
| Retail / Consumer | 3–6% |
| Construction | 4–7% |
| Hospitality / Restaurants | 5–10% |
| Energy (upstream) | 3–8% |
| Financial services | 1–2% |
| Real estate | 2–5% |

---

## Hard Rules for Credit Risk Outputs

1. Never state a PD as exact without bureau data — always flag as "estimated."
2. Always show full EL = PD × EAD × LGD calculation — never skip to the answer.
3. Always show UL — capital requirements are driven by UL, not EL.
4. Flag if LGD > 75% — this is a critical finding every time.
5. Z-Score in distress zone → PD ≥ 12% minimum assumption.
6. Always calculate minimum break-even spread — price discipline matters.
7. Distress zone Z-Score + LGD > 75% = Do Not Approve without exceptional compensating factors.
