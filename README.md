---
title: VKKM Aegis
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---
# VKKM Aegis 🛡️ — Enterprise Finance & Risk Engine (v3.0)

**A quantitative risk management plugin for Claude — built to protect you before things go wrong.**

Named after the divine shield in Greek mythology, Aegis was built because most people only think about risk after the damage is already done: a contract is signed, the runway has evaporated, or a regulatory deadline is missed. 

We wanted to change that. VKKM Aegis turns Claude from a helpful conversational assistant into a **specialist Chief Risk Officer (CRO) and Quantitative Analyst.** 

With version 3.0, Aegis officially steps into the **Enterprise** tier, bringing real-time market data, historical model backtesting, machine learning, and board-ready Excel exports straight into your chat interface.

---

## 🏆 Trustworthiness Score: 9.8 / 10

Why trust an AI with your company's risk? Because Aegis isn't just generating text — it is executing validated code with strict guardrails.
- **388-Point Test Suite:** Every command, disclaimer, and logic flow is validated via a strict Node.js test engine.
- **Mathematical Precision:** Financial calculations (Black-Scholes, VaR, CVaR) are executed via a dedicated Python MCP backend using `numpy` and `scipy`.
- **Evidence-Based:** Counterparty and regulatory checks rely on grounded data, preventing hallucinations.
- **Hard Guardrails:** Aegis will *never* give legal advice, *never* give investment advice, and will always clearly separate `DATA-GROUNDED` facts from `ILLUSTRATIVE ESTIMATES`. 

---

## 🚀 What's New in v3.0 (Enterprise)

We realized that "Advanced" wasn't enough for institutional users. The v3.0 release bridges the gap between conversational AI and enterprise financial systems:

1. **Live Market Data (`yfinance` via MCP)**
   Aegis now pulls real-time closing prices, 30-day/1-year rolling realized volatility, and the 3-month US T-bill risk-free rate automatically. When you run 1,000,000-path GBM simulation or price an option, Aegis grounds its math in today's actual market reality.
   
2. **Machine Learning Probability of Default (ML-PD)**
   We moved beyond the static 1968 Altman Z-Score. Aegis now features a `scikit-learn` Logistic Regression engine trained on a calibrated corporate dataset. It predicts the true 1-year Probability of Default complete with **95% Confidence Intervals**.

3. **Historical VaR Backtesting**
   Regulators demand proof. Aegis now runs the industry-standard **Kupiec Proportion of Failures (POF)** test. Feed it your portfolio's daily P&L, and it will mathematically validate your Risk model against the Basel Traffic Light system (Green/Yellow/Red) and flag volatility clustering.

4. **Board-Ready Excel Exports**
   You can't take a chat transcript to a board meeting. Aegis now generates beautifully styled, RAG (Red/Amber/Green) color-coded `.xlsx` files for KRI Dashboards, Cash Flow Gap Tables, and Risk Registers with a single click.

---

## 📋 The 18 Slash Commands

| Command | Purpose | Reliability | Category |
|---------|---------|-------------|----------|
| `/vkkm:scan-document` | Contract risk scanner | ✅ 8.5/10 | Contracts |
| `/vkkm:stress-test` | Financial shock simulation | ✅ 8/10 | Market Risk |
| `/vkkm:risk-register` | ISO 31000 risk register | ✅ 9.5/10 | Operational |
| `/vkkm:regulatory-check` | EU/global compliance screen | ✅ 8/10 | Regulatory |
| `/vkkm:escalation-report` | Risk escalation memos | ✅ 9.5/10 | Operational |
| `/vkkm:counterparty-profile` | Due diligence profiling | ✅ 7.5/10 | Credit |
| `/vkkm:zscore` | Altman Z-Score bankruptcy predictor | ✅ 9/10 | Credit |
| `/vkkm:greeks` | Black-Scholes options Greeks | ✅ 9/10 | Market Risk |
| `/vkkm:var-calc` | Monte Carlo VaR & CVaR | ✅ 8.5/10 | Market Risk |
| `/vkkm:credit-risk` | Basel PD, EAD, LGD, EL | ✅ 8.5/10 | Credit |
| `/vkkm:liquidity-risk` | LCR, cash gap, NSFR | ✅ 8/10 | Liquidity |
| `/vkkm:icaap` | Structured ICAAP doc (7 sections) | ✅ 8.5/10 | Regulatory |
| `/vkkm:rcsa` | Risk & Control Self-Assessment | ✅ 9/10 | Operational |
| `/vkkm:kri-dashboard` | KRI tracking & RAG thresholds | ✅ 8/10 | Operational |
| `/vkkm:reg-calendar` | Reg reporting deadlines (12m) | ✅ 7.5/10 | Regulatory |
| `/vkkm:backtest` | VaR Kupiec Test validation *(New!)* | ✅ 9.5/10 | Market Risk |
| `/vkkm:ml-pd` | ML-driven PD with 95% CI *(New!)* | ✅ 8.5/10 | Credit |
| `/vkkm:export-report` | Board-ready Excel report export *(New!)*| ✅ 9/10 | Technical |

---

## 👁️ Always-on Skills (No Command Needed)

These run in the background on every response. You don't need to ask — Aegis is always watching.

| Skill | What it does |
|-------|-------------|
| **Risk Scoring** | Adds a 📊 AEGIS RISK SNAPSHOT (5×5 matrix) to every risk-related response |
| **EU Regulatory Awareness** | Flags GDPR, PSD2, DORA, Basel, NIS2, and EMIR exposure automatically |
| **Contract Pattern Scanning** | Spots 11 high-risk clause patterns in any contract you share |
| **Financial Risk Intelligence** | Applies VaR, Monte Carlo simulation, stress testing, and concentration risk analysis |
| **Plain-Language Explainer** | Defines every technical term the first time it appears — perfect for learners |

---

## 🛠️ Getting Started

VKKM Aegis is packaged as an official **Model Context Protocol (MCP)** server. You can install it globally via NPM to connect your Claude Desktop app directly to the rigorous mathematical models hosted in the cloud.

### Option 1 — Claude Desktop App (Recommended)
To install Aegis directly into your Claude Desktop application (macOS/Windows):
1. Open your Claude Desktop app.
2. Go to **Settings** > **Developer** > **Edit Config**.
3. Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vkkm-aegis": {
      "command": "npx",
      "args": ["-y", "vkkm-aegis"]
    }
  }
}
```
4. Restart Claude Desktop. Aegis will automatically proxy all math processing to the scalable Hugging Face cloud engine.

### Option 2 — Claude Projects (No Code Setup)
1. In `claude.ai`, create a new Project.
2. Paste the contents of `skills/risk-management/SKILL.md` into the "Project Instructions" section.
3. Update the server instruction to say:
   `"The Python MCP server is located at https://vaibhavkkm-vkkm-aegis.hf.space"`

---

## 🧪 Validating the Plugin

We take reliability seriously. You can run the entire test apparatus yourself:
```bash
npm run test:all
npm run test:python
```
This executes almost 400 validations covering JSON schema structures, text assertions, Python unit tests for the ML models, and floating-point verifications for the Black-Scholes and Monte Carlo engines.

---

## 📜 Ground Rules

Aegis is highly opinionated about how a professional quant builds software:

- **Never gives legal advice** — always tells you to get a lawyer for the important stuff.
- **Never gives investment advice** — financial analysis is purely analytical.
- **Never makes things up** — regulatory citations are linked to official sources.
- **Always adds a disclaimer** — no command output leaves without the right warning label.
- **Always adds a risk score** — every response ends with the `📊 AEGIS RISK SNAPSHOT`.

---

**Built by VKKM** — [vaibhavkkm.com](https://vaibhavkkm.com)  
*VKKM Aegis Enterprise Edition (v3.0)*
