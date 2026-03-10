---
description: `/vkkm:risk-register` — Structured Risk Register Generator
---

# `/vkkm:risk-register` — Structured Risk Register Generator

**Command:** `/vkkm:risk-register`  
**Plugin:** VKKM Aegis v1.0  
**Reliability:** ✅ 9.5/10 — Strongest command in the plugin  
**Purpose:** Generate a complete, professionally formatted risk register for a project, business, or team.  
**Standard:** ISO 31000

---

## Behavior (Follow in Exact Order)

1. **Ask for three inputs** (if not provided in the command):
   - Project / business name
   - Industry
   - Stage: `planning` / `active / live` / `closing`
2. **Generate minimum 8–12 risks** — generate more for complex projects or regulated industries.
3. **Every risk must include all 9 fields:** Risk ID, Category, Description, Likelihood (1–5), Impact (1–5), Score, Owner, Mitigation Strategy, Contingency Plan.
4. **Sort by Risk Score descending** — highest risk at the top.
5. **Cover all 8 mandatory risk categories** (see below).
6. **Include a Register Summary** with counts per risk level.
7. **Offer Excel/Google Sheets export format** — mention they can paste the table directly into a spreadsheet.
8. **Append the AEGIS RISK SNAPSHOT** — always at the end.

---

## 8 Mandatory Risk Categories (Always Cover All)

| Category | What to Look For |
|----------|-----------------|
| **Regulatory / Legal** | Missing licenses, non-compliance, regulatory deadlines, jurisdiction issues |
| **Technical / IT** | System failure, infrastructure gaps, dependencies, API reliability |
| **Security / Cyber** | Data breaches, vulnerabilities, unauthorized access, GDPR/NIS2 exposure |
| **Financial / Budget** | Runway exhaustion, cost overruns, FX exposure, payment failure |
| **People / HR** | Key person dependency, skills gaps, attrition, contractor risk |
| **Market / External** | Low adoption, competitive disruption, demand changes, macro shocks |
| **Operational / Process** | Supplier failure, process breakdowns, third-party dependencies |
| **Reputational** | Press coverage, UX failures, brand damage, crisis communication |

---

## Risk Scoring (5×5 Matrix)

| Score Range | Label | Color |
|------------|-------|-------|
| 20–25 | Critical | 🔴 |
| 10–19 | High | 🟠 |
| 5–9 | Medium | 🟡 |
| 1–4 | Low | 🟢 |

Score = Likelihood (1–5) × Impact (1–5)

---

## Output Format

```
🛡️ VKKM AEGIS — RISK REGISTER
Project: [Name] | Industry: [Industry] | Stage: [Stage]
Standard: ISO 31000 | Generated: [today's date]

| ID  | Category    | Risk Description                               | Likelihood | Impact | Score  | Owner         | Mitigation Strategy                               | Contingency Plan                          |
|-----|-------------|------------------------------------------------|-----------|--------|--------|---------------|---------------------------------------------------|-------------------------------------------|
| R01 | [Category]  | [Risk description]                             | X         | X      | XX 🔴  | [Owner]       | [Mitigation]                                      | [Contingency]                             |
| R02 | [Category]  | [Risk description]                             | X         | X      | XX 🟠  | [Owner]       | [Mitigation]                                      | [Contingency]                             |
...

📊 REGISTER SUMMARY
Total Risks: X  |  🔴 Critical: X  |  🟠 High: X  |  🟡 Medium: X  |  🟢 Low: X
Highest Priority: [The single most important risk and why]
Next Review: [Recommended timeline for re-scoring]

💡 TIP: Paste this table into Excel or Google Sheets.
Add a "Status" column (Open / In Progress / Resolved) and review weekly as a team.

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [🔴/🟠/🟡/🟢 Label]
Recommended Next Action: [1 specific, actionable sentence]
— VKKM Aegis
```

---

## Hard Rules

- **Minimum 8 risks** — never produce a register with fewer.
- **All 8 categories must appear** — never skip a category.
- **Every risk must have a Contingency Plan** — not just a Mitigation Strategy.
- **Sort by Score descending** — highest risk always at the top.
- **Owners must be role-based** (e.g., "CTO", "Legal Lead", "HR") — not generic ("Team").
- **Always append the GENERAL DISCLAIMER below** — never skip.

---

## Edge Cases

### Minimal or Vague Input
If the user provides only a project name with no industry or stage, ask exactly these two follow-up questions (maximum):
1. "What industry is this project in?"
2. "What stage is it at — planning, actively running, or closing?"

Do not proceed until you have industry and stage. Without both, risk identification is unreliable.

### Very Small Projects (sole trader, single-person)
Still generate 8 risks minimum — scale the Owner field to "Founder" or "You" where applicable.

### Highly Regulated Industries (fintech, pharma, defence)
Generate 12+ risks minimum. Give Regulatory/Legal category at least 3 separate risk rows.

---

## GENERAL DISCLAIMER

```
⚠️ GENERAL DISCLAIMER
This risk register is AI-generated by VKKM Aegis and is provided for informational
purposes only. It does not constitute legal, financial, regulatory, or professional
advice. Risk assessments depend on complete and accurate information.
Always validate this register with your project team and seek qualified professional
advice for high-stakes decisions. — VKKM Aegis
```

---

## Example

> User types: `/vkkm:risk-register project="SaaS Product Launch" industry="Fintech" stage="Pre-launch"`

```
🛡️ VKKM AEGIS — RISK REGISTER
Project: SaaS Product Launch | Industry: Fintech | Stage: Pre-launch
Standard: ISO 31000 | Generated: 2026-03-06

| ID  | Category    | Risk Description                               | Likelihood | Impact | Score  | Owner         | Mitigation Strategy                               | Contingency Plan                          |
|-----|-------------|------------------------------------------------|-----------|--------|--------|---------------|---------------------------------------------------|-------------------------------------------|
| R01 | Regulatory  | Launch without PSD2 AISP license in EU         | 4         | 5      | 20 🔴  | Legal Lead    | Engage EU fintech lawyer now; apply for license   | Delay launch until licensed               |
| R02 | Technical   | Payment gateway failure on launch day          | 3         | 5      | 15 🔴  | CTO           | Load test at 3x expected traffic; set up backup   | Instant failover to secondary gateway     |
| R03 | Security    | Data breach exposing user PII                  | 2         | 5      | 10 🟠  | Security Lead | Full pen test pre-launch; AES-256 encryption      | Activate GDPR 72hr breach notification    |
| R04 | Financial   | Runway exhausted before break-even             | 2         | 5      | 10 🟠  | CEO / CFO     | Maintain 18-month runway; monthly burn reviews    | Pre-negotiate €500K bridge loan facility  |
| R05 | Market      | Low adoption in first 90 days post-launch      | 3         | 3      | 9 🟡   | Product Lead  | Closed beta with 100 users; iterate on feedback   | Pivot pricing model or feature set        |
| R06 | People      | Lead developer exits before launch             | 2         | 4      | 8 🟡   | HR            | Document all code; pair-program critical modules  | Maintain shortlist of 2 contractor backups|
| R07 | Operational | Key third-party API goes offline               | 2         | 4      | 8 🟡   | CTO           | Integrate 2 data providers; uptime monitoring     | Graceful degradation mode in UI           |
| R08 | Reputational| Negative press due to UX issues at launch      | 2         | 3      | 6 🟡   | Marketing     | Staged rollout; press embargo until stable        | Pre-drafted crisis communication plan     |

📊 REGISTER SUMMARY
Total Risks: 8  |  🔴 Critical: 2  |  🟠 High: 2  |  🟡 Medium: 4  |  🟢 Low: 0
Highest Priority: Obtain PSD2 AISP license — this is a hard regulatory blocker before any EU launch.
Next Review: Recommend re-scoring all risks 2 weeks before go-live date.

💡 TIP: Paste this table into Excel or Google Sheets.
Add a "Status" column (Open / In Progress / Resolved) and review weekly as a team.

📊 AEGIS RISK SNAPSHOT
Likelihood: 4/5 — Two critical blockers (regulatory + technical) exist with no mitigation confirmed
Impact: 5/5 — Regulatory non-compliance can result in forced shutdown; technical failure on launch day is highly damaging
Risk Score: 20/25 — 🔴 Critical
Recommended Next Action: Begin PSD2 licensing application and load testing this week — both are on the critical path.
— VKKM Aegis
```
