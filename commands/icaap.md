# Command Spec: `/vkkm:icaap`
# VKKM Aegis — ICAAP Document Generator
# Version: 2.0 | Reliability: 8.5/10
# EBA ICAAP Guidelines (EBA/GL/2016/10) — Basel III Pillar 2.

---

## Overview

**Purpose:** Generate a structured Internal Capital Adequacy Assessment Process
(ICAAP) document — the regulatory document that banks and significant financial
institutions must submit to their supervisory authority (ECB, national CA) annually
under Pillar 2 of the Basel III / CRD framework.

**Who uses this:** Risk officers, CFOs, and compliance teams at banks, credit institutions,
investment firms, and significant fintech entities preparing for SREP review.

**Framework source:** EBA ICAAP Guidelines (EBA/GL/2016/10), CRD Article 73,
Basel Committee on Banking Supervision — Pillar 2 Supervisory Review Process.

---

## Behavior

### Step 1 — Collect institution profile

| Input | Example |
|-------|---------|
| Institution type | Retail bank, investment firm, credit institution, fintech (EMI) |
| Total assets | €2.5 billion |
| Business model | Summary (e.g., SME lending, mortgage bank, payments) |
| Current CET1 ratio | 14.2% |
| Current Tier 1 ratio | 15.1% |
| Current Total Capital ratio | 17.3% |
| Pillar 1 minimum requirement | 8% total capital |
| Key risk types | Which risks are material to this institution |
| Jurisdiction | For national CA-specific requirements |

### Step 2 — Generate the 7-section ICAAP document

Produce each section fully — not as a template but as a realistic, institution-specific document.

### Step 3 — Flag gaps against EBA ICAAP guidelines

After generating each section, identify any areas where the output does not meet
EBA ICAAP guidelines or where additional data/analysis would be required for
submission to a supervisor.

### Step 4 — Append compliance disclaimer and AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — ICAAP DOCUMENT GENERATOR
Institution: [name] | Type: [type] | Total Assets: [amount]
Regulatory Framework: CRD/CRR — Basel III Pillar 2
Reference: EBA/GL/2016/10
Date: [today] | For: [year] SREP submission

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1: EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Institution overview]
[Key risk profile — top 3 risks]
[Capital position summary — CET1/Tier 1/Total Capital vs. requirements]
[Key ICAAP conclusions]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2: BUSINESS MODEL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Business activities and revenue model]
[Key revenue drivers and sustainability]
[Strategic risks and vulnerabilities]
[Peer group comparison (brief)]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3: RISK INVENTORY & MATERIALITY ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
| Risk Type | Materiality | Rationale |
|-----------|-------------|-----------|
| Credit Risk | [M/NM/NA] | [reason] |
| Market Risk | [M/NM/NA] | [reason] |
| Operational Risk | [M/NM/NA] | [reason] |
| Liquidity Risk | [M/NM/NA] | [reason] |
| Interest Rate Risk in Banking Book | [M/NM/NA] | [reason] |
| Concentration Risk | [M/NM/NA] | [reason] |
| Reputational Risk | [M/NM/NA] | [reason] |
| Strategic Risk | [M/NM/NA] | [reason] |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4: CAPITAL REQUIREMENTS BY RISK TYPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Current Pillar 1 ratios vs. minimum requirements]
[Pillar 2 add-on per material risk type]
[Total Internal Capital Requirement (ICR)]
[Available capital vs. ICR — headroom/shortfall]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5: STRESS TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Baseline scenario — capital projections]
[Adverse scenario — defined shock, capital impact]
[Severely adverse scenario — tail risk, capital impact]
[Recovery capacity and management actions]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6: CAPITAL PLANNING (3-YEAR FORWARD LOOK)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Projected capital ratios — Year 1, 2, 3]
[Capital actions planned (issuance, dividend policy)]
[Contingency capital sources]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 7: GOVERNANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Board oversight structure]
[Management body involvement]
[ICAAP review frequency and process]
[External validation / audit]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ EBA GUIDELINE GAPS IDENTIFIED:
[List any sections where data/analysis is insufficient for EBA guidelines]

🏛️ COMPLIANCE DISCLAIMER:
[Standard compliance disclaimer]

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [label]
Recommended Next Action: [1 sentence]
— VKKM Aegis
```

---

## Hard Rules

1. **All 7 sections are mandatory.** Never generate a partial ICAAP document.
2. **Always flag EBA guideline gaps** — supervisors will review against EBA/GL/2016/10 specifically.
3. **Never tell a user their ICAAP is complete or supervisor-ready.** Always note that it requires review by qualified regulatory professionals.
4. **Always note the reporting year** this ICAAP covers.
5. **Materiality assessment is required for all 8 standard risk types** — not just the ones the institution thinks are relevant.
6. **Capital headroom must be quantified** — not just described as "adequate."
7. **Stress scenarios must include a severely adverse scenario** — mild stress testing is insufficient for SREP purposes.
8. **Always append Compliance Disclaimer and AEGIS RISK SNAPSHOT.**

---

## Example

**Input:**
> Institution: Retail lending bank | Total Assets: €2.5B | CET1: 14.2%
> Key risks: credit risk (SME loans), operational risk (IT), liquidity
> Jurisdiction: Germany (BaFin)

**Output:**
```
🛡️ VKKM AEGIS — ICAAP DOCUMENT GENERATOR
Institution: [Retail Lending Bank] | Type: Credit Institution | Total Assets: €2.5B
Regulatory Framework: CRD IV / CRR — Basel III Pillar 2
Reference: EBA/GL/2016/10 | BaFin CircularAT 4.1 (MaRisk)
Date: 2026-03-06 | For: 2026 SREP Submission (Annual)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1: EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The institution is a German retail lending bank with total assets of €2.5 billion,
primarily engaged in SME commercial lending (62% of loan book) and residential
mortgages (28%). The remaining 10% comprises consumer loans and investment securities.

Key risk profile: Credit risk is the dominant material risk, followed by operational
risk (IT infrastructure concentration) and interest rate risk in the banking book (IRRBB).

Capital position: CET1 ratio of 14.2% represents a comfortable buffer above the 4.5%
Pillar 1 minimum and the estimated SREP requirement of ~10.5% (Pillar 1 + P2R + CBR).
Capital headroom stands at approximately 370bps — equivalent to €92.5M of CET1 capital.

ICAAP conclusion: Capital is internally assessed as adequate under the baseline and
adverse scenarios. Capital planning confirms the institution can maintain a CET1 ratio
above 10.5% through 2028 without requiring external capital issuance.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3: RISK INVENTORY & MATERIALITY ASSESSMENT
(Section 2 abbreviated in this example)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
| Risk Type | Materiality | Rationale |
|-----------|-------------|-----------|
| Credit Risk | ✅ Material | 62% of assets in SME lending; elevated PD environment post-2025 |
| Market Risk | ❌ Non-Material | Trading book < 5% of total assets; no proprietary trading |
| Operational Risk | ✅ Material | Core IT infrastructure — single data centre; BCP gaps identified |
| Liquidity Risk | ✅ Material | LCR 118%; NSFR 107% — above minimums but watch deposit concentration |
| IRRBB | ✅ Material | Fixed-rate mortgage book creates rate sensitivity; EVE impact -8% in +200bps shock |
| Concentration Risk | ✅ Material | Top 10 SME borrowers represent 23% of loan book |
| Reputational Risk | ❌ Non-Material | No active litigation; no press incidents in 24 months |
| Strategic Risk | ✅ Material | FinTech competition in SME lending; managed by digital product roadmap |

[Sections 4–7 and EBA gaps would follow in full output...]

⚠️ EBA GUIDELINE GAPS IDENTIFIED:
1. IRRBB — EVE sensitivity analysis required for all 6 standard BIS shocks,
   not just +200bps. Implement before submission.
2. Section 6 — Capital planning projections should include dividend policy assumptions
   explicitly. Currently not addressed.
3. Section 7 — ICAAP review frequency: should explicitly state board sign-off date
   and management body approval process per EBA/GL/2016/10 para. 55.

🏛️ COMPLIANCE DISCLAIMER:
This document was generated by VKKM Aegis as a structured template and starting point
for ICAAP preparation. It does NOT constitute a completed, supervisor-ready ICAAP
submission. ICAAP documents require: review and sign-off by the management body and
board, validation by internal audit or a qualified external party, integration of
actual financial data from the institution's systems, and alignment with the specific
supervisory expectations of the competent authority (ECB/BaFin/other national CA).
Always engage a qualified regulatory specialist before submitting to a supervisor.

📊 AEGIS RISK SNAPSHOT
Likelihood: 2/5 — CET1 at 14.2% provides substantial headroom; baseline capital adequate
Impact: 4/5 — ICAAP deficiencies identified by supervisors can trigger Pillar 2 add-ons,
          additional capital requirements, or public enforcement action
Risk Score: 8/25 — 🟡 Medium
Recommended Next Action: Commission independent ICAAP review by qualified regulatory
advisor before BaFin submission — focus on IRRBB stress testing and Section 6 capital plan.
— VKKM Aegis
```

---

*Part of VKKM Aegis v2.0 — Advanced Finance Risk Management Plugin*
*Framework: EBA/GL/2016/10 | CRD Article 73 | Basel III Pillar 2*
