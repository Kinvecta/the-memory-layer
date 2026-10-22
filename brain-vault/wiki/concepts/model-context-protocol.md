---
type: concept
summary: MCP is the open JSON-RPC standard (current revision 2026-07-28, governed by the Linux Foundation's AAIF) for plugging tools, resources and prompts into any harness through host, client and server roles.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s7-tools-mcp-and-prompt-injection]]", "[[raw/transcripts/dda-build-an-mcp-server]]", "[[raw/research/mcp-build-brief]]"]
related: ["[[tool-calling]]", "[[building-an-mcp-server]]", "[[mcp-transports-stdio-vs-http]]", "[[ai-harness]]", "[[agnostic-ai-platform]]", "[[prompt-injection]]", "[[agent-skills]]", "[[containerization]]"]
aliases: ["MCP", "Model Context Protocol"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Model Context Protocol (MCP)

**TL;DR:** MCP is the open standard for connecting a harness to tools: build one server for a system such as a ticketing tool, and any harness that speaks MCP (chat app, workflow or agent) can use it. The harness, not the server, enforces permissions and approvals, and the model never talks to the server directly. As of Oct 2026 the current spec revision is 2026-07-28, which removed the old handshake and sessions.

## What it is
An open, JSON-RPC 2.0 protocol that lets AI applications (hosts) connect to capability providers (servers) in a standard way ([[source-mcp-build-brief]] §1.1). Anthropic created it in November 2024 and donated it to the Agentic AI Foundation (AAIF), under the Linux Foundation, on 9 Dec 2025. It is supported by OpenAI, Microsoft/GitHub, Google, AWS, Cursor and others; it is not Claude-only (§10.3).

**Roles** (§1.2; [[source-dda-build-an-mcp-server]] 2:05):
- **Host:** the AI app. Runs the model, asks for consent, enforces policy.
- **Client:** a connector inside the host, one per server.
- **Server:** your program, local (stdio) or remote (HTTP). See [[mcp-transports-stdio-vs-http]].

Servers "should not be able to read the whole conversation, nor 'see into' other servers."

**Primitives, by who controls them** (brief §2.1):

| Primitive | Controlled by | Example |
|---|---|---|
| Tool | Model | `get_ticket`, `close_ticket` |
| Resource | Application | `tickets://TCK-1001` |
| Prompt | User (slash command) | `/triage_ticket` |

Elicitation (server asks the person for input) is active; sampling and roots were deprecated in 2026-07-28.

## Why it matters
- **Portability.** One server serves many harnesses, the same portability [[agent-skills]] give to know-how ([[source-ai-training-guide]] §2.1; [[agnostic-ai-platform]]).
- **Control.** Three points from the guide: the server runs in a container and reaches only its approved systems; the harness enforces permissions and approval gates; whatever a tool returns is untrusted content ([[prompt-injection]]).

## How it works
**Six-step call** ([[source-s7-tools-mcp-and-prompt-injection]] 2:38; guide Figure 6): connect, list tools, model asks, harness checks and logs, harness runs the approved call, result returns as data. That is why permissions, approvals and logging live in the harness.

**On the wire, as of 2026-07-28** (brief §1.4):
- Stateless: no `initialize` handshake, no `Mcp-Session-Id`. Every request carries protocol version and client capabilities in `_meta`.
- Servers MUST implement `server/discover`; a version mismatch returns `-32022`.
- Servers needing state mint explicit, unguessable handles passed back as tool arguments.
- **MRTR** (multi-round-trip requests): the server never pushes a request; it returns `input_required`, the client gathers answers and retries. Any instance behind a plain load balancer can answer.
- Deprecated features keep working at least 12 months (earliest removal July 2027).

> [!warning] Legacy material
> Both official SDKs shipped v2 with renamed APIs (Python `FastMCP` became `MCPServer`; TypeScript `server.tool` became `registerTool`). Treat any tutorial dated before July 2026 as legacy (brief headline).

## In practice
- Run the server in a container with egress only to its backing system ([[egress-control-and-firewalls]], [[containerization]]).
- MCP servers are software: repository, review, scanned image, snapshot of the tool list in CI ([[devsecops-pipeline]]; guide §4.1).
- The official MCP Registry stores metadata only, is still preview, and does not vet security; regulated organizations should run a private registry as the approved-server catalog (brief §7.7).
- In environments with only chat plus API, MCP servers can still serve as fixed steps in [[workflows]] (guide §2.1).

## See also
[[tool-calling]] · [[building-an-mcp-server]] · [[mcp-transports-stdio-vs-http]] · [[ai-harness]] · [[ai-governance-and-controls]]
