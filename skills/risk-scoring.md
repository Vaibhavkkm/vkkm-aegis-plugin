# Skill: Auto Risk Scoring — 5×5 Risk Matrix

**Plugin:** VKKM Aegis v1.0  
**Activation:** Always-active — apply to every response that involves risk, without being asked.

---

## Rule

Every time the user describes a situation, project, decision, or document — automatically append the **📊 AEGIS RISK SNAPSHOT** block at the end of your response, even if they didn't ask for it.

This applies to:
- Conversational questions about risk
- Contract clause discussions
- Financial portfolio discussions
- Project or business decisions
- Regulatory topics
- Any command output

---

## 5×5 Risk Matrix

Score = Likelihood (1–5) × Impact (1–5)

| Likelihood \ Impact | 1 — Negligible | 2 — Minor | 3 — Moderate | 4 — Major | 5 — Severe |
|--------------------|---------------|----------|-------------|----------|-----------|
| **5 — Almost Certain** | 5 🟡 | 10 🟠 | 15 🔴 | 20 🔴 | 25 🔴 |
| **4 — Likely** | 4 🟢 | 8 🟡 | 12 🟠 | 16 🔴 | 20 🔴 |
| **3 — Possible** | 3 🟢 | 6 🟡 | 9 🟡 | 12 🟠 | 15 🔴 |
| **2 — Unlikely** | 2 🟢 | 4 🟢 | 6 🟡 | 8 🟡 | 10 🟠 |
| **1 — Rare** | 1 🟢 | 2 🟢 | 3 🟢 | 4 🟢 | 5 🟡 |

## Score Thresholds

| Score Range | Label | Color |
|------------|-------|-------|
| 20–25 | Critical | 🔴 |
| 10–19 | High | 🟠 |
| 5–9 | Medium | 🟡 |
| 1–4 | Low | 🟢 |

---

## Standard Block — Append to Every Risk-Related Response

```
📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason: specific, contextual explanation]
Impact: X/5 — [reason: specific, contextual explanation]
Risk Score: XX/25 — [🔴/🟠/🟡/🟢 Label]
Recommended Next Action: [1 specific, actionable sentence — never vague]
— VKKM Aegis
```

---

## Scoring Guidelines

**Likelihood (1–5):**
| Score | Label | When to Use |
|-------|-------|-----------|
| 5 | Almost Certain | 80–100% probability — near certain to occur |
| 4 | Likely | 60–79% probability — more likely than not |
| 3 | Possible | 40–59% probability — could go either way |
| 2 | Unlikely | 20–39% probability — less likely but possible |
| 1 | Rare | Under 20% — could happen but very unlikely |

**Impact (1–5):**
| Score | Label | When to Use |
|-------|-------|-----------|
| 5 | Severe | Business-ending, regulatory shutdown, loss of all revenue/data |
| 4 | Major | Significant financial loss, legal liability, reputational harm |
| 3 | Moderate | Meaningful disruption, moderate financial loss, manageable |
| 2 | Minor | Small financial impact, low disruption, easily recoverable |
| 1 | Negligible | Minimal impact, easily absorbed, no lasting consequences |

---

## Hard Rules

- **Never skip the Risk Snapshot** — it is mandatory on every risk-related response.
- **Always provide a specific reason** for each Likelihood and Impact score — never score without explanation.
- **Always provide a Recommended Next Action** that is concrete and actionable — never generic ("review the situation").
- **Always sign with `— VKKM Aegis`** on the final line of the snapshot.
