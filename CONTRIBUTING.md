# Contributing to Claude Code Plugins Marketplace

Thank you for your interest in contributing! This guide will help you add your plugins to the marketplace.

## Types of Contributions

### 1. MCP Servers
Model Context Protocol servers that provide new tools and capabilities to Claude Code.

### 2. Slash Commands
Custom commands that users can invoke with `/command-name`.

### 3. Hooks
Event-driven scripts that run automatically during Claude Code operations.

## How to Contribute

### Step 1: Fork the Repository

```bash
gh repo fork claude-code-marketplace/claude-code-marketplace
git clone https://github.com/YOUR_USERNAME/claude-code-marketplace
cd claude-code-marketplace
```

### Step 2: Create Your Plugin File

Create a new JSON file in the appropriate directory:

```
plugins/
├── mcp-servers/    # MCP server plugins
├── commands/       # Slash command plugins
└── hooks/          # Hook plugins
```

### Step 3: Follow the Schema

Your plugin must conform to `schemas/plugin.schema.json`. Here's a minimal example:

```json
{
  "$schema": "../../schemas/plugin.schema.json",
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "Brief description of what your plugin does",
  "type": "mcp-server",
  "author": {
    "name": "Your Name",
    "github": "your-github-username"
  },
  "repository": "https://github.com/you/your-plugin",
  "license": "MIT",
  "tags": ["relevant", "tags"],
  "install": {
    // Installation instructions
  }
}
```

### Step 4: Validate Your Plugin

```bash
npm install
npm run validate plugins/mcp-servers/your-plugin.json
```

### Step 5: Submit a Pull Request

```bash
git checkout -b add-your-plugin
git add plugins/mcp-servers/your-plugin.json
git commit -m "Add your-plugin MCP server"
git push origin add-your-plugin
```

Then open a pull request on GitHub.

## Plugin Guidelines

### Naming
- Use lowercase with hyphens: `my-awesome-plugin`
- Prefix with type for clarity: `mcp-`, `command-`, `hook-`

### Description
- Keep it under 100 characters
- Explain what the plugin does, not how

### Tags
- Use 3-5 relevant tags
- Use existing tags when possible
- Common tags: `github`, `database`, `testing`, `automation`

### Installation
- Provide complete installation instructions
- Include all required environment variables
- Test your installation steps

### Security
- Never include API keys or secrets
- Use environment variable placeholders: `${API_KEY}`
- Document required permissions

## MCP Server Specifics

For MCP servers, include the `mcp` field:

```json
{
  "mcp": {
    "tools": ["tool1", "tool2"],
    "resources": ["resource://pattern"],
    "prompts": ["prompt1"]
  }
}
```

## Command Specifics

For commands, include the `command` field:

```json
{
  "command": {
    "name": "command-name",
    "arguments": [
      {
        "name": "arg1",
        "required": true,
        "description": "What this argument does"
      }
    ]
  }
}
```

## Hook Specifics

For hooks, include the `hook` field:

```json
{
  "hook": {
    "event": "PostToolUse",
    "matcher": "Edit|Write"
  }
}
```

Valid events:
- `PreToolUse` - Before a tool runs
- `PostToolUse` - After a tool runs
- `Notification` - On notifications
- `Stop` - When Claude Code stops
- `SubagentStop` - When a subagent stops

## Review Process

1. Automated validation checks run on PR
2. A maintainer reviews your submission
3. We may request changes or clarifications
4. Once approved, your plugin is merged and available

## Questions?

- Open an issue for questions
- Join our Discord community
- Check existing plugins for examples

Thank you for contributing!
