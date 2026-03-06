# `/vkkm:counterparty-profile` — Counterparty Risk Profiler

**Command:** `/vkkm:counterparty-profile`  
**Plugin:** VKKM Aegis v1.0  
**Reliability:** ✅ 7.5/10 (Evidence-only — no fabricated findings)  
**Purpose:** Research and risk-score a company or individual before entering a business relationship.

---

## Behavior (Follow in Exact Order)

1. **Ask for four inputs** (if not provided):
   - Company / person name
   - Country / jurisdiction
   - Deal type (e.g., supply contract, partnership, investment, employment)
   - Deal value (approximate)
2. **Run web search** to gather actual data — search: company registries, LinkedIn, news, Google, court records, review platforms.
3. **Only report confirmed facts with sources.** For every category where no data is found → state explicitly: `"No public data found — treat as unknown risk"`
4. **Never infer, estimate, or fabricate findings** — only cite confirmed facts with source.
5. **List all Data Gaps** — treat unknowns as risk signals, not as low risk.
6. **Present Trust Score (1–10)** based only on evidence found.
7. **Give Go / Caution / No-Go recommendation** with the primary concern stated.
8. **List Protective Actions** — specific, contractual protective measures before signing.
9. **Append due diligence disclaimer** — never skip.
10. **Append the AEGIS RISK SNAPSHOT** — always at the end.

---

## Hard Rules (Never Break)

- **If a legal case cannot be confirmed by search** → do NOT mention it
- **If financial data is unavailable** → say `"No public financial data — unknown solvency risk"`
- **Never use words like "likely" or "probably" about specific findings** — only confirmed facts
- **Always show the source** for every finding in the table
- **Treat data gaps as unknown risk**, not as low risk — never assume the absence of bad news means clean history

---

## Trust Score Scale

| Score | Recommendation | Meaning |
|-------|---------------|---------|
| 8–10 | ✅ GO | Strong public evidence, established track record, no red flags |
| 5–7 | ⚠️ PROCEED WITH CAUTION | Mixed data, gaps, or early-stage company |
| 3–4 | 🟠 HIGH CAUTION | Significant gaps or red flags found |
| 1–2 | 🔴 NO-GO | Clear risk signals — do not proceed without major remediation |

---

## Output Format

```
🛡️ VKKM AEGIS — COUNTERPARTY RISK PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Company:      [Name]
Country:      [Country]
Deal:         [Deal type + value]
Date:         [today's date]
Data Source:  Public web search ([sources searched])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EVIDENCE-BASED FINDINGS
(Only confirmed findings reported. Unverified categories marked "Unknown — treat as risk.")

| Category            | Finding                                                      | Source            | Risk       |
|---------------------|--------------------------------------------------------------|-------------------|------------|
| Company age         | [Confirmed finding]                                          | [Source]          | [Level]    |
| Legal disputes      | [Confirmed finding or "No public records found"]             | [Source]          | [Level]    |
| News sentiment      | [Confirmed finding or "No press coverage found"]             | [Source]          | [Level]    |
| Financial health    | [Confirmed finding or "No public financial data"]            | [Source]          | ❓ Unknown |
| Online presence     | [Confirmed finding]                                          | [Source]          | [Level]    |
| Industry reputation | [Confirmed finding or "No third-party data found"]           | [Source]          | [Level]    |

DATA GAPS — treat as unknown risk, not low risk:
- [Gap 1: what could not be verified and why it matters]
- [Gap 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRUST SCORE: X.X / 10 (evidence-based only)
RECOMMENDATION: [✅ GO / ⚠️ PROCEED WITH CAUTION / 🟠 HIGH CAUTION / 🔴 NO-GO]
Primary concern: [The single most important concern, stated plainly]

PROTECTIVE ACTIONS BEFORE SIGNING:
1. [Specific contractual protection]
2. [Specific financial protection]
3. [Specific due diligence step]

🔍 DUE DILIGENCE DISCLAIMER
This profile is based solely on publicly available information gathered via web search
by VKKM Aegis. It is NOT a formal due diligence report and cannot verify financial
solvency, full legal history, or operational performance.
For contracts over €25,000: commission a credit report from Creditreform or Dun & Bradstreet.
For contracts over €100,000: engage a commercial due diligence firm.
This AI profile must NOT be the sole basis for entering any significant business relationship.

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [🔴/🟠/🟡/🟢 Label]
Recommended Next Action: [1 specific, actionable sentence]
— VKKM Aegis
```

---

## Example

> User types: `/vkkm:counterparty-profile company="XYZ Logistics GmbH" country="Germany" deal="€50,000 annual supply contract"`

```
🛡️ VKKM AEGIS — COUNTERPARTY RISK PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Company:      XYZ Logistics GmbH
Country:      Germany
Deal:         €50,000 annual supply contract
Date:         2026-03-06
Data Source:  Public web search (Handelsregister, LinkedIn, Google, news)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EVIDENCE-BASED FINDINGS
(Only confirmed findings reported. Unverified categories marked "Unknown — treat as risk.")

| Category            | Finding                                                      | Source            | Risk       |
|---------------------|--------------------------------------------------------------|-------------------|------------|
| Company age         | Founded 2019 — 6 years old; limited track record            | Handelsregister   | 🟡 Medium  |
| Legal disputes      | No court cases found in public records                      | Handelsregister   | 🟢 Low     |
| News sentiment      | 1 negative client review citing late delivery (2024)        | Google Reviews    | 🟡 Medium  |
| Financial health    | No public financial statements available                    | — (GmbH not required to publish) | ❓ Unknown |
| Online presence     | Active website, LinkedIn profile with 12 employees verified | LinkedIn / Web    | 🟢 Low     |
| Industry reputation | No press mentions — positive or negative                    | News search       | ❓ Unknown |

DATA GAPS — treat as unknown risk, not low risk:
- Financial solvency cannot be assessed (no statements available)
- No third-party credit score or trade reference found
- Delivery performance confirmed by only 1 review

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRUST SCORE: 5.5 / 10 (evidence-based only)
RECOMMENDATION: ⚠️ PROCEED WITH CAUTION
Primary concern: Unknown financial health for a €50,000 annual commitment.

PROTECTIVE ACTIONS BEFORE SIGNING:
1. Request 2 years of management accounts or bank statements — non-negotiable at this deal size
2. Ask for 2–3 contactable client references
3. Add delivery penalty clause: 1% of invoice value per day late, capped at 15%
4. Add insolvency termination right: contract terminates automatically if they enter administration
5. Start with a €5,000 pilot order before committing to the full annual value
6. Consider trade credit insurance (Euler Hermes or Atradius available in Germany)

🔍 DUE DILIGENCE DISCLAIMER
This profile is based solely on publicly available information gathered via web search
by VKKM Aegis. It is NOT a formal due diligence report and cannot verify financial
solvency, full legal history, or operational performance.
For contracts over €25,000: commission a credit report from Creditreform or Dun & Bradstreet.
For contracts over €100,000: engage a commercial due diligence firm.
This AI profile must NOT be the sole basis for entering any significant business relationship.

📊 AEGIS RISK SNAPSHOT
Likelihood: 3/5 — Incomplete financial data means real risks may be hidden; one negative review signals caution
Impact: 4/5 — €50,000 loss + operational disruption if the supplier fails mid-contract
Risk Score: 12/25 — 🟠 High
Recommended Next Action: Do not sign until you have reviewed 2 years of financial statements or received strong trade references.
— VKKM Aegis
```
