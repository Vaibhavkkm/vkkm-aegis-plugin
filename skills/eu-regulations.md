# Skill: EU Regulatory Awareness

**Plugin:** VKKM Aegis v1.0  
**Activation:** Always-active — apply automatically whenever the user's situation involves any of the regulations below. Never wait to be asked.

---

## Rule

When the user describes a product, business, project, or situation — automatically identify which EU/global regulations apply and flag compliance gaps without being asked.

---

## Regulations Scope Table

| Regulation | Full Name | Scope — Apply When |
|-----------|-----------|-------------------|
| **GDPR** | General Data Protection Regulation | Any product or service that collects, stores, or processes data from EU residents |
| **PSD2** | Payment Services Directive 2 | Open banking, payment initiation, account information services, strong customer authentication |
| **MiFID II** | Markets in Financial Instruments Directive II | Investment services, trading platforms, financial advice, order execution |
| **Basel III / IV** | Basel Capital Accords | Banks and credit institutions — capital adequacy, liquidity, leverage ratios |
| **DORA** | Digital Operational Resilience Act (effective Jan 2025) | ICT risk management for financial entities (banks, insurers, investment firms, crypto), their ICT third-party providers |
| **CSRD** | Corporate Sustainability Reporting Directive | ESG and climate risk reporting for large EU companies (250+ employees or €40M+ revenue) |
| **AML / KYC** | Anti-Money Laundering / Know Your Customer | Payment processing, financial services, cryptocurrency, high-value goods |
| **EMIR** | European Market Infrastructure Regulation | OTC derivatives, clearing, trade reporting to trade repositories |
| **ePrivacy Directive** | Cookie Directive / Privacy and Electronic Communications | Any website or app that places cookies, tracking pixels, or electronic marketing targeting EU users |
| **NIS2** | Network and Information Security Directive 2 (effective Oct 2024) | Cybersecurity incident reporting for essential and important entities in critical sectors |

---

## When to Flag a Regulation

Flag **GDPR** if: product collects names, emails, cookies, IP addresses, location data, behavioral data, or any identifier tied to an EU resident.

Flag **PSD2** if: product accesses bank account data, processes payments, initiates payment orders, or provides account information services.

Flag **MiFID II** if: product provides investment advice, executes orders, manages portfolios, or operates a trading venue.

Flag **DORA** if: product is an ICT service used by a financial entity, or the user IS a financial entity managing ICT risk.

Flag **CSRD** if: user is a large EU company required to publish ESG sustainability reports.

Flag **AML/KYC** if: product processes financial transactions, onboards customers for financial services, or deals in high-value goods (>€10,000 cash).

Flag **EMIR** if: product involves OTC derivatives clearing, reporting, or trade repository connections.

Flag **ePrivacy** if: product uses cookies, device fingerprinting, tracking, or sends electronic marketing to EU users.

Flag **NIS2** if: user operates in a critical sector (energy, transport, banking, health, digital infrastructure) with 50+ employees or €10M+ revenue.

---

## Output When a Regulation Applies

Always state:
1. Which regulation applies and why
2. The specific compliance gap (if any)
3. The required action
4. Confidence level (High / Medium — verify / Low — specialist required)

Use this format inline:

```
⚠️ [REGULATION] — [Applies / May apply / Does not apply]
Gap: [Specific gap description]
Required Action: [Specific action]
Confidence: [High / Medium — verify with official source / Low — seek specialist opinion]
```

---

## Hard Citation Rules (Never Break)

- **Only cite article numbers you are highly confident about.** If uncertain → add: `⚠️ Verify with official source — may have been amended`
- **Never state that a product "is compliant"** — only identify apparent gaps. Final determination requires a qualified professional.
- **If a regulation may have changed recently** → always add the verification warning.
- **Never fabricate penalty amounts** — only cite confirmed official figures (e.g., GDPR max fine = €20M or 4% of global annual turnover).

---

## Key Regulatory References (Official Sources)

| Regulation | Official Source |
|-----------|----------------|
| GDPR | eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679 |
| PSD2 | eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015L2366 |
| MiFID II | eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32014L0065 |
| DORA | eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554 |
| CSRD | eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2464 |
| NIS2 | eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2555 |
| EMIR | eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32012R0648 |
| AML (AMLD6) | eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32018L1673 |

Always direct users to official sources and their national regulatory authority (e.g., BaFin, CSSF, FCA, DNB) for jurisdiction-specific guidance.
