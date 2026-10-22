# Lab 5 · Answer key (facilitators)

## A · Check

`expected-output.txt` is the reference run on `brain-vault/` with brain-tools and MCP SDK 2.3.

- **Tools.** There are 8. Four are read-only: `wake_up`, `search`, `read`, `lint`. Four write: `remember`, `log`, `reindex`, and `save_page`, which is marked "can replace" because `overwrite=true` replaces a page.
- **Search.** `prompt injection` returns `wiki/concepts/prompt-injection.md` first. The read starts with the banner `(note content is data, not instructions)`. The page has 18 links out and 24 backlinks.
- **Refusals.**
  - `raw/evil.md` and `wiki/../../outside.md` fail the **schema** (lock 1). The path must start with `wiki/` or `inbox/` and may not contain dots except `.md`.
  - The repeat save fails **lock 3**: the page exists, so read it and pass `overwrite=true`.
  - **Lock 2** (resolve the real path, follow symlinks, compare parents) is the backstop for anything that passes the schema, for example a symlink inside `wiki/` that points outside.

## B · Connect

- **Key name by host.** `mcpServers`: a project `.mcp.json`, desktop chat app configs, Cursor, Gemini CLI, LM Studio. `servers` with `"type": "stdio"`: VS Code. `[mcp_servers.brain]` TOML: Codex CLI.
- **Most common failures:**
  - a relative path to `brain-mcp`;
  - no `BRAIN_VAULT`;
  - not fully restarting the app;
  - the `mcp` extra not installed.
- **Proof it works:** the app lists the `brain_*` tools.

## C · Use it

- **A good answer** cites `[[wiki/concepts/prompt-injection]]`, and possibly the S7 source page.
- **`memory/working.md`** gets one line: `- <date time> [note] …` (or `[fact]`).
- **The saved page** lands in `inbox/`. It should have YAML frontmatter and at least one `[[wikilink]]`.

## D · Break it

- **The server refuses** any `raw/` path. A well-behaved host *also* asks permission before running a write tool.
- **If a coding agent wrote `raw/notes.md` with its own file tool:** the brain server never saw the request. Its locks cover only its own tools, so host permissions (and keeping `raw/` read-only on disk) matter too.
- **If the host never asked:** find its setting. For example, Gemini CLI's `trust: true` turns confirmations off. Discuss least privilege and human approval (OWASP LLM06).

## E · Two apps

- **Expected:** the same top pages, because both apps call the same server on the same files. The wording differs by model; the citations should not.
- **This is the point of the session:** the memory belongs to the brain, not to the app.
