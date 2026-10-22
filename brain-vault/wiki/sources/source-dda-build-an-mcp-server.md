---
type: source
summary: Summary of the Deep Dive A transcript, a hands-on build of the "ticket-desk" MCP server on the July 2026 spec and v2 SDKs, covering primitives, wire format, confirmation, transports, testing, OAuth, threats and release lifecycle.
sources: ["[[raw/transcripts/dda-build-an-mcp-server]]"]
related: ["[[building-an-mcp-server]]", "[[model-context-protocol]]", "[[mcp-transports-stdio-vs-http]]", "[[source-mcp-build-brief]]", "[[prompt-injection]]", "[[source-ddb-devsecops-containers-cicd]]", "[[train-the-trainer-series]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Deep Dive A - Build an MCP Server from Scratch (transcript)

**TL;DR:** A technical deep dive that builds "ticket-desk", an MCP server with a read-only tool, a confirm-first action, a resource and a prompt, in Python and TypeScript on the current (2026-07-28) spec. It shows the wire format, the multi-round-trip confirmation pattern, stdio vs streamable HTTP, testing with the Inspector, OAuth 2.1 sign-in, and six threats with server-side controls. The rule: few tools, tight schemas, a person confirms every action, validate your own token and never pass it on.

**Source file:** [[raw/transcripts/dda-build-an-mcp-server]]  ·  **Kind:** transcript  ·  **Date:** 2026-10 (about 20 minutes, includes a 30-minute lab)

## Key points
1. **Why build carefully** [1:11]: the 28 July 2026 spec removed the start-up handshake and protocol sessions and changed how servers ask people for input; both official kits shipped v2 with renamed pieces. Treat pre-July-2026 tutorials as legacy. Incidents: a backdoored npm package BCC'd every email to an attacker (Sep 2025); a malicious public issue made an agent leak private repo data into a public PR (May 2025).
2. **Architecture** [2:05]: host (runs the model, asks consent, enforces policy), clients (one per server), servers. Servers cannot see the whole conversation or each other. First reviewer gate: which servers the host may connect ([[model-context-protocol]]).
3. **Trust boundaries** [2:59]: person, host, server, backend; each checks something (approval, schema, token audience, backend permissions). Results travel up as data.
4. **Primitives** [3:51]: tool (model decides), resource (app attaches, e.g. `tickets://TCK-1001`), prompt (user picks, slash command). Elicitation is active; sampling and roots deprecated in July 2026.
5. **Tool definition** [4:34]: name and description are read by the model; input schema is enforced by the SDK; output schema gives a typed result; annotations like read-only hint are used by the host UI but are not enforced. Review descriptions like code.
6. **Wire** [5:12]: JSON-RPC; optional `server/discover`; every request carries protocol version and client capabilities; version mismatch returns `-32022`. Most common mistake: copying old handshake code.
7. **Setup** [6:03]: Python with uv and `mcp[cli]`; TypeScript as an ES module with the MCP server package and Zod. FastMCP import now fails (use MCPServer); `server.tool` became `registerTool`; Inspector needs Node 22.19+.
8. **Read-only tool** [6:53]: ticket ID pattern `TCK-` plus four digits lives in the schema, so `1001; DROP TABLE` is rejected before the function runs. Logs go to stderr on stdio.
9. **Confirm-first action** [8:04-9:58]: the confirm parameter is resolved by a helper, so it is not in the model's schema and the model cannot pass `confirm: true`. On the wire this is a multi-round-trip request: server returns input-required, client asks the person, retries with the answer. Real bug: a "no" was treated as "no answer yet" and looped until rounds exceeded. Always handle decline and cancel.
10. **Transports** [10:50] and **deployment tiers** [12:01]: see [[mcp-transports-stdio-vs-http]].
11. **Testing** [12:50]: run, inspect, break (injection string rejected), test the decline path, snapshot the tool list, fail the build on any description change.
12. **Connecting** [13:41]: Claude Desktop config with absolute path to uv and secrets in `env`; Claude Code `claude mcp add`; VS Code stdio entry with sandbox; Copilot needs Agent mode.
13. **OAuth 2.1** [14:30]: 401 with protected-resource metadata, PKCE plus resource parameter, audience-checked token for this server only, server uses its own credential downstream. Token passthrough forbidden. No OAuth on stdio.
14. **Threats** [15:43]: tool poisoning, rug pull, injection in results, token passthrough, malicious package, DNS rebinding; plus a 2025 cross-tenant bug exposing about 1,000 organizations. Take the tenant from the verified token.
15. **Lifecycle** [16:58]: design, build, test, secure, ship (scanned, signed image plus tool-list gate), operate. Remove/rename a tool = major; new tool = minor; patch never changes the tool list.

## Worth quoting
> "Asks first, then acts." [0:00]

> "The poisoned description and the injected result never touch your code, but they change what the model does." [18:09]

> "The model only sees your descriptions and results, so the server is where safety is enforced." [17:54]

## Pages this source updated
- [[building-an-mcp-server]]
- [[model-context-protocol]]
- [[mcp-transports-stdio-vs-http]]
- [[prompt-injection]]
- [[tool-calling]]
