---
type: comparison
summary: Side-by-side of MCP's two current transports, stdio for one local user and streamable HTTP for shared or remote servers, with security differences, common errors and a decision guide (HTTP+SSE is deprecated).
sources: ["[[raw/transcripts/dda-build-an-mcp-server]]", "[[raw/research/mcp-build-brief]]"]
related: ["[[model-context-protocol]]", "[[building-an-mcp-server]]", "[[containerization]]", "[[egress-control-and-firewalls]]", "[[secrets-management]]", "[[source-dda-build-an-mcp-server]]", "[[source-mcp-build-brief]]"]
aliases: ["stdio vs streamable HTTP", "MCP transports"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# MCP transports: stdio vs streamable HTTP

**TL;DR:** Pick by who uses the server: stdio when one person runs it locally (the host spawns it as a child process and nothing listens on the network), streamable HTTP when many people share it behind a gateway with OAuth. The older HTTP+SSE transport is deprecated. Both can run in containers, and both need least access.

| | stdio | Streamable HTTP |
|---|---|---|
| Who uses it | One person, one machine (Tier A) | Team, remote, many clients (Tier B and C) |
| How it connects | Host launches server as a subprocess; newline-delimited JSON-RPC over stdin/stdout | Client sends each JSON-RPC message as a POST to one endpoint (e.g. `/mcp`); answer is JSON or a per-request SSE stream for progress |
| Required headers | None | `MCP-Protocol-Version`, `Mcp-Method`, plus `Mcp-Name` on tool calls, resource reads and prompt gets; must match the body or `400` / `-32020` |
| Credentials | From the environment; spec says stdio should not use OAuth | OAuth 2.1 resource server: PRM, PKCE, `resource` parameter, audience check; 401 / 403 |
| Who can reach it | Only the parent process (a security plus) | Anyone who can reach the URL, so gateway, TLS and Host/Origin checks matter |
| Runs with | The user's own permissions | Its own service account and least-privilege backend credential |
| Number-one bug | A stray `print()` or `console.log()` to stdout corrupts the stream and the host drops the connection | Binding to `0.0.0.0` drops the DNS-rebinding guard unless real host names are allow-listed; forged Host gets `421` |
| Logging | stderr only (stdout is the wire) | stdout is fine; OpenTelemetry recommended |
| Scaling | Single process | Stateless in 2026-07-28, so any instance behind a plain load balancer can answer |
| Typical config | Claude Desktop `mcpServers` with absolute command path and `env`; `claude mcp add ticket-desk -- uv ...`; VS Code stdio with sandbox | `claude mcp add --transport http ...`; Claude custom connectors; ChatGPT Developer Mode (remote only) |

Sources: [[source-dda-build-an-mcp-server]] 10:50 and 12:01; [[source-mcp-build-brief]] §3 and §6.4.

## When to pick which
**Pick stdio** for a personal or developer tool, anything touching local files, or a single user. Nothing listens on the network. Remember that local is not automatically safe: local servers run with the user's privileges, and DNS rebinding, malicious configs and supply-chain attacks all hit local setups (brief §10.3). Treat MCP config as code and never let a model or web input write it.

**Pick streamable HTTP** for a team or shared service that needs central auth, audit and many clients. Put TLS, OAuth token validation and rate limiting at a gateway; the token must be for this server only, and the server calls the backend with its own credential (never token passthrough). Bind locally during development and allow-list host names in production.

**Tier C, a container in a cluster** (DDA 12:01): a signed image, non-root, secrets injected at run time, and a firewall that allows the backend API and blocks unknown hosts ([[container-hardening]], [[secrets-management]], [[egress-control-and-firewalls]]). A stdio server can also be containerized and launched with `docker run -i --rm` from the host config (brief §9.1).

**Air-gapped or classified enclave:** either transport, but host the server inside the enclave; remote HTTP needs an internal identity provider, and the public registry will not apply (brief §3.5).

**Legacy client that only speaks SSE:** fix the client; add an SSE endpoint only as a time-boxed bridge. HTTP+SSE has been deprecated since 2025-03-26 (brief §3.3).

> [!tip] Rule of thumb
> "Local for one, remote for many, and always least access." (DDA 12:01)
