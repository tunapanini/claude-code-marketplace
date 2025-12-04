#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const SCHEMA_PATH = path.join(__dirname, '..', 'schemas', 'plugin.schema.json');

function validate(filePath) {
  const ajv = new Ajv({ allErrors: true, strict: false });
  addFormats(ajv);

  const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf-8'));
  const validate = ajv.compile(schema);

  const content = fs.readFileSync(filePath, 'utf-8');
  const plugin = JSON.parse(content);

  const valid = validate(plugin);

  if (valid) {
    console.log(`✓ ${filePath} is valid`);
    return true;
  } else {
    console.error(`✗ ${filePath} has errors:`);
    for (const error of validate.errors) {
      console.error(`  - ${error.instancePath || '/'}: ${error.message}`);
    }
    return false;
  }
}

function validateAll() {
  const pluginsDir = path.join(__dirname, '..', 'plugins');
  const types = ['mcp-servers', 'commands', 'hooks', 'agents'];
  let hasErrors = false;

  for (const type of types) {
    const typeDir = path.join(pluginsDir, type);
    if (!fs.existsSync(typeDir)) continue;

    const files = fs.readdirSync(typeDir).filter(f => f.endsWith('.json'));

    for (const file of files) {
      const filePath = path.join(typeDir, file);
      if (!validate(filePath)) {
        hasErrors = true;
      }
    }
  }

  process.exit(hasErrors ? 1 : 0);
}

// Main
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log('Validating all plugins...\n');
  validateAll();
} else {
  let hasErrors = false;
  for (const arg of args) {
    if (!validate(arg)) {
      hasErrors = true;
    }
  }
  process.exit(hasErrors ? 1 : 0);
}
