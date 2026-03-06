# Changelog

## v1.1 — 6 March 2026

The big improvement in this release is the test suite. Previously there was no way to know programmatically whether the plugin was fully intact — now there is. Run `npm test` and you get 190 checks across file structure, JSON validity, command spec completeness, disclaimer coverage, risk scoring consistency, and EU regulation accuracy.

A few gaps that slipped through in v1.0 were also fixed:

- `plugin.json` was missing the `system_prompt` inline field, which Claude Code and direct API callers need. Added, along with per-command metadata in a new `command_specs` array and a `skills_paths` list.
- `risk-register.md` and `escalation-report.md` were both missing disclaimer blocks — fixed and each given a proper edge cases section to handle vague inputs, unknown root causes, and varying project complexity.
- `eu-regulations.md` now explicitly states DORA's effective date (17 January 2025) and NIS2's effective date (18 October 2024). They were referenced but the dates weren't there.

**What's new:**
- `tests/validate.js` — validation suite, 190 assertions, no npm dependencies
- `tests/fixtures/` — sample contract, portfolio, and project brief for manual testing
- `tests/README.md` — per-command manual test checklists
- `.claude-plugin/schema.json` — JSON Schema for plugin.json validation
- `schemas/mcp-schema.json` — JSON Schema for .mcp.json validation
- `package.json`, `.gitignore`, `CHANGELOG.md`

---

## v1.0 — 6 March 2026

First release. Built the entire plugin from scratch based on the VKKM Aegis specification:

- Master prompt at `skills/risk-management/SKILL.md` (canonical copy at `skills/vkkm-aegis/SKILL.md`)
- Plugin manifest at `.claude-plugin/plugin.json`
- MCP connector config at `.mcp.json` (FactSet, MSCI, Google Drive, DocuSign, SharePoint)
- Six slash command specs: `scan-document`, `stress-test`, `risk-register`, `regulatory-check`, `escalation-report`, `counterparty-profile`
- Six always-active skill files: `risk-scoring`, `eu-regulations`, `contract-patterns`, `financial-risk`, `plain-language`, `disclaimers`

---

*VKKM Aegis — by Vaibhav Mangroliya | vaibhavkkm.com*
