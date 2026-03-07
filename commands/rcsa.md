# Command Spec: `/vkkm:rcsa`
# VKKM Aegis — Risk & Control Self-Assessment Generator
# Version: 2.0 | Reliability: 9/10
# Industry-standard operational risk methodology — ISO 31000 / Basel II OpRisk.

---

## Overview

**Purpose:** Generate a structured Risk and Control Self-Assessment (RCSA) — the
standard operational risk tool used by banks, financial institutions, and regulated
entities to identify, assess, and control risks in every business process.

**Who uses this:** Operational risk teams, compliance officers, business line managers,
and internal auditors conducting process risk reviews.

**Framework source:** ISO 31000 (Risk Management), Basel II Operational Risk Framework,
EBA operational risk guidelines. Industry-standard in banking, insurance, and fintech.

---

## Behavior

### Step 1 — Collect process information

| Input | Description | Example |
|-------|------------|---------|
| Process name | Name of the business process being assessed | Customer Onboarding |
| Department | Which team owns this process | Compliance |
| Process description | 2-3 sentences describing what happens | Collecting customer identity documents, screening against sanctions lists, opening accounts |
| Key systems involved | Technology components | CRM, identity verification tool, core banking system |
| Volume | How many times this process runs per day/month | 500 onboardings/month |
| Regulatory requirements | Which regulations constrain this process | KYC/AML, GDPR |

### Step 2 — Identify risks

Generate a comprehensive list of risks in the process. Cover all four OpRisk categories:
- **People risks** — human error, skills gap, fraud, deliberate misconduct
- **Process risks** — process failure, inadequate procedures, control gaps
- **Systems risks** — technology failure, data loss, cybersecurity, outages
- **External event risks** — third-party failure, fraud, regulatory change

For complex processes: aim for 6–10 risks minimum.

### Step 3 — Score inherent risk (before controls)

```
Inherent Risk Score = Likelihood (1–5) × Impact (1–5)

This is the risk that exists regardless of any controls.
Ask: "If we had no controls at all, how bad would this be?"
```

### Step 4 — Identify and rate controls

For each risk, list:
- What controls currently exist?
- Control type: Preventive (stop the event) or Detective (catch it after)
- Control effectiveness: Strong / Moderate / Weak / None

```
Control Effectiveness Assessment:
  Strong:   Automated, tested regularly, no manual workarounds
  Moderate: Manual but consistently applied; some testing
  Weak:     Manual, inconsistently applied, rarely tested
  None:     No control exists
```

### Step 5 — Score residual risk (after controls)

```
Residual Risk = Inherent Risk × Control Reduction Factor

Control Reduction Factors:
  Strong   → multiply by ~0.2 (80% risk reduction)
  Moderate → multiply by ~0.4 (60% risk reduction)
  Weak     → multiply by ~0.7 (30% risk reduction)
  None     → multiply by 1.0 (no reduction)

Residual risk should be scored on the same 1–25 scale.
```

### Step 6 — Identify control gaps

Flag any residual risk that:
- Remains above 12/25 (High or Critical)
- Has a "Weak" or "None" control rating
- Has no detective control for a high-impact risk event

### Step 7 — Recommend additional controls

For each gap, specify:
- What additional control is needed
- Control type (Preventive / Detective / Corrective)
- Implementation priority (Immediate / 30 days / 90 days)
- Suggested owner

### Step 8 — Append AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — RISK & CONTROL SELF-ASSESSMENT (RCSA)
Process: [name] | Department: [dept] | Date: [today]
Framework: ISO 31000 | Volume: [X per month]
Regulatory scope: [regulations applicable]

| # | Risk Description | Inherent Risk | Control | Effectiveness | Residual Risk | Gap? |
|---|-----------------|--------------|---------|---------------|--------------|------|
| 1 | [risk] | [score 🔴/🟠/🟡/🟢] | [control description] | [Strong/Moderate/Weak/None] | [score 🔴/🟠/🟡/🟢] | [Y/N — gap description] |
[continue for all risks]

CONTROL GAPS IDENTIFIED: [count]

PRIORITY REMEDIATION:
| # | Gap | Recommended Control | Priority | Owner |
|---|-----|---------------------|----------|-------|
[List each gap with recommendation]

RCSA SUMMARY:
| Metric | Value |
|--------|-------|
| Total risks identified | [n] |
| Critical residual risks (>20/25) | [n] |
| High residual risks (10–19/25) | [n] |
| Control gaps requiring remediation | [n] |
| Next RCSA review | [date — recommended] |

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason based on highest residual risk]
Impact: X/5 — [reason]
Risk Score: XX/25 — [label]
Recommended Next Action: [1 sentence]
— VKKM Aegis
```

---

## Hard Rules

1. **Always assess inherent risk before controls** — this is the sequence that matters. Reversing it corrupts the analysis.
2. **Never rate all controls as "Strong"** — this is the most common RCSA failure. Be honest and conservative.
3. **Regulatory risks must be rated at maximum impact** — a KYC breach or AML failure is always 5/5 impact.
4. **Always identify at least one detective control per high-impact risk.** If there's no way to detect the failure, that IS a gap.
5. **Flag any control rated "Weak" where inherent risk is 12+/25** — this combination always needs remediation.
6. **Never call a control "Strong" if it is manual and not tested.** Testing is what makes a control strong.
7. **Recommend a review date** — RCSA is a living document, not a one-time exercise.
8. **No DISCLAIMER, no output.** Every RCSA output must end with a note that the assessment is based on the information provided and requires validation by a qualified operational risk professional before submission to management or regulators. Label output: `⚠️ DISCLAIMER: This RCSA is a structured starting point. Validate with your operational risk team before submission.`

---

## Example

**Input:**
> Process: Customer Onboarding | Department: Compliance
> Description: Collecting customer ID documents, screening sanctions/PEP lists, opening accounts
> Volume: 500/month | Regulations: KYC/AML (AMLD6), GDPR

**Output:**
```
🛡️ VKKM AEGIS — RISK & CONTROL SELF-ASSESSMENT (RCSA)
Process: Customer Onboarding | Department: Compliance | Date: 2026-03-06
Framework: ISO 31000 / Basel II OpRisk | Volume: 500 onboardings/month
Regulatory scope: AML/KYC (AMLD6), GDPR, internal KYC policy

| # | Risk Description | Inherent Risk | Control | Effectiveness | Residual Risk | Gap? |
|---|-----------------|--------------|---------|---------------|--------------|------|
| 1 | Customer identity not verified → KYC breach, account opened for criminal | 25/25 🔴 | ID document check + external database screening (automated) | Moderate | 12/25 🟠 | Yes — enhanced due diligence for high-risk/PEP customers not systematic |
| 2 | PEP/sanctions list not screened → AML regulatory breach, fines | 25/25 🔴 | Automated sanctions screening (daily list update) | Strong | 8/25 🟡 | Watch — adverse media screening missing; consider adding |
| 3 | Data entry error → wrong customer record created, GDPR breach | 9/25 🟡 | Dual-entry verification (data entry + supervisor check) | Moderate | 4/25 🟢 | No — residual risk acceptable |
| 4 | System outage → onboarding process halts; customer SLA breach | 12/25 🟠 | Manual backup procedure (paper forms) | Weak | 10/25 🟠 | Yes — manual procedure is not documented or tested; no recovery time target |
| 5 | Document forgery not detected → fraudulent account opened | 20/25 🔴 | Basic visual document check | Weak | 15/25 🔴 | Yes — biometric verification not in place; no liveness check |
| 6 | GDPR breach: data stored beyond retention period | 16/25 🔴 | Manual deletion review (quarterly) | Weak | 12/25 🟠 | Yes — automated data lifecycle management required; manual process unreliable |

CONTROL GAPS IDENTIFIED: 4

PRIORITY REMEDIATION:
| # | Gap | Recommended Control | Priority | Owner |
|---|-----|---------------------|----------|-------|
| 1 | Document forgery risk (15/25 residual) | Implement biometric ID verification + liveness check (Onfido, iProov, or equivalent) | Immediate | Head of Compliance |
| 2 | No systematic enhanced due diligence for high-risk/PEP | Build automated EDD trigger: any PEP flag or high-risk country → mandatory enhanced review workflow | 30 days | Compliance Officer |
| 3 | System outage manual procedure undocumented | Document manual procedure; run quarterly test; define RTO target (≤2hr) | 30 days | CTO + Compliance |
| 4 | GDPR data retention not automated | Implement automated data lifecycle management; configure system-enforced deletion at 7yr mark | 90 days | DPO + CTO |

RCSA SUMMARY:
| Metric | Value |
|--------|-------|
| Total risks identified | 6 |
| Critical residual risks (>20/25) | 0 (document forgery remediated to 15/25 🔴) |
| High residual risks (10–19/25) | 3 |
| Control gaps requiring remediation | 4 |
| Next RCSA review | Recommend re-assessment in 90 days after gap remediation |

📊 AEGIS RISK SNAPSHOT
Likelihood: 3/5 — Document forgery risk is the dominant finding; biometric gaps are
             industry-wide but that doesn't reduce the risk for this institution
Impact: 5/5 — KYC and AML regulatory breaches carry fines, supervisory action, and
          reputational damage — always rated maximum impact in financial services
Risk Score: 15/25 — 🔴 Critical (regulatory breach potential)
Recommended Next Action: Implement biometric ID verification this month — document forgery
at 15/25 residual risk is the most severe open control gap and a regulatory examination finding.
— VKKM Aegis
```

---

*Part of VKKM Aegis v2.0 — Advanced Finance Risk Management Plugin*
*Framework: ISO 31000 | Basel II Operational Risk | EBA OpRisk Guidelines*
