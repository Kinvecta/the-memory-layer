#!/usr/bin/env bash
# Copy the vault's skills into the folders each harness auto-discovers.
#   Claude Code / Cowork : <vault>/.claude/skills/
#   Codex / Agent Skills : <vault>/.agents/skills/
# Usage: ./install-skills.sh /path/to/brain-vault
set -euo pipefail
VAULT="${1:-${BRAIN_VAULT:-.}}"
for dest in .claude/skills .agents/skills; do
  mkdir -p "$VAULT/$dest"
  for s in "$VAULT"/skills/*/; do
    name="$(basename "$s")"
    rm -rf "$VAULT/$dest/$name"
    cp -R "$s" "$VAULT/$dest/$name"
  done
  echo "Installed $(ls "$VAULT/skills" | wc -l | tr -d ' ') skills into $VAULT/$dest"
done
