# Lab 5 · Add the brain to your AI app

Replace `/ABSOLUTE/PATH` with your real paths:

- `brain-mcp` lives in the virtual environment where you installed brain-tools, for example `brain-tools/.venv/bin/brain-mcp`.
- Use the full path. Many apps don't load your shell's PATH.

After you edit a config, **fully quit and restart the app**, then check that the `brain_*` tools are listed.

## Most apps: `mcpServers` (JSON)

Use this in a project `.mcp.json`, a desktop chat app's config file, Cursor (`.cursor/mcp.json`), Gemini CLI (`settings.json`) and LM Studio (`mcp.json`):

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

Example add commands (check your app's docs):

```
claude mcp add brain -e BRAIN_VAULT=/ABSOLUTE/PATH/brain-vault -- /ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp
gemini mcp add -e BRAIN_VAULT=/ABSOLUTE/PATH/brain-vault brain /ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp
```

## IDEs that use `servers` (JSON), for example VS Code `.vscode/mcp.json`

```json
{
  "servers": {
    "brain": {
      "type": "stdio",
      "command": "/ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp",
      "env": { "BRAIN_VAULT": "/ABSOLUTE/PATH/brain-vault" }
    }
  }
}
```

## CLIs that use TOML, for example Codex `~/.codex/config.toml`

```toml
[mcp_servers.brain]
command = "/ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp"

[mcp_servers.brain.env]
BRAIN_VAULT = "/ABSOLUTE/PATH/brain-vault"
```

## Sharing one brain over HTTP (advanced; not needed for the lab)

```
brain serve --http --port 8765      # serves http://127.0.0.1:8765/mcp, localhost only
```

The server rejects requests from other web origins (HTTP 403), but it has **no login**. Only share it behind a reverse proxy that adds authentication.

## Troubleshooting

- **Tools don't appear.** The path is wrong or the app wasn't restarted. Run the command in a terminal: it should print one `vault: …` line and then wait. Press Ctrl-C to stop it.
- **"No module named mcp".** Install the extra: `pip install -e "brain-tools[mcp]"`.
- **Search finds nothing.** Run `brain index` in the vault first.
