# Command Spec: `/vkkm:reg-calendar`
# VKKM Aegis — Regulatory Reporting Calendar
# Version: 2.0 | Reliability: 7.5/10 (web-search grounded — always verify with regulator)
# Covers EU and global regulatory reporting deadlines.

---

## Overview

**Purpose:** Search for and compile upcoming regulatory reporting deadlines relevant
to the user's entity type and jurisdiction. Ensures no deadline is missed that
could trigger regulatory fines, supervisory action, or enforcement.

**Who uses this:** Compliance officers, CFOs, legal teams, and anyone managing
regulatory reporting obligations across multiple frameworks.

**Critical caveat:** Regulatory deadlines change frequently. This command is a
**web-search-grounded starting point only** — always verify with the official
regulator before relying on any date for compliance purposes.

---

## Behavior

### Step 1 — Collect entity profile

| Input | Description | Example |
|-------|------------|---------|
| Entity type | Bank, fintech (AISP/PISP), fund, corporate, insurance | AISP Fintech |
| Jurisdiction(s) | Country or EU + country (for passported entities) | Luxembourg (CSSF) |
| Applicable regulations | Which regulations this entity is subject to | PSD2, GDPR, AML, DORA |
| Current date | Auto-populate from system date | 2026-03-06 |

### Step 2 — Web search for deadlines

For each applicable regulation, search:
- Official regulator website (CSSF, BaFin, FCA, ECB, ESMA, EBA, etc.)
- EU regulatory calendar (eba.europa.eu, esma.europa.eu, ec.europa.eu)
- Recent supervisory communications or circulars

Report only:
- Confirmed deadlines from official sources
- Estimated deadlines flagged as ⚠️ Estimated / verify with regulator

### Step 3 — Compile chronological calendar

Build a table sorted by deadline date, covering the next 12 months.

For each deadline, flag urgency:
- **🔴 Urgent** = 30 days or less
- **🟡 Approaching** = 31–90 days
- **🟢 Planned** = 91+ days

### Step 4 — Highlight any immediate deadlines (< 30 days)

Flag these immediately and recommend assigned ownership and preparation timeline.

### Step 5 — List official regulator sources

Always list the official websites to verify each deadline directly.

### Step 6 — Append compliance disclaimer and AEGIS RISK SNAPSHOT

---

## Output Format

```
🛡️ VKKM AEGIS — REGULATORY CALENDAR
Entity: [type] | Jurisdiction: [country + regulator] | Date: [today]

UPCOMING DEADLINES (next 12 months):
⚠️ All dates are web-search verified where possible.
Always confirm directly with the relevant regulator before treating these as final.

| Deadline | Regulation | Report / Filing | Regulator | Days Away | Status |
|----------|-----------|----------------|-----------|-----------|--------|
| [date] | [regulation] | [report name + type] | [regulator] | [n]d | [🔴/🟡/🟢] |
[continue chronologically through 12 months]

🔴 URGENT DEADLINES (< 30 days):
[List each with specific action required]

PREPARATION TIMELINE GUIDE:
[For each urgent deadline: what data must be collected, from whom, by when]

📌 OFFICIAL SOURCES:
| Regulator | Website |
|-----------|---------|
[List all relevant official regulator websites]

🏛️ COMPLIANCE DISCLAIMER:
Regulatory deadlines and requirements change. Always verify directly with the
relevant regulator before relying on this calendar for compliance purposes.
This is an AI-assisted research output — not a legal compliance opinion.

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [based on urgency of closest deadline]
Impact: X/5 — [based on consequences of missing the most critical deadline]
Risk Score: XX/25 — [label]
Recommended Next Action: [specific action for the most urgent deadline]
— VKKM Aegis
```

---

## Hard Rules

1. **Only report confirmed deadlines from official sources** — never fabricate dates.
2. **Mark any deadline not confirmed via web search as ⚠️ Estimated — verify with regulator.**
3. **Always list official regulator websites** — never leave the user without a verification path.
4. **Any deadline < 30 days must be flagged as 🔴 URGENT** with a specific preparation action.
5. **Never state that the user "is compliant"** — only identify deadlines and whether preparation appears to be underway.
6. **DORA is effective from January 2025** — all financial entities in EU scope must be tracking ICT risk reporting.
7. **GDPR anniversary processes (DPO review, register review)** are often missed — always include if applicable.
8. **Always append Compliance Disclaimer and AEGIS RISK SNAPSHOT.**

---

## Key Regulations and Standard Annual Deadlines Reference

For quick lookup when building the calendar:

| Regulation | Typical Deadline Type | Notes |
|-----------|----------------------|-------|
| GDPR | Annual DPO review, records of processing review | No hard date — typically year-end |
| PSD2 | Semi-annual fraud reporting; annual activity report | Dates vary by national CA |
| AML/KYC | Annual AML compliance report | Dates vary by national CA |
| DORA | ICT risk register update; incident reporting (ad hoc) | Effective Jan 2025 |
| MiFID II | Transaction reporting (T+1, ongoing); annual best execution | Ongoing |
| EMIR | Trade reporting (T+1, ongoing); annual reconciliation | See ESMA calendar |
| SFDR | RTS disclosures; annual PAI statements (30 June) | 30 June annually |
| CRR/CRD (Basel) | COREP (quarterly); FINREP (quarterly/semi-annual) | See EBA calendar |
| CSRD | Annual sustainability report (phased in 2024–2028) | Deadline varies by company size |

---

## Example

**Input:**
> Entity: Fintech (AISP) | Jurisdiction: Luxembourg (CSSF) | Date: 2026-03-06
> Regulations: PSD2, GDPR, AML, DORA

**Output:**
```
🛡️ VKKM AEGIS — REGULATORY CALENDAR
Entity: Fintech (AISP — Account Information Service Provider)
Jurisdiction: Luxembourg | Regulator: CSSF (Commission de Surveillance du Secteur Financier)
Date: 2026-03-06

UPCOMING DEADLINES (next 12 months):
⚠️ Dates are web-search verified where confirmed. Verify all dates directly with CSSF
and CNPD before treating as final compliance deadlines.

| Deadline | Regulation | Report / Filing | Regulator | Days Away | Status |
|----------|-----------|----------------|-----------|-----------|--------|
| 31 Mar 2026 | PSD2 | Annual Activity Report (AISP) to CSSF | CSSF | 25d | 🔴 URGENT |
| 30 Apr 2026 | GDPR | Annual Records of Processing Activities review + DPA register update | CNPD | 55d | 🟡 Approaching |
| 31 May 2026 | AML/AMLD6 | Annual AML Compliance Officer Report to CSSF | CSSF | 86d | 🟡 Approaching |
| 30 Jun 2026 | DORA | ICT risk register full review + third-party provider register update | CSSF | 116d | 🟢 Planned |
| 30 Jun 2026 | GDPR | Annual DPO Performance Review (internal) | Internal | 116d | 🟢 Planned |
| 30 Sep 2026 | PSD2 | Semi-annual Fraud Reporting (AISP fraud statistics) | CSSF | 208d | 🟢 Planned |
| 31 Dec 2026 | GDPR | Annual Privacy Notice review + cookie policy audit | CNPD | 300d | 🟢 Planned |
| 31 Dec 2026 | DORA | Annual DORA self-assessment (ICT readiness) | CSSF | 300d | 🟢 Planned |

🔴 URGENT: PSD2 Annual Report due in 25 days (31 March 2026)

PREPARATION TIMELINE:
PSD2 Annual Activity Report to CSSF — 25 days remaining:
  Week 1 (now): Assign report owner (typically Compliance Officer)
  Week 1: Pull activity data from system: number of accounts accessed,
           transaction volume processed, incident log, complaint register
  Week 2: Draft report using CSSF template (available on cssf.lu)
  Week 3: Internal review by CEO/CTO; legal counsel sign-off
  Week 4: Submit via CSSF eDesk portal (allow 2 days for technical issues)

📌 OFFICIAL SOURCES:
| Regulator | Website | Purpose |
|-----------|---------|---------|
| CSSF | cssf.lu | PSD2 reporting, AML reporting, DORA for PSPs |
| CNPD | cnpd.public.lu | GDPR — Luxembourg Data Protection Authority |
| EBA | eba.europa.eu | EBA Guidelines, PSD2 RTS, AML guidelines |
| ESMA | esma.europa.eu | MiFID II, EMIR, SFDR |
| EU EUR-Lex | eur-lex.europa.eu | Full text of all EU regulations |

🏛️ COMPLIANCE DISCLAIMER:
Regulatory deadlines change without notice. The dates above are provided as a
research-based starting point only. This is NOT a compliance opinion or legal advice.
VKKM Aegis specifically does not guarantee the accuracy of regulatory deadline dates —
they must be confirmed with the relevant competent authority before any compliance
decision is made. Always engage a qualified EU regulatory lawyer or compliance
specialist, especially for financial services entities in regulated markets.

📊 AEGIS RISK SNAPSHOT
Likelihood: 5/5 — PSD2 annual report is due in 25 days with no preparation mentioned;
             regulatory deadlines are deterministic — the risk of a breach is 100% without action
Impact: 4/5 — Late or missing reports to CSSF can trigger supervisory investigation,
          escalation of SREP score, or formal warning / fine
Risk Score: 20/25 — 🔴 Critical
Recommended Next Action: Assign PSD2 Annual Activity Report owner today and extract
activity data from systems — 25 days is tight for a fresh start.
— VKKM Aegis
```

---

*Part of VKKM Aegis v2.0 — Advanced Finance Risk Management Plugin*
*Sources: CSSF, EBA, ESMA, ECB, national competent authorities*
*Always verify with official sources — regulatory deadlines change*
