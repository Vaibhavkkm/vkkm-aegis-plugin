# Skill: Plain-Language Explainer

**Plugin:** VKKM Aegis v1.0  
**Activation:** Always-active — automatically define any technical term the first time it is used in a conversation.

---

## Rule

Whenever a technical term, acronym, regulatory name, financial concept, legal term, or risk framework is used for the **first time in a conversation** — immediately add a one-line plain-language definition inline, before continuing.

This applies whether the term is used by the user or by VKKM Aegis.

Format: `[Term] — [one-line plain-language definition]`

Do NOT repeat the definition if the term has already been defined earlier in the same conversation.

---

## Pre-Defined Glossary

Use these definitions as the default — always prefer plain language over technical jargon.

### Financial Terms

| Term | Plain-Language Definition |
|------|--------------------------|
| **VaR (Value at Risk)** | The maximum expected loss over a given period at a stated confidence level. A 1-day 95% VaR of €5,000 means there is a 5% chance you could lose more than €5,000 in a single day. |
| **Monte Carlo Simulation** | Instead of predicting one scenario, we simulate thousands of possible outcomes using random inputs to show the full range from best case to worst case. |
| **GBM (Geometric Brownian Motion)** | A mathematical model describing how asset prices move randomly over time — the standard assumption in options pricing and simulation models. |
| **Duration** | A measure of how sensitive a bond's price is to interest rate changes. A bond with 8-year duration loses ~8% of value for every 1% rise in rates. |
| **Convexity** | An adjustment to duration that accounts for the fact that the relationship between bond prices and interest rates is curved, not linear. |
| **Basis Points (bps)** | A unit of measurement for interest rates. 1 basis point = 0.01%. A 300bps rate rise = 3% increase in interest rates. |
| **Concentration Risk** | The risk of having too much exposure to a single asset, sector, geography, or counterparty — typically flagged above 20% exposure. |
| **Liquidity Risk** | The risk that an asset cannot be sold quickly without a significant price reduction. |
| **Correlation Risk** | The risk that assets which appear diversified actually move together in a crisis, reducing the expected benefit of diversification. |
| **Spread** | The difference in yield between two instruments (e.g., corporate bond vs. government bond). A wider spread = higher perceived credit risk. |
| **Stress Test** | Simulating what happens to a portfolio or business under an adverse event (rate hike, market crash, client loss) to measure potential losses. |

### Legal / Contract Terms

| Term | Plain-Language Definition |
|------|--------------------------|
| **NDA (Non-Disclosure Agreement)** | A contract that prevents parties from sharing confidential information with third parties. |
| **IP (Intellectual Property)** | Legal ownership over creative work — code, designs, documents, inventions. Without an IP clause, ownership may be legally ambiguous. |
| **Force Majeure** | A contract clause that excuses a party from performance due to unforeseeable events (natural disasters, pandemics, war). |
| **Indemnity** | A contractual obligation by one party to cover the losses or liabilities of another. |
| **Jurisdiction** | The country or region whose laws govern the contract and handle disputes. |
| **Governing Law** | The legal system that applies to a contract (e.g., "This agreement is governed by the laws of Germany"). |
| **Kill Fee** | A payment made to a contractor when a project is cancelled — compensation for lost expected revenue. |
| **SLA (Service Level Agreement)** | A contract defining the service standard expected, with penalties for non-compliance. |

### Regulatory Terms

| Term | Plain-Language Definition |
|------|--------------------------|
| **GDPR** | EU regulation that governs how companies collect, store, and process personal data from EU residents. Max fine: €20M or 4% of global annual turnover. |
| **PSD2** | EU law governing digital payment services. Requires a license (AISP/PISP) to access bank account data or initiate payments on behalf of users. |
| **DORA** | EU regulation (effective Jan 2025) requiring financial entities to manage ICT (tech) operational risk — covering resilience, incident reporting, and third-party ICT risk. |
| **MiFID II** | EU law regulating investment services — investment advice, trading, portfolio management, and financial instrument markets. |
| **AML/KYC** | Anti-Money Laundering (AML) laws require financial services companies to verify customer identity (Know Your Customer / KYC) and monitor for suspicious transactions. |
| **NIS2** | EU cybersecurity law (effective Oct 2024) requiring critical infrastructure and important-sector entities to implement cybersecurity measures and report incidents. |
| **EMIR** | EU regulation requiring reporting and central clearing of OTC (over-the-counter) derivative contracts. |
| **Basel III / IV** | International banking standards that set minimum capital and liquidity requirements for banks to remain solvent under stress. |
| **CVSS Score** | Common Vulnerability Scoring System — a standardized score from 0–10 rating the severity of a cybersecurity vulnerability. 9.0–10.0 = Critical. |
| **DPA (Data Protection Authority)** | The national regulator enforcing GDPR in each EU country (e.g., BaFin in Germany for financial regulation, CNIL in France for data protection). |
| **AISP (Account Information Service Provider)** | A PSD2-licensed entity that can access bank account information on behalf of a user. Requires authorization from the national regulator. |

### Risk Management Terms

| Term | Plain-Language Definition |
|------|--------------------------|
| **ISO 31000** | The international standard for risk management frameworks — defines principles, guidelines, and a risk management process. |
| **Risk Register** | A structured document listing all identified risks with their likelihood, impact, scores, owners, and mitigation strategies. |
| **Risk Matrix (5×5)** | A grid mapping Likelihood (1–5) against Impact (1–5) to produce a Risk Score (1–25). Higher scores = higher priority. |
| **Contingency Plan** | A pre-planned response that activates IF a risk event actually occurs — distinct from a mitigation strategy (which tries to prevent it). |
| **Mitigation Strategy** | An action taken before a risk event occurs to reduce its likelihood or impact. |
| **Escalation Path** | A predefined chain of authority — who to notify and who takes over if a risk exceeds a defined threshold. |

---

## Hard Rules

- **Define on first use only** — do not repeat definitions already given in the conversation.
- **Keep definitions to one sentence** — never write a paragraph when a sentence works.
- **Always use plain language** — no jargon in the explanation of jargon.
- **Add a 📚 Learning Note** for student or learner users to expand on the concept with a practical example.
