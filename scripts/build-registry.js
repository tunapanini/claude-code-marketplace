#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const PLUGINS_DIR = path.join(__dirname, '..', 'plugins');
const OUTPUT_FILE = path.join(__dirname, '..', 'registry.json');

function readPlugins(dir) {
  const plugins = [];
  const types = ['mcp-servers', 'commands', 'hooks', 'agents'];

  for (const type of types) {
    const typeDir = path.join(dir, type);
    if (!fs.existsSync(typeDir)) continue;

    const files = fs.readdirSync(typeDir).filter(f => f.endsWith('.json'));

    for (const file of files) {
      const filePath = path.join(typeDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const plugin = JSON.parse(content);

      plugins.push({
        ...plugin,
        _source: `plugins/${type}/${file}`
      });
    }
  }

  return plugins;
}

function buildRegistry() {
  const plugins = readPlugins(PLUGINS_DIR);

  const registry = {
    $schema: './schemas/registry.schema.json',
    version: '1.0.0',
    updated: new Date().toISOString(),
    count: plugins.length,
    plugins: plugins.sort((a, b) => a.name.localeCompare(b.name))
  };

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(registry, null, 2));

  console.log(`✓ Built registry with ${plugins.length} plugins`);
  console.log(`  - MCP Servers: ${plugins.filter(p => p.type === 'mcp-server').length}`);
  console.log(`  - Commands: ${plugins.filter(p => p.type === 'command').length}`);
  console.log(`  - Hooks: ${plugins.filter(p => p.type === 'hook').length}`);
  console.log(`  - Agents: ${plugins.filter(p => p.type === 'agent').length}`);
}

buildRegistry();
