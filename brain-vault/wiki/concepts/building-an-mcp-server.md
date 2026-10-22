---
type: concept
summary: How to build a current (2026-07-28 spec, v2 SDK) MCP server safely, using the ticket-desk example: tight schemas, a confirm-first action, stderr logging, Inspector tests, tool-list snapshots, OAuth without token passthrough, and a 12-point hardening checklist.
sources: ["[[raw/transcripts/dda-build-an-mcp-server]]", "[[raw/research/mcp-build-brief]]", "[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[model-context-protocol]]", "[[mcp-transports-stdio-vs-http]]", "[[tool-calling]]", "[[prompt-injection]]", "[[devsecops-pipeline]]", "[[container-hardening]]", "[[secrets-management]]", "[[image-signing-and-provenance]]", "[[ai-governance-and-controls]]"]
aliases: ["MCP server build", "ticket-desk"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Building an MCP server

**TL;DR:** Build on the v2 SDKs and the 2026-07-28 spec; anything older is legacy. Keep tools few with tight schemas, make every side effect ask a person first (and handle "no"), log to stderr on stdio, snapshot the tool list in CI, and on HTTP validate your own token and never pass it on. The model only sees your descriptions and results, so the server is where safety is enforced.

## What it is
The hands-on path taught in [[source-dda-build-an-mcp-server]], backed by [[source-mcp-build-brief]]. The running example, **ticket-desk**, has one read-only tool (`get_ticket`), one action that requires confirmation (`close_ticket`), one resource template (`tickets://{id}`) and one prompt (`triage_ticket`). Concepts are in [[model-context-protocol]].

## Why it matters
A server acts with your authority, a probabilistic model picks the tool, and results flow straight into the model's context (brief §8). Incidents are real: the `postmark-mcp` npm backdoor BCC'd every email to an attacker (Sep 2025, 1,643 downloads); an Asana MCP logic bug exposed data across about 1,000 customer organizations (2025).

## How it works
**Setup, verified 20 Oct 2026** (brief §5.1): Python `uv add "mcp[cli]"` (mcp 2.3.0, Python 3.10+); TypeScript `npm install @modelcontextprotocol/server zod` (2.3.1, ESM only, Node 20+); Inspector 2.11.0 needs Node 22.19.0+. Legacy traps: `from mcp.server.fastmcp import FastMCP` now fails (use `MCPServer`); `server.tool()` became `registerTool()`.

**Build** (DDA 6:53-9:58):
- Type hints are the schema. A pattern like `^TCK-\d{4}$` rejects `1001; DROP TABLE` before your function runs, returning an error the model can read and fix.
- Set honest annotations (`readOnlyHint`), but they are hints, not enforcement.
- For actions, resolve the confirmation outside the model's schema so the model cannot pass `confirm: true`. The server returns `input_required`; the client asks the person and retries.
- **Always handle decline and cancel.** A real bug treated "no" as "no answer yet" and looped until `INPUT_REQUIRED_ROUNDS_EXCEEDED`.
- On stdio, stdout is the wire: log to stderr ([[mcp-transports-stdio-vs-http]]).

**Test like a reviewer** (DDA 12:50): run it (silence on stdio is correct); list tools with the Inspector CLI; break it with an injection string; confirm "no" leaves the ticket open; commit a `tools/list` snapshot; fail CI when the live list differs. Test both protocol eras if you support older hosts. Without an OS keychain the Inspector stores secrets unencrypted.

**Secure (remote)** (DDA 14:30; brief §4): OAuth 2.1 with protected-resource metadata, PKCE and the `resource` parameter; check audience; 401 for bad token, 403 for missing scope; small scopes; no tokens in URLs. Downstream, use the server's own credential. **Token passthrough is forbidden.** Take the tenant from the verified token, never from an argument.

**Ship and operate** (DDA 16:58): scanned, signed image plus a tool-list gate ([[image-signing-and-provenance]], [[devsecops-pipeline]]); logs, audit, rate limits, alert on tool-list change. Semver: remove/rename a tool = major; new tool = minor; patch never changes the tool list. Deprecate before you delete.

## In practice
**Hardening checklist** (brief §8.3, condensed):
1. Least privilege; read-only by default; narrow action tools.
2. Human confirmation for side effects; never rely on hints.
3. Tight input schemas (`pattern`, `enum`, `maxLength`).
4. Output hygiene: needed fields only, no secrets or PII, small results.
5. OAuth 2.1, audience check, no passthrough.
6. Unguessable, user-bound, expiring state handles.
7. Rate limits (a spec MUST) and timeouts.
8. Structured audit logs to the SIEM.
9. Bind localhost, Host/Origin allow-list, TLS, egress allow-list ([[egress-control-and-firewalls]]).
10. Secrets from environment or a manager ([[secrets-management]]).
11. Pinned versions, lockfiles, digests, SBOM, internal mirror.
12. Container as non-root, read-only filesystem, dropped capabilities ([[container-hardening]]).

**Connecting a host** (DDA 13:41): Claude Desktop config with the absolute path to `uv` and secrets in `env`; `claude mcp add` in Claude Code; VS Code stdio entry with sandbox; Copilot only calls tools in Agent mode.

> [!tip] Lab aha
> Poisoned descriptions and injected results never touch your code, yet change what the model does. Schema, confirmation and snapshot catch them ([[prompt-injection]]).

## See also
[[model-context-protocol]] · [[mcp-transports-stdio-vs-http]] · [[tool-calling]] · [[source-ddb-devsecops-containers-cicd]]
