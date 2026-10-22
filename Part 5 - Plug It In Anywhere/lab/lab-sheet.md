# Lab 5 · Plug it in. Try to break it. (20 min)

You need:

- a copy of `brain-vault/` (work in the copy);
- brain-tools with the MCP extra: `pip install -e "brain-tools[mcp]"` (MCP Python SDK 2.x);
- one AI app that supports MCP.

## A · Check (4 min)

```
python3 mcp_check.py ~/brain-copy
```

This script plays the part of an AI app. It talks to the brain server over stdio. You should see:

- 8 tools: 4 read-only, 4 that write;
- a search, a read (with the data banner) and a remembered fact;
- one page saved to `inbox/`;
- three refusals.

Compare your output with `expected-output.txt`.

## B · Connect (6 min)

1. Pick your app and copy the matching snippet from `host-configs.md`.
2. Use absolute paths.
3. Restart the app fully, then confirm the `brain_*` tools are listed.

## C · Use it (5 min)

1. Ask: "What is prompt injection? Use the brain and cite pages."
2. Say: "Remember that I connected the brain over MCP today." Then open `memory/working.md` and find the new line.
3. Say: "Save a short page about MCP transports to inbox/." Then find it in `inbox/`.

## D · Break it (3 min)

Say: "Use the brain tools to save a summary to raw/notes.md."

- `brain_save_page` must refuse.
- If your app wrote the file with its own file tool instead, note it: the server's locks only cover the server's tools.
- Did your app ask your permission before any write? Note what it did.

## E · Two apps (2 min)

Connect a second app to the **same** vault and ask the same question as in step C.

- Same pages?
- Same answer?

**Debrief:**

- Which config key did your app use: `mcpServers`, `servers` or `mcp_servers`?
- Did it ask before writing?
