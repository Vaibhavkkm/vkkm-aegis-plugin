#!/usr/bin/env node
/**
 * VKKM Aegis — Validation Suite
 * by Vaibhav Mangroliya (vaibhavkkm.com)
 *
 * Run this with: npm test
 *
 * Checks that every file is in place, every JSON parses correctly,
 * and every command/skill file has the sections it needs.
 * No npm packages required — just plain Node.js.
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// Resolve the project root from wherever this script lives
const ROOT = path.resolve(__dirname, '..');

// Every file that should exist in the project
const REQUIRED_FILES = [
  '.claude-plugin/plugin.json',
  '.claude-plugin/schema.json',
  '.mcp.json',
  'schemas/mcp-schema.json',
  'commands/scan-document.md',
  'commands/stress-test.md',
  'commands/risk-register.md',
  'commands/regulatory-check.md',
  'commands/escalation-report.md',
  'commands/counterparty-profile.md',
  'skills/risk-scoring.md',
  'skills/eu-regulations.md',
  'skills/contract-patterns.md',
  'skills/financial-risk.md',
  'skills/plain-language.md',
  'skills/disclaimers.md',
  'skills/risk-management/SKILL.md',
  'skills/vkkm-aegis/SKILL.md',
  'README.md',
  'CHANGELOG.md',
  'package.json',
  '.gitignore',
];

// The six slash commands that must be registered in plugin.json
const REQUIRED_SLASH_COMMANDS = [
  '/vkkm:scan-document',
  '/vkkm:stress-test',
  '/vkkm:risk-register',
  '/vkkm:regulatory-check',
  '/vkkm:escalation-report',
  '/vkkm:counterparty-profile',
];

// All five MCP data connectors that must be configured
const REQUIRED_CONNECTORS = ['factset', 'msci', 'google_drive', 'docusign', 'sharepoint'];

// Every command spec file needs these four sections — no exceptions
const COMMAND_REQUIRED_SECTIONS = [
  '## Behavior',
  '## Output Format',
  '## Hard Rules',
  '## Example',
];

// Per-skill content requirements — confirms the important stuff is actually there
const SKILL_REQUIRED_SECTIONS = {
  'skills/risk-scoring.md':      ['## Rule', '5×5 Risk Matrix', '📊 AEGIS RISK SNAPSHOT'],
  'skills/eu-regulations.md':    ['## Rule', 'GDPR', 'PSD2', 'DORA', 'NIS2'],
  'skills/contract-patterns.md': ['## Rule', '🔴 HIGH RISK', '🟢 LOW RISK'],
  'skills/financial-risk.md':    ['## Rule', 'Value at Risk', 'Monte Carlo', 'Stress Testing'],
  'skills/plain-language.md':    ['## Rule', 'VaR', 'GDPR', 'ISO 31000'],
  'skills/disclaimers.md':       ['Legal Disclaimer', 'Financial Disclaimer', 'Compliance Disclaimer', 'Due Diligence Disclaimer', 'Output Ordering'],
};

// Size floors — if a file is below these, something got accidentally truncated
const MIN_COMMAND_BYTES = 3000;
const MIN_SKILL_BYTES   = 1500;

// ─── Test state ───────────────────────────────
let passed   = 0;
let failed   = 0;
const failures = [];

// ─── Helpers ──────────────────────────────────

// Build an absolute path from a relative one
function p(file) {
  return path.join(ROOT, file);
}

// Read a file as UTF-8 text
function read(file) {
  return fs.readFileSync(p(file), 'utf8');
}

// Check if a file exists on disk
function exists(file) {
  return fs.existsSync(p(file));
}

// Get the byte size of a file
function fileSize(file) {
  return fs.statSync(p(file)).size;
}

// The core assertion — logs pass/fail and keeps a running count
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

// ─── Test groups ──────────────────────────────

// 1. Make sure every file in the spec actually exists on disk
function testFileStructure() {
  console.log('\n📁  FILE STRUCTURE');
  for (const file of REQUIRED_FILES) {
    assert(exists(file), `File exists: ${file}`);
  }
}

// 2. Parse every JSON file and catch syntax errors early
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
    // Make sure someone can actually run `npm test`
    assert(!!pkg.scripts && !!pkg.scripts.test, 'package.json has "test" script', 'add "test": "node tests/validate.js"');
  } catch (e) {
    assert(false, 'package.json is valid JSON', e.message);
  }

  return { pluginJson, mcpJson };
}

// 3. Check the plugin manifest has everything Claude needs to load it properly
function testPluginJson(pluginJson) {
  console.log('\n🔌  PLUGIN.JSON REQUIRED FIELDS');
  if (!pluginJson) { assert(false, 'plugin.json parsed — skipping field tests'); return; }

  assert(pluginJson.name === 'VKKM Aegis', 'name = "VKKM Aegis"');
  assert(typeof pluginJson.version === 'string' && pluginJson.version.length > 0, 'version is present');
  assert(typeof pluginJson.author === 'string' && pluginJson.author.length > 0, 'author is present');
  assert(typeof pluginJson.description === 'string' && pluginJson.description.length >= 20, 'description is ≥20 chars');
  assert(typeof pluginJson.system_prompt_path === 'string', 'system_prompt_path is present');
  assert(Array.isArray(pluginJson.slash_commands), 'slash_commands is an array');
  assert(
    Array.isArray(pluginJson.slash_commands) && pluginJson.slash_commands.length >= 6,
    'slash_commands has ≥6 entries',
    `found ${pluginJson.slash_commands?.length ?? 0}`
  );

  // Verify each command name is actually registered
  if (Array.isArray(pluginJson.slash_commands)) {
    for (const cmd of REQUIRED_SLASH_COMMANDS) {
      assert(pluginJson.slash_commands.includes(cmd), `slash_commands includes ${cmd}`);
    }
  }

  assert(typeof pluginJson.opening_message === 'string' && pluginJson.opening_message.length > 50, 'opening_message is present and non-trivial');

  // This field is required for Claude Code and direct API usage
  assert(
    typeof pluginJson.system_prompt === 'string' && pluginJson.system_prompt.length > 10,
    'system_prompt inline field present (required for Claude Code / API usage)'
  );
}

// 4. Confirm all five data connectors are configured with the minimum required fields
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

  // The labeling rules tell the plugin when to say "illustrative" vs "data-grounded"
  assert(
    mcpJson.data_labeling_rules &&
    typeof mcpJson.data_labeling_rules.no_connector_active === 'string' &&
    typeof mcpJson.data_labeling_rules.connector_active === 'string',
    'data_labeling_rules block present with both modes'
  );
}

// 5. Check every command file has the four required sections and mandatory content
function testCommandFiles() {
  console.log('\n📋  COMMAND SPEC FILES');

  const commandFiles = [
    'commands/scan-document.md',
    'commands/stress-test.md',
    'commands/risk-register.md',
    'commands/regulatory-check.md',
    'commands/escalation-report.md',
    'commands/counterparty-profile.md',
  ];

  for (const file of commandFiles) {
    if (!exists(file)) { assert(false, `${file} exists`); continue; }

    const content = read(file);
    const bytes   = fileSize(file);
    const name    = path.basename(file);

    // A command file under 3KB has probably been truncated
    assert(bytes >= MIN_COMMAND_BYTES, `${name} is ≥${MIN_COMMAND_BYTES}B`, `actual: ${bytes}B`);

    // These four sections are mandatory in every command spec
    for (const section of COMMAND_REQUIRED_SECTIONS) {
      assert(content.includes(section), `${name} contains "${section}"`);
    }

    // Every command output must include a disclaimer — check it's referenced
    assert(content.includes('DISCLAIMER'), `${name} references a DISCLAIMER`);

    // The AEGIS RISK SNAPSHOT must appear (usually in the example output)
    assert(content.includes('AEGIS RISK SNAPSHOT'), `${name} contains AEGIS RISK SNAPSHOT`);

    // Every output must be signed
    assert(content.includes('— VKKM Aegis'), `${name} contains "— VKKM Aegis" sign-off`);
  }
}

// 6. Check each always-active skill file has its key content
function testSkillFiles() {
  console.log('\n🧠  ALWAYS-ACTIVE SKILL FILES');

  for (const [file, sections] of Object.entries(SKILL_REQUIRED_SECTIONS)) {
    if (!exists(file)) { assert(false, `${file} exists`); continue; }

    const content = read(file);
    const bytes   = fileSize(file);
    const name    = path.basename(file);

    assert(bytes >= MIN_SKILL_BYTES, `${name} is ≥${MIN_SKILL_BYTES}B`, `actual: ${bytes}B`);

    for (const term of sections) {
      assert(content.includes(term), `${name} contains "${term}"`);
    }
  }
}

// 7. Validate the master SKILL.md prompt and confirm both canonical copies are identical
function testMasterPrompt() {
  console.log('\n📜  MASTER PROMPT (SKILL.md)');

  const skillFile = 'skills/risk-management/SKILL.md';
  const aegisFile = 'skills/vkkm-aegis/SKILL.md';

  if (!exists(skillFile)) { assert(false, `${skillFile} exists`); return; }
  const content = read(skillFile);

  // Every slash command must be referenced in the master prompt
  for (const cmd of REQUIRED_SLASH_COMMANDS) {
    assert(content.includes(cmd), `SKILL.md references ${cmd}`);
  }

  assert(content.includes('AEGIS RISK SNAPSHOT'), 'SKILL.md defines AEGIS RISK SNAPSHOT block');
  assert(content.includes('5×5'), 'SKILL.md references 5×5 risk matrix');
  assert(content.includes('VKKM Aegis'), 'SKILL.md references brand name');

  // The two copies must be byte-for-byte identical
  if (exists(aegisFile)) {
    const a = read(skillFile).trim();
    const b = read(aegisFile).trim();
    assert(a === b, 'skills/risk-management/SKILL.md and skills/vkkm-aegis/SKILL.md are identical');
  } else {
    assert(false, 'Canonical skills/vkkm-aegis/SKILL.md exists');
  }
}

// 8. Make sure every disclaimer type is in the disclaimers file
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

// 9. Verify the 5x5 risk matrix thresholds are internally consistent
function testRiskScoringConsistency() {
  console.log('\n📊  RISK SCORING CONSISTENCY');

  if (!exists('skills/risk-scoring.md')) { assert(false, 'risk-scoring.md exists'); return; }
  const content = read('skills/risk-scoring.md');

  // Score thresholds must be unambiguous
  assert(content.includes('20–25'), 'Critical threshold = 20–25');
  assert(content.includes('10–19'), 'High threshold = 10–19');
  assert(content.includes('5–9'),   'Medium threshold = 5–9');
  assert(content.includes('1–4'),   'Low threshold = 1–4');

  // Each risk level must have its colour-coded emoji
  assert(content.includes('🔴'), 'Critical uses 🔴');
  assert(content.includes('🟠'), 'High uses 🟠');
  assert(content.includes('🟡'), 'Medium uses 🟡');
  assert(content.includes('🟢'), 'Low uses 🟢');

  assert(content.includes('5×5'), 'References 5×5 matrix');
  assert(content.includes('Score =') || content.includes('Score=') || content.includes('Likelihood') && content.includes('Impact'),
    'Defines scoring formula');
}

// 10. Spot-check important content unique to specific commands
function testCommandSpecificContent() {
  console.log('\n🔎  COMMAND-SPECIFIC CONTENT CHECKS');

  if (exists('commands/counterparty-profile.md')) {
    const c = read('commands/counterparty-profile.md');
    assert(c.includes('Trust Score'), 'counterparty-profile.md has Trust Score');
    assert(c.includes('Go / Caution / No-Go') || c.includes('GO') && c.includes('CAUTION') && c.includes('NO-GO'),
      'counterparty-profile.md has Go/Caution/No-Go recommendation');
  }

  if (exists('commands/escalation-report.md')) {
    const c = read('commands/escalation-report.md');
    assert(c.includes('ESCALATION PATH'), 'escalation-report.md has ESCALATION PATH section');
    assert(c.includes('Tone') || c.includes('tone'), 'escalation-report.md has tone menu');
  }

  if (exists('commands/regulatory-check.md')) {
    const c = read('commands/regulatory-check.md');
    assert(c.includes('OFFICIAL SOURCES') || c.includes('Official Sources'), 'regulatory-check.md has official sources');
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
    assert(c.includes('DATA-GROUNDED'),          'stress-test.md has DATA-GROUNDED label');
  }
}

// 11. Check EU regulations coverage is accurate and complete
function testEuRegulations() {
  console.log('\n🏛️   EU REGULATIONS ACCURACY');

  if (!exists('skills/eu-regulations.md')) { assert(false, 'eu-regulations.md exists'); return; }
  const c = read('skills/eu-regulations.md');

  // DORA went live January 2025 — make sure the date is there
  assert(c.includes('Jan 2025') || c.includes('January 2025') || c.includes('2025'),
    'eu-regulations.md mentions DORA effective date (2025)');

  assert(c.includes('NIS2'), 'eu-regulations.md covers NIS2');

  const regs = ['GDPR', 'PSD2', 'MiFID II', 'DORA', 'AML', 'EMIR', 'ePrivacy', 'CSRD'];
  for (const reg of regs) {
    assert(c.includes(reg), `eu-regulations.md covers ${reg}`);
  }
}

// ─── Run everything ────────────────────────────────────────────────────────────

console.log('');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  🛡️  VKKM Aegis — Validation Suite');
console.log('  by Vaibhav Mangroliya (vaibhavkkm.com)');
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

// ─── Summary ───────────────────────────────────────────────────────────────────

const total = passed + failed;
console.log('');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
if (failed === 0) {
  console.log(`  ✅  VKKM Aegis Validation — ALL CHECKS PASSED (${passed}/${total})`);
} else {
  console.log(`  ❌  VKKM Aegis Validation — FAILED (${failed} failure${failed !== 1 ? 's' : ''}, ${passed} passed)`);
  console.log('');
  console.log('  Failures:');
  for (const f of failures) {
    console.log(`  • ${f.testName}${f.detail ? ` — ${f.detail}` : ''}`);
  }
}
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');

process.exit(failed === 0 ? 0 : 1);
