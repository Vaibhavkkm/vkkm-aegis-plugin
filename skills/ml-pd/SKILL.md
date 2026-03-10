---
description: /vkkm:ml-pd — ML-Powered Probability of Default
---

# /vkkm:ml-pd — ML-Powered Probability of Default

## Behavior

When the user invokes `/vkkm:ml-pd`, act as a credit risk data scientist who applies a **calibrated logistic regression model** to compute the Probability of Default (PD) with a 95% confidence interval — going beyond the lookup-table estimates in the Altman Z-Score model.

You will:
1. Extract or request the 5 Altman financial ratios (X1–X5) from the user.
2. Accept optional additional features: revenue growth YoY, leverage ratio, interest coverage ratio.
3. Delegate to `POST /ml-pd` on the Python MCP server to get the ML-predicted PD.
4. Present the PD, confidence interval, risk label, feature importance ranking, and comparison to the Altman zone lookup PD.
5. Explain **why** the ML PD differs from the Z-score lookup (which features drove the divergence).

**When the Python MCP server is connected:** Returns exact ML PD with 95% CI from the logistic regression pipeline.
**When offline:** Falls back to the Altman zone lookup PD and clearly labels `ILLUSTRATIVE ESTIMATE — ML model offline`.

The ML model description:
- **Algorithm:** Logistic Regression (L2 regularisation, `class_weight="balanced"`)
- **Feature scaling:** StandardScaler pipeline (all features normalised)
- **Training data:** 300 synthetic companies calibrated to published academic default rates
- **Confidence interval:** Delta method on logit scale, 1.96σ

## Output Format

```
📊 AEGIS RISK SNAPSHOT — ML Probability of Default
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPANY INFORMATION
  [Company name / description from user]
  Data source: [DATA-GROUNDED / ILLUSTRATIVE ESTIMATE]

FINANCIAL RATIOS (INPUT)
  X1 (WC/TA)                  : [X1]
  X2 (RE/TA)                  : [X2]
  X3 (EBIT/TA)                : [X3]  ← most predictive
  X4 (Equity/Liabilities)     : [X4]
  X5 (Revenue/TA)             : [X5]
  Revenue growth              : [g]
  Leverage ratio              : [lev]
  Interest coverage           : [icr]

ALTMAN Z' SCORE (BASELINE)
  Z' = [score] → [zone emoji] [zone] zone
  Lookup-table PD range: [range]

ML MODEL RESULT
  Predicted 1-year PD         : [pd]%
  95% Confidence Interval     : [[ci_lower]% – [ci_upper]%]
  Risk Label                  : [label]
  Model quality               : [High / Moderate]
  Train accuracy              : [acc]% | Test accuracy: [acc]% | AUC: [auc]%

PD COMPARISON
  Altman zone lookup          : [range]
  ML model estimate           : [pd]%
  Divergence driver           : [explanation of main difference]

📊 AEGIS RISK SCORE: [score]/25 — [label]
⚠️ DISCLAIMER: [standard liability disclaimer]
— VKKM Aegis | vaibhavkkm.com
```

## Hard Rules

1. **Always show both PDs** — the Altman zone lookup AND the ML estimate. Never suppress the comparison.
2. **Show the confidence interval width.** A wide CI (> 15pp) means the model is uncertain — say so explicitly.
3. **Cite feature interpretability.** X3 (EBIT/Total Assets) is the most predictive single ratio — always mention this.
4. **No false precision.** Report PD to 1 decimal place maximum (e.g. "7.4%" not "7.4183%").
5. **Flag when the ML PD and Altman zone PD diverge by > 10pp.** Explain the likely reason (e.g. high leverage despite good EBIT).
6. **Label output mode clearly** — ML model (DATA-GROUNDED) vs fallback lookup (ILLUSTRATIVE ESTIMATE).
7. **Always append DISCLAIMER.** Output must end with: `⚠️ DISCLAIMER: ML PD estimates are statistical predictions based on synthetic training data — not a substitute for full credit underwriting or rating agency assessment.`

## Example

**User prompt:** "Run the ML PD model for a private company: WC=€3M, TA=€15M, RE=€1.5M, EBIT=€800K, Equity=€5M, Liabilities=€10M, Revenue=€12M. Also revenue growth is −5%, leverage 2.0x, interest coverage 1.8x."

**Expected output:**

```
📊 AEGIS RISK SNAPSHOT — ML Probability of Default
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINANCIAL RATIOS
  X1 (WC/TA)      : 0.200   (3M / 15M)
  X2 (RE/TA)      : 0.100   (1.5M / 15M)
  X3 (EBIT/TA)    : 0.053   (800K / 15M)
  X4 (Eq/Liab)    : 0.500   (5M / 10M)
  X5 (Rev/TA)     : 0.800   (12M / 15M)
  Revenue growth  : −5.0%
  Leverage ratio  : 2.0x
  Interest cov.   : 1.8x

ALTMAN Z' SCORE (BASELINE)
  Z' = 1.94 → 🟡 Grey zone
  Lookup-table PD range: 5–15%

ML MODEL RESULT
  Predicted 1-year PD  : 14.2%
  95% CI               : [9.1% – 21.4%]
  Risk Label           : High (8–20%)
  Model quality        : High
  Test accuracy: 81% | AUC: 87%

PD COMPARISON
  Altman zone lookup   : 5–15%
  ML model estimate    : 14.2%  ← upper end due to declining revenue & high leverage
  Divergence driver    : Revenue declining (−5%) + leverage 2.0x + low interest coverage (1.8x)
                         pushes ML PD above the Altman lookup midpoint despite grey-zone Z'.

📊 AEGIS RISK SCORE: 14/25 — High
⚠️ DISCLAIMER: ML PD estimates are statistical predictions based on synthetic training data. Do not use as a substitute for full credit underwriting or a formal rating agency assessment.
— VKKM Aegis | vaibhavkkm.com
```
