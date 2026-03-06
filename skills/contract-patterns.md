# Skill: Contract Risk Pattern Recognition

**Plugin:** VKKM Aegis v1.0  
**Activation:** Always-active — apply automatically whenever any contract text, clause, or legal document is shared. Never wait to be asked.

---

## Rule

When the user shares any contract text, agreement excerpt, NDA, SLA, employment contract, or any clause from a legal document — automatically scan for all high-risk and low-risk patterns below, and present findings in the clause findings table. Do not wait for the user to ask.

---

## 🔴 HIGH RISK Patterns — Always Flag

Scan for each of these and flag immediately if found (or if conspicuously absent):

| Pattern | Why It's High Risk | What to Recommend |
|---------|------------------|--------------------|
| **Termination without notice or cause** | Leaves the user vulnerable to instant contract end with no compensation | Negotiate minimum notice period (14–30 days) + kill fee for work completed |
| **Unlimited liability on the user's side** | A small contract could expose the user to unlimited financial claims | Cap liability at total contract value — standard market practice |
| **Missing IP ownership / assignment clause** | Without it, ownership of created work is legally ambiguous | Add explicit clause: IP transfers upon receipt of full payment |
| **Vague or missing payment terms** | Disputes over payment timing are the #1 contract dispute | Define: payment amount, due date, late payment interest rate (e.g., 1.5%/month) |
| **Auto-renewal with opt-out window under 30 days** | Short opt-out windows trap users in unwanted renewals | Negotiate minimum 30-day opt-out window with written notice requirement |
| **Jurisdiction set to an unfavorable or foreign territory** | Legal disputes in foreign courts are expensive and unpredictable | Negotiate governing law to user's home jurisdiction |
| **Missing or one-sided NDA / confidentiality clause** | User's confidential information may not be protected | Add mutual NDA with clear definition of what constitutes confidential information |
| **Force majeure clause missing, too broad, or too narrow** | Leaves critical events (pandemics, cyberattacks, natural disasters) legally unclear | Add balanced force majeure clause covering specific, named events |
| **Penalty / indemnity clauses with no financial cap** | Exposes user to disproportionate financial claims | Cap indemnity/penalty at total contract value or a defined fixed amount |
| **Unilateral amendment rights** | Other party can change terms without the user's consent | Require mutual written consent for any contract amendments |
| **Missing dispute resolution process** | No defined process = expensive litigation by default | Add escalation path: negotiation → mediation → arbitration → court |

---

## 🟢 LOW RISK Signals — Confirm and Reassure

Identify these positive signals and confirm they are well-drafted:

| Signal | Why It's Good | What to Note |
|--------|--------------|------------|
| **Clear payment terms with due dates** | Reduces payment disputes and cash flow risk | Confirm due date, late payment interest rate, and invoicing process |
| **Defined deliverables and written acceptance criteria** | Prevents scope creep and "work rejection" disputes | Confirm acceptance criteria are objective and measurable |
| **Capped mutual liability** | Both parties share risk fairly | Confirm the cap amount is proportionate to contract value |
| **Mutual NDA in place** | Both parties' information is protected | Confirm the definition of "confidential information" is clear |
| **Defined termination process with adequate notice** | Both parties know exactly how to exit | Confirm notice period is sufficient (minimum 14 days) |
| **Governing law clearly stated** | Clear jurisdiction reduces legal uncertainty | Confirm the jurisdiction is favorable to the user |

---

## Clause Table Format (Always Use This Structure)

Present every finding in this table — never present contract findings as plain prose:

```
| Clause     | Finding                                           | Risk Level   | Recommendation                                                     |
|------------|---------------------------------------------------|--------------|---------------------------------------------------------------------|
| Clause X.X | [What was found — quote the clause briefly]       | 🔴 Critical  | [Specific negotiation or fix]                                      |
| Clause X.X | [Positive finding]                                | 🟢 Low       | No action needed — well drafted                                    |
```

---

## Hard Rules

- **Scan automatically** — never wait for the user to ask "what do you think of this clause?"
- **Always scan for all 11 high-risk patterns** — even if only 1–2 clauses are shared (user may have shared a subset)
- **If a critical clause is missing entirely** — flag it as a finding with Risk Level 🔴 Critical
- **Never give legal advice** — always recommend professional legal review for high-stakes contracts
- **Always follow the clause table** with the Legal Disclaimer and AEGIS RISK SNAPSHOT
