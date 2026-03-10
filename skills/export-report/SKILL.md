---
description: /vkkm:export-report — Structured Excel/JSON Report Generator
---

# /vkkm:export-report — Structured Excel/JSON Report Generator

## Behavior

When the user invokes `/vkkm:export-report`, generate a **downloadable structured report** from any prior VKKM Aegis command output. The report is delivered as a `.xlsx` file link (via the Python MCP server) or a complete JSON payload ready for system integration.

This command is always run **after** another command (e.g. `/vkkm:kri-dashboard`, `/vkkm:var-calc`, `/vkkm:liquidity-risk`) to export that command's structured output.

Supported export types:
- `kri` → KRI Dashboard (.xlsx with RAG colour-coding per cell)
- `gap-table` → Cash Flow Gap Analysis (.xlsx with conditional red formatting on shortfalls)
- `credit-risk` → Credit Risk Assessment (.xlsx with EL/UL/spread breakdown)
- `risk-register` → ISO 31000 Risk Register (.xlsx with score-based colouring)
- `backtest` → VaR Backtest Report (.xlsx with Basel zone highlighted)
- `json` → Any of the above as a structured JSON payload

**When the Python MCP server is connected:** Calls `POST /export/excel` or `POST /export/json` → returns a download URL or base64-encoded file.
**When offline:** Deliver the data in a clean Markdown table format and instruct the user to copy-paste into Excel, noting `⚠️ MCP server required for .xlsx generation`.

## Output Format

**When Excel export succeeds:**
```
📊 AEGIS REPORT GENERATED — [type] Export
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ DOWNLOAD READY
  File type : Excel (.xlsx)
  Report    : [report name]
  Contents  : [short description of sheets]
  Generated : [timestamp]
  Label     : DATA-GROUNDED / ILLUSTRATIVE ESTIMATE

SHEET SUMMARY
  Sheet 1 — [name] : [description]
  [...]

FORMATTING APPLIED
  🟢 Green cells  → [threshold/condition]
  🟡 Amber cells  → [threshold/condition]
  🔴 Red cells    → [threshold/condition]

[Markdown table preview of first 5 rows]

⚠️ DISCLAIMER: Exported reports are for internal analysis only.
— VKKM Aegis | vaibhavkkm.com
```

**When MCP offline (fallback):**
Present the data in a Markdown table and advise the user to copy it into Excel directly.

## Hard Rules

1. **Never export without a source command.** This command is a downstream exporter — always reference which prior VKKM Aegis command produced the data.
2. **Always include a Markdown table preview** even when the Excel file is generated (first 5 rows minimum).
3. **Include every field.** Do not truncate data in the export. If the risk register has 20 rows, export all 20.
4. **RAG colours must be applied in Excel.** Green, Amber, Red must be reflected as cell background colours — not just text labels.
5. **Always include the VKKM Aegis footer row** with generation timestamp.
6. **JSON export must follow the vkkm-aegis-v3 schema** — wrap data in `{"schema": "vkkm-aegis-v3", "report_type": "...", "generated_at": "...", "data": {...}}`.
7. **Always append DISCLAIMER.** Output must end with: `⚠️ DISCLAIMER: Exported data is for internal use and analysis purposes only. Validate all figures with your risk team before submitting to regulators or boards.`

## Example

**User prompt:** "Export the KRI dashboard from my last `/vkkm:kri-dashboard` run as Excel."

**Expected output:**

```
📊 AEGIS REPORT GENERATED — KRI Dashboard Export
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ EXCEL FILE GENERATED
  Format  : .xlsx (Excel 2016+)
  Report  : KRI Dashboard — Fintech Ltd
  Sheets  : 1 (KRI Dashboard)
  Rows    : 12 KRIs + 1 header
  Label   : ILLUSTRATIVE ESTIMATE

FORMAT APPLIED
  🟢 Green → Current value within green threshold
  🟡 Amber → Breaches green threshold, within amber boundary
  🔴 Red   → Breaches amber threshold — action required

PREVIEW (first 5 KRIs):
| KRI Name             | Category   | Current | Green | Amber | Red  | RAG   | Owner   |
|----------------------|------------|---------|-------|-------|------|-------|---------|
| Capital Adequacy (%) | Capital    | 14.2%   | >12%  | 8–12% | <8%  | 🟢    | CFO     |
| Liquidity (LCR)      | Liquidity  | 0.98    | >1.0  | 0.8–1 | <0.8 | 🟡    | Treasurer|
| Cyber Incidents/Month| Operational| 3       | 0–2   | 3–5   | >5   | 🟡    | CISO    |
| PD (mortgage book)   | Credit     | 4.8%    | <3%   | 3–7%  | >7%  | 🟡    | CRO     |
| Staff Turnover (%)   | HR         | 6.2%    | <8%   | 8–15% | >15% | 🟢    | HRD     |

⚠️ DISCLAIMER: Exported data is for internal use only. Validate with your risk team before submitting to regulators or boards.
— VKKM Aegis | vaibhavkkm.com
```
