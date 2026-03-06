# VKKM Aegis 🛡️

**A risk management plugin for Claude — built to protect you before things go wrong.**

Named after the divine shield in Greek mythology, Aegis was built because most people only think about risk after they've already signed the contract, run out of runway, or missed a regulatory deadline.

This plugin changes that.

---

## What it does

VKKM Aegis turns Claude into a specialist risk analyst. It handles six high-value risk scenarios through slash commands, and runs five background skills on every response — so it's always watching, whether you ask it to or not.

Built for freelancers, founders, project managers, finance teams, and anyone who's ever been blindsided by a clause they didn't read carefully enough.

---

## Commands

| Command | What it does | Reliability |
|---------|-------------|-------------|
| `/vkkm:scan-document` | Scans contracts for dangerous clauses — unlimited liability, missing IP ownership, auto-renewal traps, and more | 8.5/10 |
| `/vkkm:stress-test` | Runs financial shock scenarios (rate hikes, market crashes, FX swings, client loss) against your portfolio or business | 8/10 |
| `/vkkm:risk-register` | Builds a complete ISO 31000 risk register with likelihood, impact, owners, and contingency plans | 9.5/10 |
| `/vkkm:regulatory-check` | Screens your product or business for EU regulatory gaps — GDPR, PSD2, DORA, MiFID II, NIS2, and more | 8/10 |
| `/vkkm:escalation-report` | Writes a proper escalation memo for your CTO, CEO, Board, or regulator — with the right tone for each audience | 9.5/10 |
| `/vkkm:counterparty-profile` | Researches a supplier, client, or business partner before you sign anything | 7.5/10 |

---

## Always-on skills (no command needed)

These run in the background on every response. You don't need to ask.

| Skill | What it does |
|-------|-------------|
| **Risk Scoring** | Adds a 📊 AEGIS RISK SNAPSHOT (5×5 matrix) to every risk-related response |
| **EU Regulatory Awareness** | Flags GDPR, PSD2, DORA, MiFID II, NIS2, and EMIR exposure automatically |
| **Contract Pattern Scanning** | Spots 11 high-risk clause patterns in any contract you share |
| **Financial Risk Intelligence** | Applies VaR, Monte Carlo simulation, stress testing, and concentration risk analysis |
| **Plain-Language Mode** | Defines every technical term the first time it appears — no assumed knowledge |

---

## Getting started

### Option 1 — Claude Projects / Custom Instructions (fastest)
Paste the full contents of `skills/risk-management/SKILL.md` as your custom instructions or system prompt. Done.

### Option 2 — Claude Cowork
The canonical skill path is already set up at `skills/vkkm-aegis/SKILL.md`. Load that as your active skill.

### Option 3 — API
Use `skills/risk-management/SKILL.md` as your system prompt. The `plugin.json` manifest is already configured with the inline `system_prompt` field for API callers.

### Option 4 — Live data connectors (optional)
Configure `.mcp.json` with your API keys to go from *Illustrative Estimate* mode to *Data-Grounded* mode:

| Connector | What it unlocks |
|-----------|----------------|
| **FactSet** | Live market data — equities, bonds, FX, risk factors |
| **MSCI** | Index data, ESG risk factors, factor models |
| **Google Drive** | Batch contract scanning directly from Drive |
| **DocuSign** | Contract ingestion straight from envelopes |
| **SharePoint** | Enterprise document access |

> Without connectors, all financial outputs carry the `📊 ILLUSTRATIVE ESTIMATE` label automatically.

---

## Running the validation suite

```bash
npm test
```

This runs a zero-dependency Node.js test suite that checks everything — file structure, JSON validity, required sections in every command spec, correct disclaimers, risk score consistency, and more.

```
✅  VKKM Aegis Validation — ALL CHECKS PASSED (190/190)
```

See `tests/README.md` for the full manual testing guide with fixture files for each command.

---

## Project structure

```
vkkm-aegis-plugin/
├── .claude-plugin/
│   ├── plugin.json          ← Plugin manifest (name, commands, opening message, etc.)
│   └── schema.json          ← JSON Schema for validating plugin.json
├── .mcp.json                ← Live data connector config
├── schemas/
│   └── mcp-schema.json      ← JSON Schema for validating .mcp.json
├── commands/
│   ├── scan-document.md     ← /vkkm:scan-document
│   ├── stress-test.md       ← /vkkm:stress-test
│   ├── risk-register.md     ← /vkkm:risk-register
│   ├── regulatory-check.md  ← /vkkm:regulatory-check
│   ├── escalation-report.md ← /vkkm:escalation-report
│   └── counterparty-profile.md ← /vkkm:counterparty-profile
├── skills/
│   ├── risk-management/
│   │   └── SKILL.md         ← Master prompt (original)
│   ├── vkkm-aegis/
│   │   └── SKILL.md         ← Canonical Claude Cowork path
│   ├── risk-scoring.md      ← 5×5 matrix + AEGIS RISK SNAPSHOT
│   ├── eu-regulations.md    ← GDPR, PSD2, DORA, Basel, NIS2, EMIR, etc.
│   ├── contract-patterns.md ← High/low risk clause pattern library
│   ├── financial-risk.md    ← VaR, Monte Carlo, GBM, stress testing
│   ├── plain-language.md    ← 30+ term glossary, auto-defined on first use
│   └── disclaimers.md       ← Disclaimer templates for all five output types
├── tests/
│   ├── validate.js          ← Test suite (190 checks, no dependencies)
│   ├── README.md            ← Manual testing guide + per-command checklists
│   └── fixtures/
│       ├── sample-contract.txt    ← 15-clause freelance contract for scan-document
│       ├── sample-portfolio.json  ← 60/30/10 portfolio for stress-test
│       └── sample-project.md     ← Fintech SaaS brief for risk-register / regulatory-check
├── CHANGELOG.md
├── package.json
├── .gitignore
└── README.md
```

---

## Ground rules

Aegis is opinionated about a few things:

- **Never gives legal advice** — always tells you to get a lawyer for the important stuff
- **Never gives investment advice** — financial analysis is always labelled as illustrative
- **Never makes things up** — regulatory citations and counterparty findings are evidence-only
- **Always adds a disclaimer** — no command output leaves without the right one
- **Always adds a risk score** — every response ends with the 📊 AEGIS RISK SNAPSHOT
- **Max two clarifying questions** — it doesn't stall

---

## Troubleshooting

**Plugin isn't activating**
Make sure you've pasted the full contents of `skills/risk-management/SKILL.md` as your system prompt. It needs to be the entire file, not a summary.

**Commands aren't showing up**
Claude custom instructions don't natively support slash commands in all interfaces. Use natural language instead — just describe what you need and Aegis will handle it.

**Financial outputs look generic**
That's expected without a live data connector. All outputs in standalone mode are labelled `📊 ILLUSTRATIVE ESTIMATE` and use standard market assumptions. Connect FactSet or MSCI via `.mcp.json` for grounded analysis.

**Tests failing**
Run `node tests/validate.js` directly to see which specific checks are failing. Each failure shows the exact assertion and why it didn't pass.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

---

**Made by Vaibhav Mangroliya** — [vaibhavkkm.com](https://vaibhavkkm.com)  
VKKM Aegis Validation · v1.1 · March 2026
