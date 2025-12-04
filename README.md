# Claude Code Plugins Marketplace

Community-driven marketplace for Claude Code plugins, commands, and hooks.

## Plugin Types

### MCP Servers
Model Context Protocol servers that extend Claude Code's capabilities with new tools and integrations.

### Slash Commands
Custom commands that can be invoked with `/command-name` in Claude Code.

### Hooks
Event-driven scripts that run automatically in response to Claude Code actions.

## Installation

### Installing MCP Servers

1. Find the plugin in `plugins/mcp-servers/`
2. Copy the configuration from the `install.config` field
3. Add it to your `~/.claude/settings.json` or Claude Desktop config

Example:
```bash
# View plugin details
cat plugins/mcp-servers/github.json

# The install.config shows what to add to your settings
```

### Installing Slash Commands

1. Find the command in `plugins/commands/`
2. Run the install command or manually copy the file

Example:
```bash
# Install review-pr command
curl -o ~/.claude/commands/review-pr.md https://raw.githubusercontent.com/claude-code-community/commands/main/review-pr.md
```

### Installing Hooks

1. Find the hook in `plugins/hooks/`
2. Add the hook configuration to your `~/.claude/settings.json`

Example:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint -- --fix $CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

## Available Plugins

### MCP Servers
| Plugin | Description | Tags |
|--------|-------------|------|
| [mcp-github](plugins/mcp-servers/github.json) | GitHub API integration | github, git, issues |
| [mcp-filesystem](plugins/mcp-servers/filesystem.json) | Secure filesystem access | files, directories |
| [mcp-postgres](plugins/mcp-servers/postgres.json) | PostgreSQL database integration | database, sql |
| [mcp-puppeteer](plugins/mcp-servers/puppeteer.json) | Browser automation | browser, screenshots |
| [mcp-sequential-thinking](plugins/mcp-servers/sequential-thinking.json) | Structured reasoning | thinking, problem-solving |

### Commands
| Plugin | Description | Usage |
|--------|-------------|-------|
| [review-pr](plugins/commands/review-pr.json) | PR code review | `/review-pr <number>` |
| [create-component](plugins/commands/create-component.json) | Scaffold components | `/create-component <name>` |
| [git-conventional](plugins/commands/git-conventional.json) | Conventional commits | `/commit` |
| [explain-codebase](plugins/commands/explain-codebase.json) | Codebase documentation | `/explain` |

### Hooks
| Plugin | Description | Event |
|--------|-------------|-------|
| [auto-lint](plugins/hooks/auto-lint.json) | Auto-lint after edits | PostToolUse |
| [auto-test](plugins/hooks/auto-test.json) | Run related tests | PostToolUse |
| [notify-slack](plugins/hooks/notify-slack.json) | Slack notifications | Stop |
| [security-scan](plugins/hooks/security-scan.json) | Block dangerous commands | PreToolUse |

## Contributing

### Adding a New Plugin

1. Fork this repository
2. Create a new JSON file in the appropriate directory:
   - `plugins/mcp-servers/` for MCP servers
   - `plugins/commands/` for slash commands
   - `plugins/hooks/` for hooks
3. Follow the schema in `schemas/plugin.schema.json`
4. Submit a pull request

### Plugin Schema

All plugins must conform to the JSON schema at `schemas/plugin.schema.json`.

Required fields:
- `name`: Unique plugin identifier (lowercase, hyphens only)
- `version`: Semantic version (e.g., "1.0.0")
- `description`: Brief description
- `type`: One of "mcp-server", "command", or "hook"
- `author`: Object with at least `name` field

### Validation

```bash
# Validate a plugin against the schema
npm run validate plugins/mcp-servers/your-plugin.json
```

## Registry API

The marketplace provides a JSON registry at `registry.json` for programmatic access:

```bash
# Fetch all plugins
curl https://claude-code-marketplace.github.io/registry.json

# Filter by type
curl https://claude-code-marketplace.github.io/registry.json | jq '.plugins[] | select(.type == "mcp-server")'
```

## License

MIT - See individual plugins for their specific licenses.
