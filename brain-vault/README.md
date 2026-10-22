# The Memory Layer: reference vault

This is a "second brain" built from plain markdown. People read it in Obsidian. Any AI harness can recall
from it, including Claude Code, Cowork, Codex, Gemini CLI, Cursor, and local models.

## Open it

- **Obsidian:** choose *Open folder as vault* and select this folder. Graph view, backlinks and
  properties work out of the box.
- **Any editor:** it is just a folder of `.md` files.

## Point an AI at it

| Harness | How |
|---|---|
| Claude Code / Cowork | Start in this folder. `CLAUDE.md` loads `AGENTS.md`. Run `../brain-tools/install-skills.sh .` once to install the skills. |
| Codex, Cursor, OpenCode | They read `AGENTS.md` automatically. Skills are installed to `.agents/skills/`. |
| Gemini CLI | `GEMINI.md` imports `AGENTS.md`. |
| Claude Desktop or any MCP host | Add the `brain` MCP server (see `../brain-tools/README.md`). |
| Anything else | Paste `memory/core.md` and `index.md` into the chat, then ask it to request pages by path. |

## Map

- `AGENTS.md`: the operating manual. Read it first.
- `index.md`: the catalog.
- `log.md`: the audit trail.
- `memory/`: core, working, episodes and reports.
- `raw/`: immutable sources.
- `wiki/`: compiled knowledge.
- `skills/`: ingest, query, lint, remember and reflect.
- `templates/`: page templates.
