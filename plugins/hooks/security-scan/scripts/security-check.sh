#!/bin/bash
# Security check script for Claude Code
# Blocks potentially dangerous commands

COMMAND="$CLAUDE_TOOL_INPUT"

# Dangerous patterns
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "dd if="
  "mkfs"
  "> /dev/sd"
  "chmod 777"
  "curl.*|.*sh"
  "wget.*|.*sh"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: Potentially dangerous command detected: $pattern"
    exit 1
  fi
done

exit 0
