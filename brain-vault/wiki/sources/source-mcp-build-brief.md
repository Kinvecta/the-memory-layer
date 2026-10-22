---
type: source
summary: Summary of the research brief (verified 20 Oct 2026) behind Deep Dive A, covering the 2026-07-28 MCP spec, v2 SDK versions, transports, OAuth authorization, real MCP incidents, a 12-point hardening checklist and change control.
sources: ["[[raw/research/mcp-build-brief]]"]
related: ["[[building-an-mcp-server]]", "[[model-context-protocol]]", "[[mcp-transports-stdio-vs-http]]", "[[prompt-injection]]", "[[source-dda-build-an-mcp-server]]", "[[secrets-management]]", "[[container-hardening]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Source brief: Building an MCP Server from Scratch

**TL;DR:** The primary research document behind [[source-dda-build-an-mcp-server]], with every version and date checked against primary sources on 20 Oct 2026 and both reference servers run and tested. Its headline: the ground moved in July 2026, so treat any earlier tutorial as legacy. It is the place to go for exact error codes, package versions, OAuth steps, incident details and the hardening checklist.

**Source file:** [[raw/research/mcp-build-brief]]  ·  **Kind:** notes (research brief)  ·  **Date:** 2026-10-20

## Key points
1. **Definition and governance** (§1.1): MCP is an open, JSON-RPC 2.0 protocol. Anthropic created it in November 2024 and donated it to the Agentic AI Foundation (AAIF) under the Linux Foundation on 9 Dec 2025. Tier-1 SDKs: TypeScript, Python, C#, Go, Rust, Ruby.
2. **Current spec 2026-07-28** (§1.4-1.5): stateless, no `initialize` handshake, no `Mcp-Session-Id`; `server/discover` is a MUST; every request self-describes in `_meta`; version mismatch is `-32022`. MRTR replaces server-initiated requests. Deprecated: roots, sampling, protocol logging, HTTP+SSE, dynamic client registration. Deprecated features keep working at least 12 months, so July 2027 is the earliest removal.
3. **Primitives** (§2.1-2.5): tools (model-controlled), resources (application-controlled), prompts (user-controlled). Annotation defaults: `readOnlyHint` false, `destructiveHint` true, `idempotentHint` false, `openWorldHint` true. Annotations are untrusted hints. Input-validation failures should be tool execution errors (`isError: true`) so the model can self-correct.
4. **Transports** (§3): stdio (stdout is the wire; credentials from environment) and streamable HTTP (single POST endpoint, `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name` headers; mismatch is `-32020`). HTTP+SSE deprecated. See [[mcp-transports-stdio-vs-http]].
5. **Versions verified 20 Oct 2026** (§5.1): Python `mcp` 2.3.0; TypeScript `@modelcontextprotocol/server` 2.3.1 (ESM only, Node 20+, Zod v4); Inspector 2.11.0 (Node 22.19.0+). v2 servers answer both protocol eras.
6. **Authorization** (§4): server is an OAuth 2.1 resource server; PRM (RFC 9728) required; auth code + PKCE with the `resource` parameter (RFC 8707); `iss` check (RFC 9207); 401 for bad tokens, 403 `insufficient_scope` for step-up. Token passthrough forbidden; use own credentials or token exchange downstream.
7. **Common errors** (§6.4): stray stdout output, relative paths in host config, missing env vars, v1 imports on v2, `421` from the DNS-rebinding guard, decline loop ending in `INPUT_REQUIRED_ROUNDS_EXCEEDED`.
8. **Client connection details** (§7): Claude Code warns above 10,000 tokens of tool output and caps at 25,000 by default; ChatGPT Developer Mode treats tools as writes needing confirmation unless `readOnlyHint` is set. The official MCP Registry is metadata-only, still preview, does not vet security, and has no private servers; government should run a private registry.
9. **Threats with incidents** (§8.1): Invariant Labs tool poisoning (Apr 2025); WhatsApp rug pull demo; GitHub "toxic agent flow" (26 May 2025); Asana cross-tenant leak (~1,000 orgs, offline 4-17 Jun 2025); `postmark-mcp` backdoor (v1.0.16, 1,643 downloads); `mcp-remote` CVE-2025-6514 (CVSS 9.6); Inspector CVE-2025-49596 (CVSS 9.4); TS SDK CVE-2025-66414. OX Security's April 2026 STDIO-config claim is vendor research with CVE-list inconsistencies.
10. **Hardening checklist** (§8.3): 12 items covering least privilege, human confirmation, input validation, output hygiene, auth, state handles, rate limits, audit, network, secrets, supply chain and isolation. Summarized in [[building-an-mcp-server]].
11. **Change control** (§9.3): treat the tool surface as an API contract; golden-file snapshot of `tools/list` in CI; semver rules; deprecate, don't delete.
12. **Uncertainties** (end): host support for 2026-07-28 not confirmed; registry still preview; OWASP MCP Top 10 in beta; Dockerfile not built.

## Worth quoting
> "Treat any tutorial dated before July 2026 as legacy."

> Servers "should not be able to read the whole conversation, nor 'see into' other servers."

> "More surface = more risk and worse tool selection. Keep tools few, focused and well described."

## Pages this source updated
- [[building-an-mcp-server]]
- [[model-context-protocol]]
- [[mcp-transports-stdio-vs-http]]
- [[prompt-injection]]
