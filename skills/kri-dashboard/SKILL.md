---
description: Command Spec: `/vkkm:kri-dashboard`
---

# Command Spec: `/vkkm:kri-dashboard`
# VKKM Aegis — Key Risk Indicator (KRI) Dashboard Setup
# Version: 2.0 | Reliability: 8/10
# BCBS 239 / ISO 31000 operational risk monitoring framework.

---

## Overview

**Purpose:** Define a set of Key Risk Indicators (KRIs) for a business or department,
set Green/Amber/Red threshold levels, and track the entity's current status against
those thresholds. Generates a live-readable RAG (Red-Amber-Green) dashboard.

**Who uses this:** Chief Risk Officers, CFOs, board risk committees, operational
risk managers, and compliance monitors who need early warning of increasing risk.

**What makes a good KRI:** A KRI must be SMART:
- **Specific** to a risk
- **Measurable** (a real number, not an opinion)
- **Actionable** (if it turns red, you know what to do)
- **Relevant** to the most material risks
- **Timely** (available before the risk materialises — leading indicator, not lagging)

---

## Behavior

### Step 1 — Collect entity profile

| Input | Description |
|-------|------------|
| Entity type | Company, bank, fintech, department, fund |
| Industry | Financial services, technology, manufacturing, etc. |
| Top 3–5 risk areas | The main categories of risk this entity faces |
| Current metric values | Optional — if current values provided, show RAG status immediately |

### Step 2 — Design KRI set (8–12 indicators)

Cover these domains based on entity type:

**Financial / Liquidity:**
- Cash runway (months)
- Revenue concentration (top client %)
- Debt service coverage ratio
- Days Sales Outstanding (DSO)
- Burn rate vs. plan

**Operational / Technology:**
- System uptime / availability (%)
- Cyber incidents (per month)
- Unresolved IT vulnerabilities (count)
- Disaster recovery test pass rate (%)

**People:**
- Employee turnover (annual %)
- Key person / single-point-of-failure dependency
- HR escalations (per month)

**Regulatory / Compliance:**
- Open regulatory findings (count)
- Overdue compliance training (%)
- SARs / suspicious activity reports (if applicable)
- Audit exceptions (per quarter)

**Credit / Counterparty:**
- Portfolio non-performing loan ratio
- Top-10 borrower concentration
- Overdue receivables > 60 days

### Step 3 — Set Green/Amber/Red thresholds for each KRI

For each indicator:
- **Green** = acceptable operating range — no immediate action needed
- **Amber** = early warning — management attention required, trend must be reversed
- **Red** = threshold breach — escalation required immediately

Thresholds should be:
- Based on regulatory requirements where they exist (e.g., LCR ≥ 100%)
- Based on industry benchmarks where available
- Based on the entity's stated risk appetite where defined

### Step 4 — Accept current values from the user

If the user provides current metric values, immediately calculate and display RAG status.
If not, generate the KRI framework with placeholder status and ask for values.

### Step 5 — Flag all Red and Amber KRIs with priority actions

### Step 6 — Recommend monitoring frequency per KRI

### Step 7 — Append AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — KRI DASHBOARD
Entity: [name/type] | Date: [today] | Review: [frequency]

| #  | KRI | Green | Amber | Red | Current | Status | Trend |
|----|-----|-------|-------|-----|---------|--------|-------|
| 1  | [indicator] | [threshold] | [threshold] | [threshold] | [value] | [🟢/🟡/🔴] | [↑↓→] |
[continue for all KRIs]

DASHBOARD SUMMARY:
🔴 RED: [count]  |  🟡 AMBER: [count]  |  🟢 GREEN: [count]

PRIORITY ACTIONS:
🔴 KRI #[n] — [name] at [current value]: [specific action with owner and deadline]
🟡 KRI #[n] — [name]: [monitoring action or trend reversal needed]

RECOMMENDED MONITORING FREQUENCY:
| KRI | Frequency | Owner |
[table of monitoring cadence]

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [based on number and severity of red/amber KRIs]
Impact: X/5 — [based on nature of red KRIs]
Risk Score: XX/25 — [label]
Recommended Next Action: [most critical single action]
— VKKM Aegis
```

---

## Hard Rules

1. **Always generate 8–12 KRIs minimum.** Fewer provides insufficient monitoring coverage.
2. **Every KRI must have a clear Red threshold** — not just a vague "if it gets worse."
3. **Red KRIs always require an immediate priority action** in the output — not just flagging.
4. **Never set all thresholds as "above industry average"** — use specific numbers.
5. **Regulatory minimums are always the Red threshold** (e.g., LCR < 100% is always Red, not Amber).
6. **Include at least one leading indicator** — KRIs that predict future risk, not just describe past losses.
7. **Always include a monitoring frequency recommendation** — a dashboard with no review cadence provides no protection.
8. **If the user provides current values, show trends** where possible (↑ worsening, ↓ improving, → stable).
9. **Always append DISCLAIMER.** Every KRI dashboard output must note: `⚠️ DISCLAIMER: KRI thresholds should be calibrated to your specific risk appetite and validated by qualified risk professionals. This dashboard is a starting point — not a replacement for a formally approved risk appetite statement.`

---

## Example

**Input:**
> Company: Fintech startup | Industry: Financial Services | Review: Monthly
> Top risks: cash, client concentration, regulatory findings, cyber
> Current values provided by user

**Output:**
```
🛡️ VKKM AEGIS — KRI DASHBOARD
Entity: Fintech Startup | Industry: Financial Services
Date: 2026-03-06 | Review Frequency: Monthly

| #  | KRI | Green | Amber | Red | Current | Status | Trend |
|----|-----|-------|-------|-----|---------|--------|-------|
| 1  | Cash runway (months) | >12mo | 6–12mo | <6mo | 5.9mo | 🔴 RED | ↓ |
| 2  | Top client revenue concentration | <25% | 25–40% | >40% | 42% | 🔴 RED | → |
| 3  | Open regulatory findings (count) | 0 | 1–2 | >2 | 1 | 🟡 AMBER | → |
| 4  | System uptime (%) | >99.5% | 98–99.5% | <98% | 99.7% | 🟢 GREEN | ↑ |
| 5  | Employee turnover (annual %) | <10% | 10–20% | >20% | 8% | 🟢 GREEN | → |
| 6  | Customer complaints (per month) | <5 | 5–15 | >15 | 3 | 🟢 GREEN | ↓ |
| 7  | Days Sales Outstanding (DSO) | <30d | 30–60d | >60d | 45d | 🟡 AMBER | ↑ |
| 8  | Cyber incidents (per month) | 0 | 1 | >1 | 0 | 🟢 GREEN | → |
| 9  | Overdue compliance training (%) | <5% | 5–15% | >15% | 12% | 🟡 AMBER | ↑ |
| 10 | Unresolved critical IT vulnerabilities | 0 | 1–2 | >2 | 1 | 🟡 AMBER | → |
| 11 | Revenue plan vs. actual (%) | >95% | 80–95% | <80% | 89% | 🟡 AMBER | ↓ |
| 12 | Outstanding debt service vs. cash (%) | <10% | 10–20% | >20% | 7% | 🟢 GREEN | → |

DASHBOARD SUMMARY:
🔴 RED: 2  |  🟡 AMBER: 5  |  🟢 GREEN: 5
Warning: 7 of 12 KRIs are Amber or Red — this is an elevated risk environment.

PRIORITY ACTIONS:

🔴 KRI #1 — Cash runway at 5.9 months: CRITICAL
  Action: Arrange revolving credit facility (minimum €150K) before end of month.
  This is the single highest-priority action — everything else is secondary.
  Owner: CFO | Deadline: 30 days

🔴 KRI #2 — Client concentration at 42%: CRITICAL
  Action: Activate client diversification programme. Set formal target: top client
  must fall below 25% of revenue within 12 months. Monthly tracking required.
  Owner: CEO + Head of Sales | Deadline: Immediate action plan; 12-month target

🟡 KRI #3 — Open regulatory finding: ESCALATE
  Action: Ensure the open finding has a documented remediation plan with deadline.
  If unresolved after 30 days, escalate to board risk committee.
  Owner: Compliance Officer | Deadline: 30 days to resolution

🟡 KRI #7 — DSO trending upward to 45 days:
  Action: Implement stricter collections process. Review top-5 overdue accounts.
  Consider early payment incentives. DSO above 60 = Red — reverse trend now.
  Owner: Finance Team | Deadline: Review next month's DSO

🟡 KRI #9 — Compliance training at 12% overdue (trending worse):
  Action: Mandatory completion deadline to staff. Block system access for non-compliant
  users if this reaches 15% (Red threshold) — regulatory audit risk.
  Owner: Compliance Officer | Deadline: 2 weeks

RECOMMENDED MONITORING FREQUENCY:
| KRI | Frequency | Owner |
|-----|-----------|-------|
| Cash runway, Revenue vs. plan | Weekly | CFO |
| Client concentration, DSO | Monthly | CFO + Sales |
| Regulatory findings, Compliance training | Monthly | Compliance Officer |
| System uptime, Cyber incidents, IT vuln | Weekly | CTO |
| Employee turnover, Customer complaints | Monthly | HR + Customer Success |

📊 AEGIS RISK SNAPSHOT
Likelihood: 5/5 — Two KRIs already in Red with current values; five in Amber and trending
             in the wrong direction. This is an active risk environment, not a forward-looking one.
Impact: 5/5 — Cash exhaustion and client concentration loss are existential risk events;
          regulatory findings can trigger supervisory action
Risk Score: 25/25 — 🔴 Critical
Recommended Next Action: Cash runway is the existential priority — arrange revolving credit
facility within 30 days, then address client concentration within 90 days.
— VKKM Aegis
```

---

*Part of VKKM Aegis v2.0 — Advanced Finance Risk Management Plugin*
*Framework: BCBS 239 Risk Data Aggregation | ISO 31000 | EBA OpRisk Guidelines*
