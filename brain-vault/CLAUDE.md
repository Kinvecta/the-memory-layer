# CLAUDE.md

This vault is a second brain. The full operating manual is in AGENTS.md, which every harness shares:

@AGENTS.md

## Claude-specific notes

- Skills live in `skills/`. Running `brain-tools/install-skills.sh` copies them into `.claude/skills/`,
  which lets Claude Code and Cowork load them automatically. The same script fills `.agents/skills/`
  for Codex and other harnesses that read the Agent Skills format.
- Prefer the `brain` CLI or the `brain` MCP server for search. Use plain Read and Grep for exact lookups.
- When you finish an ingest or lint, run `git add -A && git commit -m "<op>: <what>"` if the vault is a git repo.
