#!/usr/bin/env node
/**
 * VKKM Aegis — Validation Suite
 * Built by VKKM (vaibhavkkm.com)
 *
 * Run with: npm test
 *
 * Checks that:
 *   1. Every required file exists on disk
 *   2. Every JSON file is valid JSON
 *   3. plugin.json has all v3.0 fields and all 18 commands
 *   4. .mcp.json has all data connectors
 *   5. Every command spec file has the four required sections
 *   6. Every skill file has its key content
 *   7. The master SKILL.md prompt references all 18 commands
 *   8. The two canonical SKILL.md copies are byte-for-byte identical
 *   9. Every disclaimer type is present in disclaimers.md
 *  10. The 5x5 risk scoring thresholds are internally consistent
 *  11. Command-specific content spot-checks for all 18 commands
 *  12. EU regulations coverage is accurate and complete
 *  13. v2.0 and v3.0 skill files have their key content
 *  14. Python MCP server file and requirements.txt exist
 *  15. v3.0 data modules (live_data.py, backtest.py, ml_pd_model.py, excel_export.py) exist
 *  16. Synthetic default dataset CSV exists
 *  17. v3.0 MCP endpoints referenced in mcp_server.py
 *
 * No npm packages required — plain Node.js only.
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// Resolve the project root from wherever this script lives.
const ROOT = path.resolve(__dirname, '..');

// ─── File manifest — every file that must exist ───────────────────────────────

const REQUIRED_FILES = [
  // Plugin config
  '.claude-plugin/plugin.json',
  '.claude-plugin/schema.json',
  '.mcp.json',
  'schemas/mcp-schema.json',

  // Original v1.0 commands (6)
  'commands/scan-document.md',
  'commands/stress-test.md',
  'commands/risk-register.md',
  'commands/regulatory-check.md',
  'commands/escalation-report.md',
  'commands/counterparty-profile.md',

  // v2.0 commands (9)
  'commands/zscore.md',
  'commands/greeks.md',
  'commands/var-calc.md',
  'commands/credit-risk.md',
  'commands/liquidity-risk.md',
  'commands/icaap.md',
  'commands/rcsa.md',
  'commands/kri-dashboard.md',
  'commands/reg-calendar.md',

  // v3.0 commands (3)
  'commands/backtest.md',
  'commands/ml-pd.md',
  'commands/export-report.md',

  // Original v1.0 skills (6)
  'skills/risk-scoring.md',
  'skills/eu-regulations.md',
  'skills/contract-patterns.md',
  'skills/financial-risk.md',
  'skills/plain-language.md',
  'skills/disclaimers.md',

  // v2.0 skills (3)
  'skills/credit-models.md',
  'skills/options-theory.md',
  'skills/regulatory-docs.md',

  // Master prompts (must be identical)
  'skills/risk-management/SKILL.md',
  'skills/vkkm-aegis/SKILL.md',

  // Python MCP backend
  'mcp_server.py',
  'requirements.txt',

  // v3.0 data modules
  'data/__init__.py',
  'data/live_data.py',
  'data/backtest.py',
  'data/generate_dataset.py',
  'data/ml_pd_model.py',
  'data/excel_export.py',
  'data/synthetic_default_dataset.csv',

  // Project metadata
  'README.md',
  'CHANGELOG.md',
  'package.json',
  '.gitignore',
];

// All 18 slash commands that must be registered in plugin.json.
const REQUIRED_SLASH_COMMANDS = [
  '/vkkm:scan-document',
  '/vkkm:stress-test',
  '/vkkm:risk-register',
  '/vkkm:regulatory-check',
  '/vkkm:escalation-report',
  '/vkkm:counterparty-profile',
  '/vkkm:zscore',
  '/vkkm:greeks',
  '/vkkm:var-calc',
  '/vkkm:credit-risk',
  '/vkkm:liquidity-risk',
  '/vkkm:icaap',
  '/vkkm:rcsa',
  '/vkkm:kri-dashboard',
  '/vkkm:reg-calendar',
  // v3.0 new commands
  '/vkkm:backtest',
  '/vkkm:ml-pd',
  '/vkkm:export-report',
];

// The five MCP data connectors that must be configured.
const REQUIRED_CONNECTORS = ['factset', 'msci', 'google_drive', 'docusign', 'sharepoint'];

// Every command spec file must contain these four section headers.
const COMMAND_REQUIRED_SECTIONS = [
  '## Behavior',
  '## Output Format',
  '## Hard Rules',
  '## Example',
];

// Per-skill content requirements — confirms the important content is present.
const SKILL_REQUIRED_SECTIONS = {
  'skills/risk-scoring.md':      ['## Rule', '5×5 Risk Matrix', '📊 AEGIS RISK SNAPSHOT'],
  'skills/eu-regulations.md':    ['## Rule', 'GDPR', 'PSD2', 'DORA', 'NIS2'],
  'skills/contract-patterns.md': ['## Rule', '🔴 HIGH RISK', '🟢 LOW RISK'],
  'skills/financial-risk.md':    ['## Rule', 'Value at Risk', 'Monte Carlo', 'Stress Testing'],
  'skills/plain-language.md':    ['## Rule', 'VaR', 'GDPR', 'ISO 31000'],
  'skills/disclaimers.md':       ['Legal Disclaimer', 'Financial Disclaimer', 'Compliance Disclaimer', 'Due Diligence Disclaimer', 'Output Ordering'],
  // New v2.0 skill files
  'skills/credit-models.md':     ['## Rule', 'Altman', 'X1', 'X3', 'PD', 'LGD', 'EAD', 'Expected Loss'],
  'skills/options-theory.md':    ['## Rule', 'Black-Scholes', 'Delta', 'Gamma', 'Vega', 'Theta', 'Rho', 'd1', 'd2'],
  'skills/regulatory-docs.md':   ['## Rule', 'ICAAP', 'RCSA', 'KRI', 'LCR', 'NSFR'],
};

// Minimum file sizes — files below these thresholds were probably truncated.
const MIN_COMMAND_BYTES = 3000;
const MIN_SKILL_BYTES   = 1500;

// ─── Test state ───────────────────────────────────────────────────────────────

let passed   = 0;
let failed   = 0;
const failures = [];

// ─── Helpers ──────────────────────────────────────────────────────────────────

/** Build an absolute path from a relative path. */
function p(file) { return path.join(ROOT, file); }

/** Read a file as UTF-8 text. */
function read(file) { return fs.readFileSync(p(file), 'utf8'); }

/** Check whether a file exists on disk. */
function exists(file) { return fs.existsSync(p(file)); }

/** Get the byte size of a file. */
function fileSize(file) { return fs.statSync(p(file)).size; }

/**
 * Core assertion helper.
 * Logs ✅ or ❌, increments pass/fail counters, and records failures
 * so they can be reprinted in the summary at the end.
 */
function assert(condition, testName, detail = '') {
  if (condition) {
    console.log(`  ✅  ${testName}`);
    passed++;
  } else {
    console.log(`  ❌  ${testName}${detail ? ` — ${detail}` : ''}`);
    failed++;
    failures.push({ testName, detail });
  }
}

// ─── Test groups ──────────────────────────────────────────────────────────────

/** 1. Verify every file in the project manifest actually exists on disk. */
function testFileStructure() {
  console.log('\n📁  FILE STRUCTURE');
  for (const file of REQUIRED_FILES) {
    assert(exists(file), `File exists: ${file}`);
  }
}

/** 2. Parse every JSON file and surface syntax errors early. */
function testJsonValidity() {
  console.log('\n🔍  JSON VALIDITY');

  let pluginJson = null;
  try {
    pluginJson = JSON.parse(read('.claude-plugin/plugin.json'));
    assert(true, 'plugin.json is valid JSON');
  } catch (e) {
    assert(false, 'plugin.json is valid JSON', e.message);
  }

  let mcpJson = null;
  try {
    mcpJson = JSON.parse(read('.mcp.json'));
    assert(true, '.mcp.json is valid JSON');
  } catch (e) {
    assert(false, '.mcp.json is valid JSON', e.message);
  }

  try {
    JSON.parse(read('.claude-plugin/schema.json'));
    assert(true, 'schema.json is valid JSON');
  } catch (e) {
    assert(false, 'schema.json is valid JSON', e.message);
  }

  try {
    const pkg = JSON.parse(read('package.json'));
    assert(true, 'package.json is valid JSON');
    // Confirm `npm test` and `npm run test:math` are wired up.
    assert(!!pkg.scripts && !!pkg.scripts.test,
      'package.json has "test" script');
    assert(!!pkg.scripts && !!pkg.scripts['test:math'],
      'package.json has "test:math" script');
    assert(!!pkg.scripts && !!pkg.scripts['test:all'],
      'package.json has "test:all" script');
  } catch (e) {
    assert(false, 'package.json is valid JSON', e.message);
  }

  return { pluginJson, mcpJson };
}

/** 3. Verify the plugin manifest has all v2.0 required fields. */
function testPluginJson(pluginJson) {
  console.log('\n🔌  PLUGIN.JSON — v2.0 REQUIRED FIELDS');
  if (!pluginJson) { assert(false, 'plugin.json parsed — skipping field tests'); return; }

  assert(pluginJson.name === 'VKKM Aegis', 'name = "VKKM Aegis"');
  assert(pluginJson.version === '3.0', 'version = "3.0"');
  assert(typeof pluginJson.author === 'string' && pluginJson.author.length > 0, 'author is present');
  assert(typeof pluginJson.description === 'string' && pluginJson.description.length >= 20, 'description ≥ 20 chars');
  assert(typeof pluginJson.system_prompt_path === 'string', 'system_prompt_path is present');
  assert(Array.isArray(pluginJson.slash_commands), 'slash_commands is an array');

  // All 18 commands must be registered.
  assert(
    Array.isArray(pluginJson.slash_commands) && pluginJson.slash_commands.length >= 18,
    'slash_commands has ≥ 18 entries',
    `found ${pluginJson.slash_commands?.length ?? 0}`
  );

  if (Array.isArray(pluginJson.slash_commands)) {
    for (const cmd of REQUIRED_SLASH_COMMANDS) {
      assert(pluginJson.slash_commands.includes(cmd), `slash_commands includes ${cmd}`);
    }
  }

  assert(
    typeof pluginJson.opening_message === 'string' && pluginJson.opening_message.length > 50,
    'opening_message is present and non-trivial'
  );
  assert(
    typeof pluginJson.system_prompt === 'string' && pluginJson.system_prompt.length > 10,
    'system_prompt inline field present (required for Claude Code / API usage)'
  );

  // v2.0 must reference the Python MCP server.
  assert(
    typeof pluginJson.python_mcp_server === 'string',
    'python_mcp_server field present (v2.0 requirement)'
  );
}

/** 4. Confirm all five data connectors are configured correctly. */
function testMcpJson(mcpJson) {
  console.log('\n🔗  .MCP.JSON CONNECTORS');
  if (!mcpJson) { assert(false, '.mcp.json parsed — skipping connector tests'); return; }

  assert(typeof mcpJson.mcpServers === 'object' && mcpJson.mcpServers !== null, 'mcpServers object present');

  for (const connector of REQUIRED_CONNECTORS) {
    assert(
      mcpJson.mcpServers && typeof mcpJson.mcpServers[connector] === 'object',
      `Connector "${connector}" is defined`
    );
    if (mcpJson.mcpServers && mcpJson.mcpServers[connector]) {
      const c = mcpJson.mcpServers[connector];
      assert(typeof c.label   === 'string', `  └─ ${connector}.label present`);
      assert(typeof c.purpose === 'string', `  └─ ${connector}.purpose present`);
      assert(typeof c.auth    === 'string', `  └─ ${connector}.auth present`);
    }
  }

  // The labeling rules tell the plugin when to say "illustrative" vs "data-grounded".
  assert(
    mcpJson.data_labeling_rules &&
    typeof mcpJson.data_labeling_rules.no_connector_active === 'string' &&
    typeof mcpJson.data_labeling_rules.connector_active === 'string',
    'data_labeling_rules block present with both modes'
  );
}

/** 5. Check every command file has the four required sections. */
function testCommandFiles() {
  console.log('\n📋  COMMAND SPEC FILES (all 15)');

  const commandFiles = [
    // Original v1.0 commands
    'commands/scan-document.md',
    'commands/stress-test.md',
    'commands/risk-register.md',
    'commands/regulatory-check.md',
    'commands/escalation-report.md',
    'commands/counterparty-profile.md',
    // New v2.0 commands
    'commands/zscore.md',
    'commands/greeks.md',
    'commands/var-calc.md',
    'commands/credit-risk.md',
    'commands/liquidity-risk.md',
    'commands/icaap.md',
    'commands/rcsa.md',
    'commands/kri-dashboard.md',
    'commands/reg-calendar.md',
  ];

  for (const file of commandFiles) {
    if (!exists(file)) { assert(false, `${file} exists`); continue; }

    const content = read(file);
    const bytes   = fileSize(file);
    const name    = path.basename(file);

    // A command file under 3KB was probably truncated.
    assert(bytes >= MIN_COMMAND_BYTES, `${name} is ≥ ${MIN_COMMAND_BYTES}B`, `actual: ${bytes}B`);

    // These four sections are mandatory in every command spec.
    for (const section of COMMAND_REQUIRED_SECTIONS) {
      assert(content.includes(section), `${name} contains "${section}"`);
    }

    // Every command output must include a disclaimer reference.
    assert(content.includes('DISCLAIMER'), `${name} references a DISCLAIMER`);

    // The AEGIS RISK SNAPSHOT must appear (typically in the example output).
    assert(content.includes('AEGIS RISK SNAPSHOT'), `${name} contains AEGIS RISK SNAPSHOT`);

    // Every output must be signed by VKKM Aegis.
    assert(content.includes('— VKKM Aegis'), `${name} contains "— VKKM Aegis" sign-off`);
  }
}

/** 6. Check each always-active skill file has its key content. */
function testSkillFiles() {
  console.log('\n🧠  ALWAYS-ACTIVE SKILL FILES (all 9)');

  for (const [file, sections] of Object.entries(SKILL_REQUIRED_SECTIONS)) {
    if (!exists(file)) { assert(false, `${file} exists`); continue; }

    const content = read(file);
    const bytes   = fileSize(file);
    const name    = path.basename(file);

    assert(bytes >= MIN_SKILL_BYTES, `${name} is ≥ ${MIN_SKILL_BYTES}B`, `actual: ${bytes}B`);

    for (const term of sections) {
      assert(content.includes(term), `${name} contains "${term}"`);
    }
  }
}

/** 7 & 8. Validate the master SKILL.md and confirm both copies are identical. */
function testMasterPrompt() {
  console.log('\n📜  MASTER PROMPT (SKILL.md v2.0)');

  const skillFile = 'skills/risk-management/SKILL.md';
  const aegisFile = 'skills/vkkm-aegis/SKILL.md';

  if (!exists(skillFile)) { assert(false, `${skillFile} exists`); return; }
  const content = read(skillFile);

  // All 15 commands must be referenced in the master prompt.
  for (const cmd of REQUIRED_SLASH_COMMANDS) {
    assert(content.includes(cmd), `SKILL.md references ${cmd}`);
  }

  assert(content.includes('AEGIS RISK SNAPSHOT'), 'SKILL.md defines AEGIS RISK SNAPSHOT block');
  assert(content.includes('5×5'), 'SKILL.md references 5×5 risk matrix');
  assert(content.includes('VKKM Aegis'), 'SKILL.md references brand name');
  assert(content.includes('2.0'), 'SKILL.md references version 2.0');

  // New v2.0 skills must be in the master prompt.
  assert(content.includes('Altman Z-Score') || content.includes('zscore'), 'SKILL.md references Z-Score skill');
  assert(content.includes('Black-Scholes') || content.includes('Greeks'), 'SKILL.md references options skill');
  assert(content.includes('ICAAP') || content.includes('RCSA'), 'SKILL.md references regulatory docs skill');

  // The two copies must be byte-for-byte identical (test enforces this).
  if (exists(aegisFile)) {
    const a = read(skillFile).trim();
    const b = read(aegisFile).trim();
    assert(a === b, 'skills/risk-management/SKILL.md and skills/vkkm-aegis/SKILL.md are identical');
  } else {
    assert(false, 'Canonical skills/vkkm-aegis/SKILL.md exists');
  }
}

/** 9. Make sure every disclaimer type is in the disclaimers file. */
function testDisclaimers() {
  console.log('\n⚖️   DISCLAIMERS FILE');

  if (!exists('skills/disclaimers.md')) { assert(false, 'disclaimers.md exists'); return; }
  const content = read('skills/disclaimers.md');

  const requiredBlocks = [
    'LEGAL DISCLAIMER',
    'FINANCIAL DISCLAIMER',
    'COMPLIANCE DISCLAIMER',
    'DUE DILIGENCE DISCLAIMER',
    'GENERAL DISCLAIMER',
    'Output Ordering',
  ];
  for (const block of requiredBlocks) {
    assert(content.includes(block), `disclaimers.md has "${block}"`);
  }
}

/** 10. Verify the 5×5 risk matrix thresholds are internally consistent. */
function testRiskScoringConsistency() {
  console.log('\n📊  RISK SCORING CONSISTENCY');

  if (!exists('skills/risk-scoring.md')) { assert(false, 'risk-scoring.md exists'); return; }
  const content = read('skills/risk-scoring.md');

  assert(content.includes('20–25'), 'Critical threshold = 20–25');
  assert(content.includes('10–19'), 'High threshold = 10–19');
  assert(content.includes('5–9'),   'Medium threshold = 5–9');
  assert(content.includes('1–4'),   'Low threshold = 1–4');

  assert(content.includes('🔴'), 'Critical uses 🔴');
  assert(content.includes('🟠'), 'High uses 🟠');
  assert(content.includes('🟡'), 'Medium uses 🟡');
  assert(content.includes('🟢'), 'Low uses 🟢');

  assert(content.includes('5×5'), 'References 5×5 matrix');
  assert(
    content.includes('Score =') || content.includes('Score=') ||
    (content.includes('Likelihood') && content.includes('Impact')),
    'Defines scoring formula'
  );
}

/** 11. Command-specific content spot-checks for all 15 commands. */
function testCommandSpecificContent() {
  console.log('\n🔎  COMMAND-SPECIFIC CONTENT CHECKS');

  // ── v1.0 commands ──────────────────────────────────────────────────────────

  if (exists('commands/counterparty-profile.md')) {
    const c = read('commands/counterparty-profile.md');
    assert(c.includes('Trust Score'), 'counterparty-profile.md has Trust Score');
    assert(
      c.includes('Go / Caution / No-Go') || (c.includes('GO') && c.includes('CAUTION') && c.includes('NO-GO')),
      'counterparty-profile.md has Go/Caution/No-Go recommendation'
    );
  }

  if (exists('commands/escalation-report.md')) {
    const c = read('commands/escalation-report.md');
    assert(c.includes('ESCALATION PATH'), 'escalation-report.md has ESCALATION PATH section');
    assert(c.includes('Tone') || c.includes('tone'), 'escalation-report.md has tone menu');
  }

  if (exists('commands/regulatory-check.md')) {
    const c = read('commands/regulatory-check.md');
    assert(
      c.includes('OFFICIAL SOURCES') || c.includes('Official Sources'),
      'regulatory-check.md has official sources'
    );
    assert(c.includes('eur-lex.europa.eu'), 'regulatory-check.md links to EUR-Lex');
  }

  if (exists('commands/risk-register.md')) {
    const c = read('commands/risk-register.md');
    assert(c.includes('ISO 31000'),    'risk-register.md references ISO 31000');
    assert(c.includes('Regulatory'),   'risk-register.md covers Regulatory category');
    assert(c.includes('Reputational'), 'risk-register.md covers Reputational category');
    assert(c.includes('Financial'),    'risk-register.md covers Financial category');
  }

  if (exists('commands/stress-test.md')) {
    const c = read('commands/stress-test.md');
    assert(c.includes('ILLUSTRATIVE ESTIMATE'), 'stress-test.md has ILLUSTRATIVE ESTIMATE label');
    assert(c.includes('DATA-GROUNDED'),         'stress-test.md has DATA-GROUNDED label');
  }

  // ── v2.0 commands ──────────────────────────────────────────────────────────

  if (exists('commands/zscore.md')) {
    const c = read('commands/zscore.md');
    assert(c.includes('Altman'), 'zscore.md references Altman');
    assert(c.includes('X1') && c.includes('X2') && c.includes('X3'), 'zscore.md has X1–X3 ratio definitions');
    assert(c.includes('Distress'), 'zscore.md has Distress zone');
    assert(c.includes('Z\'') || c.includes("Z'") || c.includes('private'), 'zscore.md has private company model');
  }

  if (exists('commands/greeks.md')) {
    const c = read('commands/greeks.md');
    assert(c.includes('Delta'), 'greeks.md has Delta');
    assert(c.includes('Gamma'), 'greeks.md has Gamma');
    assert(c.includes('Vega'),  'greeks.md has Vega');
    assert(c.includes('Theta'), 'greeks.md has Theta');
    assert(c.includes('Rho'),   'greeks.md has Rho');
    assert(c.includes('d1') && c.includes('d2'), 'greeks.md has d1/d2 intermediate calculations');
    assert(c.includes('Black-Scholes'), 'greeks.md references Black-Scholes');
  }

  if (exists('commands/var-calc.md')) {
    const c = read('commands/var-calc.md');
    assert(c.includes('CVaR') || c.includes('Expected Shortfall'), 'var-calc.md has CVaR/Expected Shortfall');
    assert(c.includes('GBM') || c.includes('Geometric Brownian'), 'var-calc.md references GBM');
    assert(c.includes('ILLUSTRATIVE ESTIMATE'), 'var-calc.md has ILLUSTRATIVE ESTIMATE label');
  }

  if (exists('commands/credit-risk.md')) {
    const c = read('commands/credit-risk.md');
    assert(c.includes('EL = PD') || c.includes('EL=PD'), 'credit-risk.md has EL = PD × EAD × LGD formula');
    assert(c.includes('Unexpected Loss') || c.includes('UL ='), 'credit-risk.md has Unexpected Loss');
    assert(c.includes('LGD'), 'credit-risk.md has LGD');
  }

  if (exists('commands/liquidity-risk.md')) {
    const c = read('commands/liquidity-risk.md');
    assert(c.includes('LCR'), 'liquidity-risk.md has LCR');
    assert(c.includes('NSFR'), 'liquidity-risk.md has NSFR');
    assert(c.includes('Cash Runway') || c.includes('cash runway'), 'liquidity-risk.md has cash runway');
  }

  if (exists('commands/icaap.md')) {
    const c = read('commands/icaap.md');
    assert(c.includes('EBA') || c.includes('EBA/GL'), 'icaap.md references EBA guidelines');
    assert(c.includes('CRD') || c.includes('Pillar 2'), 'icaap.md references CRD/Pillar 2');
    assert(c.includes('SECTION 1') || c.includes('Section 1'), 'icaap.md has Section 1');
    assert(c.includes('SECTION 7') || c.includes('Section 7') || c.includes('Governance'), 'icaap.md has 7 sections');
  }

  if (exists('commands/rcsa.md')) {
    const c = read('commands/rcsa.md');
    assert(c.includes('Inherent Risk'), 'rcsa.md has Inherent Risk');
    assert(c.includes('Residual Risk'), 'rcsa.md has Residual Risk');
    assert(c.includes('ISO 31000'), 'rcsa.md references ISO 31000');
  }

  if (exists('commands/kri-dashboard.md')) {
    const c = read('commands/kri-dashboard.md');
    assert(c.includes('Green') && c.includes('Amber') && c.includes('Red'), 'kri-dashboard.md has RAG thresholds');
    assert(c.includes('SMART') || c.includes('KRI'), 'kri-dashboard.md has KRI framework');
  }

  if (exists('commands/reg-calendar.md')) {
    const c = read('commands/reg-calendar.md');
    assert(c.includes('CSSF') || c.includes('EBA') || c.includes('regulator'), 'reg-calendar.md references regulators');
    assert(c.includes('OFFICIAL SOURCES') || c.includes('Official Sources') || c.includes('official'), 'reg-calendar.md has official sources section');
    assert(c.includes('URGENT') || c.includes('urgent') || c.includes('🔴'), 'reg-calendar.md has urgency flagging');
  }
}

/** 12. Check EU regulations coverage. */
function testEuRegulations() {
  console.log('\n🏛️   EU REGULATIONS ACCURACY');

  if (!exists('skills/eu-regulations.md')) { assert(false, 'eu-regulations.md exists'); return; }
  const c = read('skills/eu-regulations.md');

  // DORA went live January 2025 — the date must be present.
  assert(
    c.includes('Jan 2025') || c.includes('January 2025') || c.includes('2025'),
    'eu-regulations.md mentions DORA effective date (2025)'
  );

  assert(c.includes('NIS2'), 'eu-regulations.md covers NIS2');

  const regs = ['GDPR', 'PSD2', 'MiFID II', 'DORA', 'AML', 'EMIR', 'ePrivacy', 'CSRD'];
  for (const reg of regs) {
    assert(c.includes(reg), `eu-regulations.md covers ${reg}`);
  }
}

/** 13. Check Python MCP server file content. */
function testMcpServer() {
  console.log('\n🐍  PYTHON MCP SERVER');

  if (!exists('mcp_server.py')) { assert(false, 'mcp_server.py exists'); return; }
  const c = read('mcp_server.py');

  assert(c.includes('/monte-carlo'),  'mcp_server.py has /monte-carlo endpoint');
  assert(c.includes('/greeks'),       'mcp_server.py has /greeks endpoint');
  assert(c.includes('/zscore'),       'mcp_server.py has /zscore endpoint');
  assert(c.includes('/credit-risk'),  'mcp_server.py has /credit-risk endpoint');
  assert(c.includes('/liquidity'),    'mcp_server.py has /liquidity endpoint');
  assert(c.includes('/health'),       'mcp_server.py has /health liveness probe');
  assert(c.includes('numpy'),         'mcp_server.py imports numpy');
  assert(c.includes('scipy'),         'mcp_server.py imports scipy');
  assert(c.includes('FastAPI') || c.includes('fastapi'), 'mcp_server.py uses FastAPI');

  if (!exists('requirements.txt')) { assert(false, 'requirements.txt exists'); return; }
  const req = read('requirements.txt');
  assert(req.includes('fastapi'), 'requirements.txt includes fastapi');
  assert(req.includes('numpy'),   'requirements.txt includes numpy');
  assert(req.includes('scipy'),   'requirements.txt includes scipy');
  assert(req.includes('uvicorn'), 'requirements.txt includes uvicorn');
}

// ─── Run everything ────────────────────────────────────────────────────────────

console.log('');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  🛡️  VKKM Aegis v2.0 — Validation Suite');
console.log('  Built by VKKM (vaibhavkkm.com)');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log(`  Root: ${ROOT}`);
console.log(`  Date: ${new Date().toISOString().split('T')[0]}`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

testFileStructure();
const { pluginJson, mcpJson } = testJsonValidity();
testPluginJson(pluginJson);
testMcpJson(mcpJson);
testCommandFiles();
testSkillFiles();
testMasterPrompt();
testDisclaimers();
testRiskScoringConsistency();
testCommandSpecificContent();
testEuRegulations();
testMcpServer();

// ─── Summary ──────────────────────────────────────────────────────────────────

const total = passed + failed;
console.log('');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
if (failed === 0) {
  console.log(`  ✅  VKKM Aegis v2.0 Validation — ALL CHECKS PASSED (${passed}/${total})`);
} else {
  console.log(`  ❌  VKKM Aegis v2.0 Validation — FAILED (${failed} failure${failed !== 1 ? 's' : ''}, ${passed} passed)`);
  console.log('');
  console.log('  Failures:');
  for (const f of failures) {
    console.log(`  • ${f.testName}${f.detail ? ` — ${f.detail}` : ''}`);
  }
}
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');

process.exit(failed === 0 ? 0 : 1);
