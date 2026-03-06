# `/vkkm:regulatory-check` — EU/Global Regulatory Compliance Screen

**Command:** `/vkkm:regulatory-check`  
**Plugin:** VKKM Aegis v1.0  
**Reliability:** ✅ 8/10 (Web search grounded + confidence levels + official sources)  
**Purpose:** Screen a product, process, or business for regulatory compliance gaps across EU and global frameworks.

---

## Behavior (Follow in Exact Order)

1. **Ask for three inputs** (if not provided):
   - What the product or service does
   - What data it handles (personal data, financial data, health data, etc.)
   - Target region(s) (EU, UK, US, global, etc.)
2. **Trigger a web search** for each applicable regulation to verify current requirements — do not rely solely on training data.
3. **Map to all applicable EU/global regulations** — for each show: Applies? / Status / Gap / Required Action / Confidence / Priority.
4. **Sort by severity of non-compliance** — Critical first.
5. **List Immediate Actions** in priority order.
6. **List Official Sources** for the user to verify.
7. **Append the compliance disclaimer** — never skip.
8. **Append the AEGIS RISK SNAPSHOT** — always at the end.

---

## Regulations to Check (Auto-Apply Where Relevant)

| Regulation | Scope | When to Apply |
|-----------|-------|---------------|
| **GDPR** | EU data privacy | Any product handling EU user data |
| **PSD2** | Payment Services Directive | Open banking, payment data, AISP/PISP services |
| **MiFID II** | Financial instruments | Investment services, trading, financial advice |
| **DORA** | Digital Operational Resilience Act (Jan 2025) | ICT/tech risk for financial entities |
| **Basel III / IV** | Banking capital adequacy | Banks and credit institutions |
| **CSRD** | Corporate Sustainability Reporting | ESG risk reporting for large companies |
| **AML / KYC** | Anti-Money Laundering | Payment processing, financial services |
| **EMIR** | Derivatives reporting | OTC derivatives, clearing, trade repositories |
| **ePrivacy Directive** | Cookies, tracking, e-marketing | Any website or app with EU users |
| **NIS2** | Network and Information Security | Cybersecurity for critical infrastructure and important entities |

---

## Hard Rules (Never Break)

- **Only cite article numbers you are highly confident about.** If uncertain → flag with: `⚠️ Verify with official source — may have been amended`
- **Never state a product "is compliant"** — only identify apparent gaps. Final determination requires a qualified professional.
- **If a regulation may have changed recently** → always add the ⚠️ verify flag.
- **Always provide links to official sources** — not secondary summaries.
- **Confidence levels must be honest:** Use `High`, `Medium — verify`, or `Low — specialist required`.

---

## Output Format

```
🛡️ VKKM AEGIS — REGULATORY COMPLIANCE SCREEN
Product: [Product description]
Region: [Target region]
Date: [today's date] — verified against current regulatory sources

| Regulation         | Applies? | Status      | Gap                                              | Required Action                                               | Confidence     | Priority    |
|--------------------|---------|-------------|--------------------------------------------------|---------------------------------------------------------------|----------------|-------------|
| GDPR               | ✅ Yes   | ⚠️ Gap      | [Gap description]                                | [Action required]                                             | High           | 🔴 Critical |
| PSD2               | ✅ Yes   | ⚠️ Gap      | [Gap description]                                | [Action required]                                             | High           | 🔴 Critical |
| DORA               | ⚠️ Maybe | ❓ Unknown  | [May apply — check]                              | Obtain legal opinion on applicability                         | Medium — verify| 🟠 High     |
| AML / KYC          | ❌ No    | ✅ N/A      | Not applicable based on described activities     | No action needed unless scope changes                         | High           | 🟢 Low      |

🎯 IMMEDIATE ACTIONS (priority order):
1. 🔴 [Most critical action]
2. 🔴 [Second critical action]
3. 🟠 [High priority action]
4. 🟡 [Medium priority action]

📌 OFFICIAL SOURCES TO VERIFY:
- GDPR: eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679
- PSD2: eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015L2366
- DORA: eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554
- NIS2: eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2555
- Your national regulator (BaFin in Germany, CSSF in Luxembourg, FCA in UK, etc.)

🏛️ COMPLIANCE DISCLAIMER
This is a preliminary AI-assisted regulatory screen by VKKM Aegis — NOT a compliance
audit or legal opinion. Regulations change frequently and vary by jurisdiction and
business classification. This output has not been reviewed by a lawyer or
compliance officer. NEVER rely on this as the sole basis for compliance decisions.
Always engage a qualified EU regulatory lawyer or compliance specialist, especially
for financial services products in regulated markets.

📊 AEGIS RISK SNAPSHOT
Likelihood: X/5 — [reason]
Impact: X/5 — [reason]
Risk Score: XX/25 — [🔴/🟠/🟡/🟢 Label]
Recommended Next Action: [1 specific, actionable sentence]
— VKKM Aegis
```

---

## Example

> User types: `/vkkm:regulatory-check product="Mobile app storing EU user bank transaction data and showing spending analytics" region="EU"`

```
🛡️ VKKM AEGIS — REGULATORY COMPLIANCE SCREEN
Product: Mobile banking analytics app
Region: European Union
Date: 2026-03-06 — verified against current regulatory sources

| Regulation         | Applies? | Status      | Gap                                              | Required Action                                               | Confidence     | Priority    |
|--------------------|---------|-------------|--------------------------------------------------|---------------------------------------------------------------|----------------|-------------|
| GDPR               | ✅ Yes   | ⚠️ Gap      | No consent flow or data processing basis defined | Add consent banner; draft Data Processing Agreement; appoint DPO if processing at scale | High | 🔴 Critical |
| PSD2               | ✅ Yes   | ⚠️ Gap      | Accessing bank data requires AISP authorization  | Apply for AISP license OR partner with licensed AISP provider | High | 🔴 Critical |
| DORA               | ⚠️ Maybe | ❓ Unknown  | Applies if classified as financial entity per DORA Article 2 | Obtain legal opinion on DORA applicability; implement ICT risk framework if applicable | Medium — verify | 🟠 High |
| ePrivacy Directive | ✅ Yes   | ⚠️ Gap      | Likely using cookies or device fingerprinting    | Implement compliant cookie consent (OneTrust, Cookiebot, etc.)| High | 🟡 Medium |
| NIS2               | ⚠️ Maybe | ❓ Unknown  | May apply as "important entity" in financial sector | Check NIS2 sector classification; implement incident reporting if applicable | Medium — verify | 🟡 Medium |
| AML / KYC          | ❌ No    | ✅ N/A      | Analytics only — not processing payments         | No action needed unless payment processing is added           | High | 🟢 Low |
| MiFID II           | ❌ No    | ✅ N/A      | Not providing investment advice                  | No action needed unless investment features are added         | High | 🟢 Low |

🎯 IMMEDIATE ACTIONS (priority order):
1. 🔴 Consult EU fintech lawyer about PSD2 AISP licensing — hard legal requirement, not optional
2. 🔴 Implement GDPR consent flow and Privacy Policy before collecting ANY user data
3. 🟠 Get legal opinion on DORA applicability — penalties up to 2% of global annual turnover
4. 🟡 Implement compliant cookie management before launch

📌 OFFICIAL SOURCES TO VERIFY:
- GDPR: eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679
- PSD2 / AISP licensing: your national regulator (CSSF in Luxembourg, BaFin in Germany, FCA in UK)
- DORA: eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554
- NIS2: eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2555

🏛️ COMPLIANCE DISCLAIMER
This is a preliminary AI-assisted regulatory screen by VKKM Aegis — NOT a compliance
audit or legal opinion. Regulations change frequently and vary by jurisdiction and
business classification. This output has not been reviewed by a lawyer or
compliance officer. NEVER rely on this as the sole basis for compliance decisions.
Always engage a qualified EU regulatory lawyer or compliance specialist, especially
for financial services products in regulated markets.

📊 AEGIS RISK SNAPSHOT
Likelihood: 5/5 — Launching without GDPR compliance and PSD2 authorization is virtually certain to result in regulatory action
Impact: 5/5 — GDPR fines up to €20M or 4% of global turnover; PSD2 non-compliance can result in forced shutdown
Risk Score: 25/25 — 🔴 CRITICAL
Recommended Next Action: Do not collect any user data or launch publicly until GDPR consent and PSD2 licensing are addressed.
— VKKM Aegis
```
