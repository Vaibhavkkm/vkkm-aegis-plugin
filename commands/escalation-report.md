# `/vkkm:escalation-report` — Risk Escalation Memo Writer

**Command:** `/vkkm:escalation-report`  
**Plugin:** VKKM Aegis v1.0  
**Reliability:** ✅ 9.5/10 — Highest reliability command  
**Purpose:** Write a professional, structured risk escalation memo for management, stakeholders, board members, or external parties.

---

## Behavior (Follow in Exact Order)

1. **Ask for four inputs** (if not provided in the command):
   - Risk description (what happened or what was found)
   - Severity (`low` / `medium` / `high` / `critical`)
   - Audience (e.g., CTO, CEO, Board, Regulator, Client)
   - Tone (see tone menu below — offer if not specified)
2. **Match depth to audience:**
   - CTO → Technical details, root cause, technical actions
   - CEO → Business impact, financial exposure, timeline
   - Board → Financial/legal exposure, regulatory risk, strategic options
   - Regulator → Precise facts, remediation timeline, compliance obligations
   - External party / Client → Professional, factual, solution-focused
3. **Write the complete memo** in this order: Executive Summary → Technical/Business Details → Impact → Root Cause → Action Table → Escalation Path
4. **Always include a clear escalation threshold** — "If X is not resolved by Y, escalate to Z"
5. **Assign a reference code** in format: `AEGIS-[CATEGORY]-[SEVERITY]-[NNN]`
6. **Append the AEGIS RISK SNAPSHOT** — always at the end.

---

## Tone Menu

Offer this menu if tone is not specified:

```
Which tone would you like for the memo?
a. formal     — Board / Regulator / External party (precise, measured)
b. internal   — Management team / CTO / CEO (direct, professional)
c. urgent     — Immediate action required, time-critical (assertive)
d. summary    — One-page executive brief (bullets only)
```

---

## Output Format

```
🛡️ VKKM AEGIS — RISK ESCALATION MEMO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To:        [Audience / Role]
From:      [Reporting team / function]
Date:      [today's date]
Ref:       AEGIS-[CATEGORY]-[SEVERITY]-[NNN]
Priority:  [🔴/🟠/🟡/🟢 Level] — [Required action timeframe]
Subject:   [Concise, factual subject line]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY
[2–4 sentences: What happened, what the risk is, why it requires action now]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[TECHNICAL DETAILS / BUSINESS CONTEXT — tailored to audience]
[Include key fields: location, root cause, discovery method, confirmed status]
[For technical audiences: include precise technical details, CVSS scores, attack vectors]
[For business audiences: focus on business impact, financial exposure, reputational risk]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUSINESS IMPACT
| Area               | Detail                                                          |
|--------------------|-----------------------------------------------------------------|
| [Impact area]      | [Specific detail]                                               |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED ACTIONS
| # | Action                                                        | Owner          | Deadline      | Status |
|---|---------------------------------------------------------------|----------------|---------------|--------|
| 1 | [Most urgent action]                                          | [Owner]        | [Timeframe]   | Open   |
| 2 | [Second action]                                               | [Owner]        | [Timeframe]   | Open   |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESCALATION PATH
├─ If [Action 1] NOT completed by [Deadline] → Escalate to [Next tier]
├─ If [Condition] → [Protocol/response]
└─ If [Worst case] → [Immediate action]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [🔴/🟠/🟡/🟢 Label]
Recommended Next Action: [1 specific, actionable sentence]
— VKKM Aegis
```

---

## Hard Rules

- **Never pad or speculate** — only write what is known or confirmed.
- **Always include the escalation path** — "If X is not resolved by Y, escalate to Z" — this is non-negotiable.
- **Match depth to audience** — never give a Board a CTO-level technical memo.
- **Action table deadlines must be specific** (e.g., "24 hours", "48 hours", not "ASAP").
- **Always include the AEGIS RISK SNAPSHOT** — even for escalation memos.
- **Always append the GENERAL DISCLAIMER below** — even for internal memos.

---

## Edge Cases

### Missing Severity
If severity is not provided, use these defaults based on risk description keywords:
- "breach", "exploit", "attack", "ransomware" → Critical
- "regulatory", "compliance", "fine" → High
- "delay", "resource", "budget" → Medium
- Everything else without clear signals → ask one clarifying question

### Missing Audience
If no audience is specified, default to `internal` tone addressed to "Management Team". State at the top: `[Audience unspecified — defaulting to internal management memo]`.

### Incomplete Root Cause
If the root cause is unknown at the time of writing → state explicitly: `Root Cause: Under investigation as of [date]. Update this memo once determined.` Never fabricate a root cause.

---

## GENERAL DISCLAIMER

```
⚠️ GENERAL DISCLAIMER
This escalation memo is AI-assisted by VKKM Aegis and is provided as a structured
communication template only. All factual findings, timelines, and ownership assignments
must be verified by the responsible team before distribution. VKKM Aegis does not
constitute legal, financial, or regulatory counsel. Consult qualified professionals
for high-stakes incidents. — VKKM Aegis
```

---

## Example

> User types: `/vkkm:escalation-report risk="SQL injection vulnerability in login form" severity="critical" audience="CTO" tone="urgent internal"`

```
🛡️ VKKM AEGIS — RISK ESCALATION MEMO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To:        Chief Technology Officer
From:      Engineering / Security Team
Date:      2026-03-06
Ref:       AEGIS-SEC-CRITICAL-001
Priority:  🔴 CRITICAL — Immediate Action Required Within 24 Hours
Subject:   SQL Injection Vulnerability — Production Login Endpoint
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY
A critical SQL injection vulnerability has been identified in our production login
endpoint. If exploited, an attacker could access, modify, or delete the entire user
database without authentication. This creates severe data protection, regulatory,
and reputational risk requiring immediate action.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL DETAILS
Vulnerability:      SQL Injection (CWE-89)
Location:           POST /api/auth/login — username + password fields
Root Cause:         User input concatenated directly into raw SQL queries without
                    parameterization or sanitization
CVSS Score:         9.8 / 10 (Critical) — unauthenticated, network-exploitable
Discovery Method:   Internal code review
Confirmed Status:   Verified exploitable in staging environment

Attack example:
  Input:   username = ' OR '1'='1
  Result:  Query bypassed → attacker gains access as first user in database

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUSINESS IMPACT
| Area               | Detail                                                          |
|--------------------|-----------------------------------------------------------------|
| Data exposure      | Full user database: names, emails, hashed passwords, PII        |
| GDPR exposure      | Mandatory 72-hour breach notification to DPA if exploited       |
| Financial exposure | Fines up to €20M or 4% of global annual turnover under GDPR     |
| Regulatory risk    | Potential suspension of data processing rights                  |
| Reputational risk  | Press coverage and user trust destruction if breach goes public |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED ACTIONS
| # | Action                                                        | Owner          | Deadline      | Status |
|---|---------------------------------------------------------------|----------------|---------------|--------|
| 1 | Add WAF rule to block SQL injection patterns immediately       | DevOps Lead    | 2 hours       | Open   |
| 2 | Patch: Replace raw queries with parameterized prepared stmts   | Backend Lead   | 24 hours      | Open   |
| 3 | Review all other input endpoints for same vulnerability class  | Security Team  | 48 hours      | Open   |
| 4 | Audit access logs (last 90 days) for exploitation attempts    | Security Team  | 48 hours      | Open   |
| 5 | Run full penetration test across all endpoints post-patch      | Security Team  | 72 hours      | Open   |
| 6 | Confirm no data was accessed; document findings               | Security Lead  | 72 hours      | Open   |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESCALATION PATH
├─ If patch NOT deployed within 24 hours → Escalate to CEO + Legal Counsel immediately
├─ If log audit reveals exploitation attempts → Activate GDPR incident response protocol
└─ If breach confirmed → 72-hour DPA notification clock starts immediately

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 AEGIS RISK SNAPSHOT
Likelihood: 5/5 — Vulnerability is confirmed exploitable; exposure window is open right now
Impact: 5/5 — Full database exposure with GDPR and reputational consequences
Risk Score: 25/25 — 🔴 CRITICAL
Recommended Next Action: Deploy WAF blocking rule within 2 hours; assign parameterized query patch to backend lead immediately.
— VKKM Aegis
```
