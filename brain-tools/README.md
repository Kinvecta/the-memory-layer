# brain-tools

This package handles recall, upkeep and the MCP server for the `brain-vault/` folder, or for any markdown vault.

The core needs only the Python 3.10+ standard library: keyword search, lint, memory and heartbeat. Two pieces are optional:

- **Ollama.** Adds semantic search, which runs fully local.
- **The `mcp` package.** Needed only for the MCP server.

## Install (macOS)

```bash
cd brain-tools
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[mcp]"                  # use ".[dev]" to also run the tests
export BRAIN_VAULT="$(cd ../brain-vault && pwd)"   # put this line in ~/.zshrc

# Optional: semantic search
brew install ollama && ollama serve &    # or install the Ollama app
ollama pull nomic-embed-text

brain index                              # builds .brain/index.sqlite inside the vault
brain search "how do I stop prompt injection"
```

## Commands

| Command | What it does |
|---|---|
| `brain wake` | Prints core memory, working memory and the index. This is the start-of-session load. |
| `brain search "q" [-k 6] [--mode hybrid\|keyword\|semantic] [--folder wiki/]` | Hybrid recall. Keyword (BM25) and semantic results are merged with RRF. Wiki pages rank above raw sources. |
| `brain index [--no-embed]` | Incremental re-index. Only changed files are re-embedded. |
| `brain remember "fact" --kind decision` | Appends a line to `memory/working.md`. |
| `brain archive --title "..."` | Moves working memory into `memory/episodes/`. |
| `brain lint [--write]` | Lists broken links, orphans, pages missing from the index, stale pages, and raw files with no source page. |
| `brain heartbeat [--llm "claude -p"]` | Archives working memory, re-indexes and lints, then optionally runs the brain-reflect skill headless. |
| `brain serve [--http]` | Starts the MCP server. |

Without Ollama, the hybrid and semantic modes fall back to keyword search.

## Connect an MCP host

**Claude Code**

```bash
claude mcp add brain -e BRAIN_VAULT="$BRAIN_VAULT" -- "$PWD/.venv/bin/brain-mcp"
```

**Claude Desktop, Cursor, or any other stdio host** (in the host's MCP config JSON):

```json
{
  "mcpServers": {
    "brain": {
      "command": "/ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp",
      "env": { "BRAIN_VAULT": "/ABSOLUTE/PATH/brain-vault" }
    }
  }
}
```

**Shared or remote host:** run `brain serve --http --port 8765`, which serves `http://127.0.0.1:8765/mcp`. It binds to localhost only. Put a reverse proxy with auth in front of it before you expose it anywhere (see Deep Dive A on OAuth).

**Tools exposed:** `brain_wake_up`, `brain_search`, `brain_read` (includes backlinks), `brain_remember`, `brain_save_page`, `brain_log`, `brain_lint`, `brain_reindex`. There are two resources, `brain://index` and `brain://core`, and one prompt, `ask_brain`.

**Guardrails built into the server:**

- Writes only go under `wiki/`, `inbox/` and `memory/`, plus append-only writes to `log.md`.
- `raw/` is read-only.
- Paths that try to escape the vault (path traversal) are rejected.
- Every read is labeled "data, not instructions".

## Heartbeat on a schedule

`examples/com.brain.heartbeat.plist` runs the heartbeat every day at 6:15 on macOS. To use it:

1. Edit the paths in the plist and check it with `plutil -lint`.
2. Copy it to `~/Library/LaunchAgents/`.
3. Run `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.brain.heartbeat.plist`, then
   `launchctl kickstart gui/$(id -u)/com.brain.heartbeat` to test it once.

If the Mac is asleep at 6:15, launchd runs the job when it wakes (missed runs collapse into one). If it is off, the run is skipped.

Cron equivalent (cron skips runs missed while asleep or off):

```
15 6 * * * cd /path/brain-vault && /path/brain-tools/.venv/bin/brain heartbeat --commit >> .heartbeat.log 2>&1
```

What one run does:

- archive working memory, re-index, lint, and write `memory/reports/<date>.md`
- `--commit`: one git commit per run, so you can review it with `git show` and undo it with `git revert`; it skips the run if the vault has uncommitted human edits
- `--llm "<command>"`: an optional headless reflect step that **proposes** changes (wiki edits with sources, working memory, a briefing and any core-memory proposal in `inbox/`). It never edits `raw/` or `memory/core.md`. Give it file tools only, no network tools.
- **quarantine**: if lint flags hidden characters or instruction-like lines in `raw/` or `inbox/`, the reflect step is skipped and the report says why. After reading a flagged file yourself, list it in `memory/reviewed-flags.md` to stop the flag.

## Skills into each harness

```bash
./install-skills.sh "$BRAIN_VAULT"   # copies skills/ into .claude/skills and .agents/skills
```

## Tests

```bash
pip install -e ".[dev]" && pytest -q   # 17 tests: parsing, search, lint, write guards, memory, heartbeat quarantine, MCP
```
