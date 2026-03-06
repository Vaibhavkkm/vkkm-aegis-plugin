# VKKM Aegis — Test Suite

## Quick Start

```bash
# From the project root:
npm test
# OR
node tests/validate.js
```

**Expected output:**
```
✅  VKKM Aegis Validation — ALL CHECKS PASSED (190/190)
```

---

## What the Automated Tests Check

The test runner (`tests/validate.js`) runs **190 assertions** with zero external dependencies — only Node.js built-ins.

| Test Group | # Checks | What's Verified |
|-----------|---------|----------------|
| File Structure | 22 | All required files exist |
| JSON Validity | 5 | plugin.json, .mcp.json, schema.json, package.json are valid JSON |
| Plugin Manifest | 14 | Required fields, all 6 slash commands listed |
| MCP Connectors | 16 | All 5 connectors with label, purpose, auth |
| Command Files | 48 | Each of 6 commands has Behavior, Output, Hard Rules, Example, Disclaimer, Snapshot |
| Skill Files | 27 | Each always-active skill has required content |
| Master Prompt | 10 | SKILL.md references all 6 commands; both copies are identical |
| Disclaimers | 6 | All 5 disclaimer blocks present |
| Risk Scoring | 10 | Thresholds and emoji labels consistent |
| Command Content | 12 | Command-specific content (Trust Score, Escalation Path, ISO 31000, etc.) |
| EU Regulations | 10 | All 10 regulations covered with accurate dates |

---

## Manual Testing with Claude

Use the fixture files to manually validate each command output against its spec.

### Test 1 — `/vkkm:scan-document` (Contract Scanner)

1. Open Claude with VKKM Aegis active
2. Paste the contents of `tests/fixtures/sample-contract.txt`
3. Type: `/vkkm:scan-document`

**Expected output validates:**
- [ ] Clause table with Clause | Finding | Risk Level | Recommendation columns
- [ ] 🔴 Critical flags on: Clause 2 (payment terms), Clause 3 (IP), Clause 4 (termination), Clause 6 (unlimited liability), Clause 8 (unilateral amendments), Clause 11 (3-day auto-renewal opt-out)
- [ ] 🟢 Low flags on: Clause 12 (defined deliverables), Clause 13 (force majeure), Clause 14 (data protection language)
- [ ] Overall Document Risk Score: should be 7–9/10 (High)
- [ ] Top 3 Priority Actions listed
- [ ] ⚖️ LEGAL DISCLAIMER present
- [ ] 📊 AEGIS RISK SNAPSHOT present with — VKKM Aegis sign-off

---

### Test 2 — `/vkkm:stress-test` (Financial Stress Test)

1. Open Claude with VKKM Aegis active
2. Paste the contents of `tests/fixtures/sample-portfolio.json`
3. Type: `/vkkm:stress-test scenario="rate hike +200bps"`

**Expected output validates:**
- [ ] Before/After portfolio value table showing impact on bond holdings (duration-adjusted)
- [ ] 📊 ILLUSTRATIVE ESTIMATE label at the top (no live connector)
- [ ] Assumption row: Duration of bond portfolio = approx 6–9 years
- [ ] Equity multiple compression noted
- [ ] Mitigation options offered
- [ ] 💡 Learning Note present
- [ ] 💰 FINANCIAL DISCLAIMER present
- [ ] 📊 AEGIS RISK SNAPSHOT present

---

### Test 3 — `/vkkm:risk-register` (Risk Register)

1. Open Claude with VKKM Aegis active
2. Paste the contents of `tests/fixtures/sample-project.md`
3. Type: `/vkkm:risk-register`

**Expected output validates:**
- [ ] 8+ risks generated
- [ ] All 8 categories appear: Regulatory, Technical, Security, Financial, People, Market, Operational, Reputational
- [ ] R01 = PSD2 license not confirmed (🔴 Critical)
- [ ] Security row: OpenAI data processing + GDPR risk
- [ ] People row: single point of failure on core algorithm
- [ ] Scores sorted descending
- [ ] Register Summary with counts
- [ ] ⚠️ GENERAL DISCLAIMER present
- [ ] 📊 AEGIS RISK SNAPSHOT present

---

### Test 4 — `/vkkm:regulatory-check` (Regulatory Screen)

1. Open Claude with VKKM Aegis active
2. Paste the contents of `tests/fixtures/sample-project.md`
3. Type: `/vkkm:regulatory-check`

**Expected output validates:**
- [ ] GDPR flagged: OpenAI data processing DPA + Purpose Limitation
- [ ] PSD2 flagged: AISP license status not confirmed
- [ ] DORA noted: applies if categorized as financial entity
- [ ] ePrivacy flagged: cookies/tracking on web app
- [ ] AML/KYC checked: likely does not apply — note why
- [ ] Each regulation has Status | Gap | Action | Confidence | Priority
- [ ] Immediate Actions table
- [ ] Official sources listed (EUR-Lex links)
- [ ] 🏛️ COMPLIANCE DISCLAIMER present
- [ ] 📊 AEGIS RISK SNAPSHOT present

---

### Test 5 — `/vkkm:escalation-report` (Escalation Memo)

Type: `/vkkm:escalation-report risk="SQL injection found in login API endpoint" severity="critical" audience="CTO" tone="urgent"`

**Expected output validates:**
- [ ] AEGIS reference code: format `AEGIS-SEC-CRITICAL-NNN`
- [ ] EXECUTIVE SUMMARY section
- [ ] BUSINESS IMPACT table
- [ ] RECOMMENDED ACTIONS table with specific deadlines (not "ASAP")
- [ ] ESCALATION PATH with ├─ tree structure and "If X not done by Y → escalate to Z"
- [ ] ⚠️ GENERAL DISCLAIMER present
- [ ] 📊 AEGIS RISK SNAPSHOT present

---

### Test 6 — `/vkkm:counterparty-profile` (Counterparty Due Diligence)

Type: `/vkkm:counterparty-profile company="Acme Digital GmbH" country="Germany" deal="€40,000 website development contract"`

**Expected output validates:**
- [ ] Web search results cited with URLs (no fabricated facts)
- [ ] Data gaps section listing what could not be confirmed
- [ ] Trust Score: X/10 with clear rationale
- [ ] GO / CAUTION / NO-GO recommendation
- [ ] Protective Actions list
- [ ] 🔍 DUE DILIGENCE DISCLAIMER present
- [ ] 📊 AEGIS RISK SNAPSHOT present

---

## Interpreting Results

| Outcome | What It Means |
|---------|--------------|
| `npm test` exits 0, all ✅ | Plugin is structurally complete and spec-compliant |
| `npm test` exits 1, some ❌ | Run `node tests/validate.js` to see which specific assertions failed |
| Manual test fails | Output does not match the command spec — review the corresponding `commands/*.md` file |

---

*Tests written for VKKM Aegis v1.1 — VKKM (vaibhavkkm.com)*
