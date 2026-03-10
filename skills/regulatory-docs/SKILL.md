---
description: Regulatory Document Generation
---

# Skill: Regulatory Document Generation
# VKKM Aegis — Always-Active Skill (auto-apply when relevant)
# Version: 2.0

## Rule

Automatically apply this skill whenever the user's situation involves:
- Preparing or reviewing ICAAP, ICLAAP, or ILAAP submissions
- Building or reviewing RCSA documentation
- Designing KRI frameworks and monitoring dashboards
- LCR / NSFR regulatory liquidity reporting
- Supervisory review process (SREP) preparation
- Operational risk regulatory capital calculations

Always: label outputs as illustrative starting points. Never state that any
generated document is supervisor-ready without qualified review.

---

## ICAAP Framework Reference

### Regulatory Foundation:

| Requirement | Source |
|-------------|--------|
| ICAAP obligation | CRD Article 73 (institutions must have sound ICAAP) |
| EBA Guidelines | EBA/GL/2016/10 — SREP and ICAAP Guidelines |
| Basel III | Pillar 2 — Supervisory Review Process |
| ECB ICAAP Guide | ECB Guide to ICAAP (for significant institutions) |

### Mandatory ICAAP Sections (EBA/GL/2016/10):

| Section | Key Content | EBA Requirement |
|---------|-------------|----------------|
| 1. Executive Summary | Risk profile, capital position, key conclusions | Para. 17 |
| 2. Business Model Analysis | Revenue drivers, strategic risks, peer comparison | Para. 22 |
| 3. Risk Inventory & Materiality | All 8 risk types assessed — not just ones management thinks apply | Para. 27 |
| 4. Capital Adequacy | Pillar 1 + Pillar 2 add-ons, headroom, ICR | Para. 33 |
| 5. Stress Testing | Baseline, adverse, severely adverse scenarios | Para. 44 |
| 6. Capital Planning | 3-year projection, dividend policy, contingency | Para. 50 |
| 7. Governance | Board sign-off, management body approval, audit | Para. 55 |

### The 8 Material Risk Types to Always Assess:

1. **Credit Risk** — default by borrowers/counterparties
2. **Market Risk** — trading book losses from price moves
3. **Operational Risk** — internal processes, systems, people, external events
4. **Liquidity Risk** — inability to meet obligations when due
5. **Interest Rate Risk in Banking Book (IRRBB)** — rate sensitivity of the non-trading book
6. **Concentration Risk** — single-name, sector, or geographic concentration
7. **Reputational Risk** — damage to the institution's standing
8. **Strategic Risk** — poor strategic decisions or failure to adapt

### IRRBB — Standard Stress Scenarios (BIS 2016):

| Scenario | Description |
|----------|-------------|
| Parallel up | All rates shift up in parallel |
| Parallel down | All rates shift down in parallel |
| Steepener | Short rates fall, long rates rise |
| Flattener | Short rates rise, long rates fall |
| Short up | Short-term rates rise only |
| Short down | Short-term rates fall only |

Run EVE (Economic Value of Equity) sensitivity for all 6 scenarios. Flag if any EVE impact > −15% of Tier 1 capital (EBA supervisory outlier threshold).

---

## RCSA Framework Reference

### Operational Risk Categories (Basel II / Basel III):

| Category | Subcategory Examples |
|----------|---------------------|
| Internal Fraud | Embezzlement, cheque fraud, mismarking |
| External Fraud | Robbery, forgery, hacking, phishing |
| Employment Practices | HR disputes, discrimination, workplace safety |
| Clients, Products & Business Practices | Mis-selling, conflicts of interest, market manipulation |
| Damage to Physical Assets | Fire, flood, terrorism |
| Business Disruption & Systems | Hardware failure, software bugs, utility outage |
| Execution, Delivery & Process Management | Data entry errors, failed settlements, documentation |

### RCSA Assessment Scale:

```
Inherent Risk = Likelihood (1–5) × Impact (1–5)

Control Effectiveness Multipliers:
  Strong (automated + tested):    × 0.20 → 80% risk reduction
  Moderate (manual, consistent):  × 0.40 → 60% risk reduction
  Weak (manual, inconsistent):    × 0.70 → 30% risk reduction
  None (no control):              × 1.00 → 0% reduction

Residual Risk = Inherent Risk Score × Control Multiplier

Escalation triggers:
  Residual > 20/25 → Immediate escalation to CRO / Board
  Residual 12–19/25 → Monthly monitoring + remediation plan
  Residual < 12/25 → Quarterly monitoring
```

### Control Types:

| Type | Description | Example |
|------|-------------|---------|
| Preventive | Stops the risk event from occurring | 4-eyes approval on wire transfers |
| Detective | Identifies the event after it occurs | Reconciliation, audit logs |
| Corrective | Restores normal state after an event | Business continuity plan, rollback |

---

## KRI Design Framework (BCBS 239 / ISO 31000)

### SMART KRI Definition:

Every KRI must be:
- **Specific:** tied to one clearly defined risk
- **Measurable:** a real number, not a colour or opinion
- **Actionable:** if it turns Red, there is a clear owner and action
- **Relevant:** forward-looking, not just a lagging indicator of past losses
- **Timely:** available fast enough to act before the risk materialises

### Standard KRI Categories for Financial Institutions:

| Category | Example KRIs |
|----------|-------------|
| Liquidity | Cash runway, LCR, NSFR, funding concentration |
| Credit | NPL ratio, CDS spread, Z-Score trend |
| Operational | System uptime, cyber incidents, open audit findings |
| People | Staff turnover, key person dependency, training overdue |
| Regulatory | Open regulatory findings, SAR filing timeliness |
| Market | VaR utilisation vs. limit, P&L delta |
| Reputational | Complaints, press sentiment, social media incidents |

### Threshold Setting Principles:

- **Red = must act now** → tie to regulatory minimum or existential threshold
- **Amber = trend reversal needed** → early warning, before Red
- **Green = normal operating range** → no automatic action required

Examples:
| KRI | Red | Amber | Green |
|-----|-----|-------|-------|
| LCR (bank) | < 100% | 100–115% | > 115% |
| Cash runway | < 6 months | 6–12 months | > 12 months |
| NPL ratio | > 5% | 3–5% | < 3% |
| System uptime | < 98% | 98–99.5% | > 99.5% |

---

## LCR / NSFR Quick Reference (Basel III)

### Liquidity Coverage Ratio (LCR):

```
LCR = HQLA / Net Cash Outflows (30-day stressed scenario)
Minimum regulatory requirement: ≥ 100%

HQLA levels:
  Level 1: Cash, central bank reserves, sovereign bonds (0% haircut)
  Level 2A: Government-backed bonds, PSE bonds (15% haircut)
  Level 2B: Non-financial corporate bonds, equities (25–50% haircut)
  Level 2 cap: Max 40% of HQLA can be Level 2 assets

Net Cash Outflows:
  = Total stressed outflows (30-day) − min(inflows, 75% of outflows)
```

### Net Stable Funding Ratio (NSFR):

```
NSFR = Available Stable Funding (ASF) / Required Stable Funding (RSF)
Minimum regulatory requirement: ≥ 100%

ASF = Σ (Liability amount × ASF factor)
  Capital + long-term bonds:          ASF factor = 100%
  Retail stable deposits (>1yr):      ASF factor = 90–95%
  Retail less stable deposits:        ASF factor = 80–85%
  Wholesale deposits (<6mo):          ASF factor = 0–50%

RSF = Σ (Asset amount × RSF factor)
  HQLA Level 1 assets:                RSF factor = 0%
  Loans to retail/SME <1yr:          RSF factor = 50%
  Residential mortgages:             RSF factor = 65%
  Loans to corporates > 1yr:         RSF factor = 85%
  Other assets:                       RSF factor = 100%
```

---

## Hard Rules for Regulatory Document Outputs

1. Always flag when a document section does not meet EBA guideline requirements.
2. Never tell a user their ICAAP is "complete" — it always requires qualified professional review.
3. All 8 risk types must be assessed in RCSA / ICAAP — even if rated non-material.
4. IRRBB must include all 6 standard BIS rate shock scenarios for banks.
5. KRI dashboard must have at least 8 indicators — fewer provides inadequate coverage.
6. LCR < 100% is always a 🔴 Critical finding — regulatory breach, immediate action required.
7. RCSA must show inherent risk BEFORE controls — the sequence is mandatory.
8. ICAAP must include a severely adverse stress scenario — mild stress testing is insufficient for SREP.
