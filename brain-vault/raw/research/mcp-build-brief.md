# Source Brief: Building an MCP Server from Scratch (current as of 20 Oct 2026)

**Purpose.** Source material for a 90-minute train-the-trainer session (deck, facilitator guide, ~8-minute narrated video) for a mixed technical audience in government and regulated organizations.
**Method.** Every version number and date was checked against primary sources on 20 Oct 2026: the spec at modelcontextprotocol.io, the official SDK repos and docs, PyPI and npm, Anthropic/OpenAI/Microsoft docs, OWASP, and original researcher disclosures. Numbered references [n] point to the Sources section.
**Code status.** Both reference servers in Section 5 were **run and tested** on 20 Oct 2026 with `mcp` 2.3.0 (Python 3.13) and `@modelcontextprotocol/server` 2.3.1 (Node 22). The tests drove them in-process, over stdio with MCP Inspector 2.11.0 CLI, and over Streamable HTTP. Both protocol eras worked: modern 2026-07-28 and legacy `initialize`.

> **Headline for trainers: the ground moved in July 2026.** The current spec revision is **2026-07-28**. It removed the `initialize`/`initialized` handshake and protocol-level sessions, and it changed how servers ask users for input [1][2][3]. Both official SDKs shipped new **major versions (v2)** with renamed APIs: Python `FastMCP` became `MCPServer`, and the TypeScript package `@modelcontextprotocol/sdk` became `@modelcontextprotocol/server`/`client` [20][29]. Most blog posts, courses and LLM-generated code still show the 2025 handshake and the v1 APIs. **Treat any tutorial dated before July 2026 as legacy.**

---

## 1. What MCP is, and the architecture

### 1.1 One-paragraph definition
The Model Context Protocol (MCP) is an open, JSON-RPC 2.0-based protocol. It lets AI applications ("hosts") connect to external capability providers ("servers") in a standard way. A server exposes **tools** (actions the model can call), **resources** (data the application can load as context) and **prompts** (user-invoked templates) [4][6]. Anthropic created MCP in November 2024 and donated it to the **Agentic AI Foundation (AAIF)**, a directed fund under the Linux Foundation, on 9 Dec 2025 [15]. The spec is now maintained under that open governance. Tier-1 SDKs exist for TypeScript, Python, C#, Go, Rust and Ruby. Java is Tier 2. Swift, PHP and Kotlin are Tier 3 [17].

### 1.2 Roles: host, client, server [4]
| Role | What it is | Responsibilities |
|---|---|---|
| **Host** | The AI application (Claude Desktop/Code, VS Code + Copilot, ChatGPT, Cursor, your own agent) | Creates clients, enforces security policy and consent, runs the LLM, aggregates context |
| **Client** | A connector inside the host, **1:1 with one server** | Attaches protocol version and capabilities to every request, routes messages, manages subscriptions |
| **Server** | Your program | Exposes tools/resources/prompts. Can be a local process (stdio) or a remote service (HTTP) |

Design principle worth quoting on a slide: servers "should not be able to read the whole conversation, nor 'see into' other servers". The host holds the conversation and enforces the boundaries between servers [4].

### 1.3 Wire format: JSON-RPC 2.0
Every message is a JSON-RPC 2.0 request, response or notification. The 2026-07-28 schema defines these methods [7]:
- **Client to server requests:** `server/discover`, `tools/list`, `tools/call`, `resources/list`, `resources/read`, `resources/templates/list`, `prompts/list`, `prompts/get`, `completion/complete`, `subscriptions/listen`.
- **Requests a server embeds in an `input_required` result** (see 1.5): `elicitation/create`, `sampling/createMessage`, `roots/list`.
- **Notifications:** `notifications/progress`, `notifications/cancelled`, `notifications/message` (deprecated), `notifications/tools|prompts|resources/list_changed`, `notifications/resources/updated`, `notifications/subscriptions/acknowledged`.

Every result now carries `resultType`: `"complete"` or `"input_required"` [3].

### 1.4 Lifecycle: then and now (the most important update for this course)
**Legacy (2024-11-05 through 2025-11-25):** `initialize` request (version + capabilities), then the `initialize` response, then the client's `notifications/initialized`, then operation, then shutdown (close stdin, or HTTP DELETE of the session). On HTTP the server minted an `Mcp-Session-Id` [3][10].

**Current (2026-07-28): stateless, with no handshake** [1][3][5]:
- **Every request is self-describing.** `params._meta` carries `io.modelcontextprotocol/protocolVersion` and `io.modelcontextprotocol/clientCapabilities`. It SHOULD also carry `io.modelcontextprotocol/clientInfo`. Servers SHOULD return `io.modelcontextprotocol/serverInfo` in each result's `_meta` [3].
- **`server/discover`**: servers **MUST** implement it. It returns `supportedVersions`, `capabilities`, `serverInfo` and optional `instructions`. Clients **MAY** call it first, and it is the recommended back-compat probe on stdio [5][9].
- **Version mismatch** returns `UnsupportedProtocolVersionError` (code `-32022`) listing supported versions. The client retries with one of them [1][3].
- **No protocol sessions.** `Mcp-Session-Id` was removed. `tools/list` etc. "MUST NOT vary per-connection" but MAY vary by the caller's authorization [6]. Servers that need state mint **explicit handles** (e.g., `basket_id`) and the model passes them back as ordinary tool arguments [3][6].
- **Shutdown**: on stdio, the client closes stdin, waits, then escalates SIGTERM to SIGKILL. On HTTP each request stands alone, so there is no session to tear down [9][10].
- `ping` and `logging/setLevel` were removed. The log level is now set per request via `_meta` [3].

Example 2026-07-28 request (from the spec) [10]:
```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: get_weather

{"jsonrpc":"2.0","id":1,"method":"tools/call",
 "params":{"name":"get_weather","arguments":{"location":"Seattle, WA"},
  "_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28",
           "io.modelcontextprotocol/clientInfo":{"name":"ExampleClient","version":"1.0.0"},
           "io.modelcontextprotocol/clientCapabilities":{}}}}
```

### 1.5 What changed recently: timeline
| Revision | Date | Key changes |
|---|---|---|
| 2025-03-26 | Mar 2025 | Streamable HTTP replaces HTTP+SSE. OAuth-based auth introduced [10] |
| 2025-06-18 | Jun 2025 | Structured tool output, elicitation, resource links, `MCP-Protocol-Version` header, auth reworked around RFC 9728 [10][11] |
| 2025-11-25 | 25 Nov 2025 | OIDC discovery, icons, incremental scope consent, tool-name guidance, URL-mode elicitation, sampling with tools, **CIMD**, experimental **tasks**, JSON Schema 2020-12 default [14] |
| **2026-07-28 (current)** | 28 Jul 2026 | Stateless core, no `initialize`, no sessions, `server/discover`, **MRTR** (multi-round-trip requests) replaces server-initiated requests, `subscriptions/listen`, required `Mcp-Method`/`Mcp-Name` headers, cacheable lists (`ttlMs`, `cacheScope`), tasks moved to an extension, RFC 9207 `iss` validation. **Deprecated:** Roots, Sampling, Logging, HTTP+SSE, Dynamic Client Registration [2][3] |

Deprecated features keep working for **at least 12 months** under the new feature-lifecycle policy, so July 2027 is the earliest removal date [1][2][16].

**MRTR in one sentence:** the server never sends its own request to the client. Instead it *returns* `resultType: "input_required"` with `inputRequests` (e.g., an elicitation form), plus an optional opaque `requestState`. The client gathers the answers and **retries the original call with a new JSON-RPC id**, adding `inputResponses` [8]. Because of this, any server instance behind a plain round-robin load balancer can answer any request [2].

---

## 2. Server primitives and client features

### 2.1 Who controls what (good slide)
| Primitive | Controlled by | Typical UI | Example |
|---|---|---|---|
| **Tool** | Model (the LLM decides to call it) | Tool picker, approval prompt | `get_ticket`, `close_ticket` |
| **Resource** | Application/host | "@-mention" or attach-file picker | `tickets://TCK-1001` |
| **Prompt** | User | Slash command / menu | `/triage_ticket` |
[6][22][33]

### 2.2 Tools [6][7]
- **Fields:** `name`, optional `title`, `description`, `icons`, `inputSchema` (JSON Schema, 2020-12 by default; MUST be a valid object, not `null`), optional `outputSchema`, optional `annotations`.
- **Names:** SHOULD be 1-128 characters and case-sensitive, using only `A-Z a-z 0-9 _ - .`. Aggregating hosts SHOULD disambiguate collisions (e.g., by prefixing the server name) [6].
- **Results:** `content[]` holds `text`, `image`, `audio`, `resource_link` or embedded `resource` blocks. `structuredContent` can be any JSON value and MUST conform to `outputSchema` if one is declared. For back-compatibility, a tool returning structured content SHOULD also return the serialized JSON as text [6].
- **Two kinds of error** [6]:
  - *Protocol errors* (JSON-RPC `error`, e.g., `-32602` unknown tool).
  - *Tool execution errors* (`isError: true` in the result). Use these for bad input and API failures, so **the model can read them and self-correct**. Input-validation failures belong here, not in protocol errors (clarified in 2025-11-25 [14]).
- **Annotations** (`ToolAnnotations`, verbatim defaults from the schema [7]):

| Hint | Meaning | Default |
|---|---|---|
| `readOnlyHint` | Does not modify its environment | `false` |
| `destructiveHint` | May perform destructive updates (only meaningful if not read-only) | `true` |
| `idempotentHint` | Repeat calls have no additional effect (only meaningful if not read-only) | `false` |
| `openWorldHint` | Interacts with an open world of external entities | `true` |

  **Annotations are hints, not security.** The spec says clients "MUST consider tool annotations to be untrusted unless they come from trusted servers" [6]. Hosts use them anyway. For example, ChatGPT Developer Mode treats every tool as a write action that needs confirmation *unless* it carries `readOnlyHint` [46].
- **Human in the loop:** "there SHOULD always be a human in the loop with the ability to deny tool invocations" [6].
- **Server MUSTs:** "Validate all tool inputs; Implement proper access controls; Rate limit tool invocations; Sanitize tool outputs" [6].
- **New in 2026-07-28:** `x-mcp-header` lets a tool parameter be mirrored into an `Mcp-Param-{Name}` HTTP header so gateways and WAFs can route on it. Never use it for secrets or PII, because headers are visible to intermediaries [6][10].

### 2.3 Resources [22][32][7]
- These are read-only data addressed by URI, e.g., `config://app` or `file:///...`.
- **Resource templates** use RFC 6570 URI templates (`users://{user_id}/profile`) and are listed via `resources/templates/list`. The Python SDK applies path-traversal, absolute-path and null-byte checks to extracted values by default [22].
- **Subscriptions:** in 2026-07-28, `resources/subscribe` was replaced by **`subscriptions/listen`**. This is one long-lived POST whose SSE response carries only the notification types the client opted into: `toolsListChanged`, `promptsListChanged`, `resourcesListChanged`, `resourceSubscriptions` [3][10].
- Annotations on content (`audience`, `priority` from 0 to 1, `lastModified`) tell the host how to use the content [7].
- The "resource not found" error code changed from `-32002` to `-32602` [3].

### 2.4 Prompts [33][7]
Prompts are named templates with arguments that return `messages[]`. Users pick them (often as slash commands). Prompt argument validation failures are **protocol errors** (`-32602`), unlike tool argument failures [33].

### 2.5 Client features (and their 2026 status)
| Feature | What it does | Status in 2026-07-28 |
|---|---|---|
| **Elicitation** | Server asks the *user* for structured input (form mode) or sends them to a URL (URL mode, e.g., OAuth or payment) | **Active.** Delivered via MRTR `input_required` [8][3] |
| **Sampling** | Server asks the host's LLM for a completion | **Deprecated** (SEP-2577). Call an LLM API directly instead [3] |
| **Roots** | Client tells server which directories it may use | **Deprecated.** Pass paths as tool args or config instead [3] |

### 2.6 Utilities
- **Progress:** the client sends a progress token, and the server emits `notifications/progress` *on that request's response stream* [3][10].
- **Cancellation:** on stdio, the client sends `notifications/cancelled`. On Streamable HTTP, **closing the response stream is the cancellation**. Either way the server SHOULD stop work and MUST NOT send further messages for that request [9][10].
- **Pagination:** list methods take `cursor` and return `nextCursor` [6].
- **Caching (new):** list results MUST carry `ttlMs` and `cacheScope` (`public`/`private`). Servers SHOULD return tools in a deterministic order, which helps prompt-cache hit rates [3][6].
- **Logging:** `notifications/message` is **deprecated**. Log to **stderr** (stdio) or use **OpenTelemetry**. Trace context (`traceparent`, `tracestate`, `baggage`) can ride in `_meta` [3]. The Python SDK v2 enables OpenTelemetry tracing by default [Python v2.0.0 release notes, via 20].
- **Completion:** `completion/complete` offers argument autocompletion for prompts and resource templates [7].
- **Tasks** (long-running work) now live in an **extension**, `io.modelcontextprotocol/tasks`, with poll-based `tasks/get`, plus `tasks/update` and `tasks/cancel` [3][16]. *Flag:* the Python SDK 2.0.0 release notes said the tasks extension was not yet included. Check the release notes for your SDK version.

---

## 3. Transports

### 3.1 stdio [9]
- The host launches the server as a **subprocess** and exchanges newline-delimited JSON-RPC over stdin/stdout. Messages MUST NOT contain embedded newlines.
- **The server MUST NOT write anything to stdout that is not a valid MCP message.** Logs go to stderr. This is the number-one beginner bug: a stray `print()` or `console.log()` corrupts the stream and the host drops the connection [18][30]. The Python v2 SDK now diverts *flushed* stray stdout to stderr while serving, but output before serving starts, or buffered output, can still corrupt the wire [24].
- Credentials come from the **environment**, not OAuth. The auth spec says stdio implementations "SHOULD NOT follow this specification, and instead retrieve credentials from the environment" [11].
- Best for: local tools, developer workstations, and anything that touches local files. Only the parent process can talk to it, which is a security plus [13].

### 3.2 Streamable HTTP (2026-07-28 shape) [10]
- One **MCP endpoint** (e.g., `https://host/mcp`) accepting **POST**. Each JSON-RPC message is its own POST, and the client's `Accept` header must list `application/json` and `text/event-stream`.
- The server answers with a single JSON body or a per-request **SSE** stream (progress notifications, then the final response).
- Required headers: `MCP-Protocol-Version`, `Mcp-Method`, plus `Mcp-Name` on `tools/call`, `resources/read` and `prompts/get`. Headers MUST match the body. On mismatch the server returns `400` and JSON-RPC `-32020 HeaderMismatch` (we reproduced this against the Python SDK).
- **Security MUSTs/SHOULDs:** "Servers MUST validate the `Origin` header… If the Origin header is present and invalid, servers MUST respond with HTTP 403". Local servers "SHOULD bind only to localhost (127.0.0.1)". Servers "SHOULD implement proper authentication for all connections".
- GET stream, DELETE, `Mcp-Session-Id` and `Last-Event-ID` resumability were all **removed**. A modern-only server answers GET/DELETE with `405` and ignores session headers.
- Best for: shared/remote/team servers, SaaS integrations, and anything deployed behind a gateway. Because it is stateless, it scales horizontally.

### 3.3 HTTP+SSE (2024-11-05): deprecated
Deprecated since 2025-03-26, and now formally "Deprecated" under the lifecycle policy. "New implementations SHOULD NOT adopt it" [10][3]. Claude Code still accepts `--transport sse` but labels it deprecated [42]. The OpenAI Agents SDK labels `MCPServerSse` deprecated [45].

### 3.4 Sessions and state
There are no protocol sessions in 2026-07-28. To keep state, return a server-minted handle and require it as an argument. The handle must be **unguessable** (secure random), have **bounded lifetime**, and be **bound server-side to the authenticated user** (e.g., store state as `<user_id>:<handle>`). "MCP servers MUST NOT treat possession of a state handle as authentication" [6][13].

### 3.5 Which transport?
| Situation | Use |
|---|---|
| Personal/dev tool, local files, single user | **stdio** |
| Team/shared service, central auth, audit, many clients | **Streamable HTTP** + OAuth, behind a gateway |
| Air-gapped or classified enclave | Either, but host the *server* inside the enclave. Remote HTTP needs an internal IdP/authorization server. The public registry and connector directories won't apply (see 7.6) |
| Legacy client that only speaks SSE | Fix the client. Add an SSE endpoint only as a time-boxed bridge |

---

## 4. Authorization for remote (HTTP) servers

**Scope:** auth is OPTIONAL, but HTTP implementations that do it SHOULD follow this spec. Stdio uses environment credentials [11].

### 4.1 Roles and standards [11]
- **MCP server = OAuth 2.1 resource server.** **MCP client = OAuth 2.1 client.** The **authorization server (AS)** can be co-hosted with the MCP server or separate, e.g., your enterprise IdP (Entra ID, Okta, Keycloak, Ping).
- Standards used: OAuth 2.1 (draft-13), RFC 6750 (bearer tokens), RFC 8414 (AS metadata), **RFC 9728 (Protected Resource Metadata)**, **RFC 8707 (Resource Indicators)**, **RFC 9207 (issuer identification)**, Client ID Metadata Documents (CIMD), OIDC Discovery, and RFC 7591 DCR (deprecated).

### 4.2 The flow, step by step [11][12]
1. The client calls the MCP endpoint without a token. The server replies **`401`** with `WWW-Authenticate: Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource", scope="tickets:read"`.
2. The client fetches the **Protected Resource Metadata** (PRM, RFC 9728). Servers **MUST** implement PRM, and it **MUST** list at least one entry in `authorization_servers`. If the header is missing, clients fall back to `/.well-known/oauth-protected-resource/<mcp-path>` and then the root path [12].
3. The client discovers **AS metadata** by trying the RFC 8414 well-known path, then OIDC discovery, in a defined priority order. It **MUST** reject metadata whose `issuer` doesn't exactly match [12].
4. **Client registration**, in priority order [11]:
   - (a) **CIMD**: the client_id is an HTTPS URL to a metadata document. SHOULD be supported.
   - (b) **Pre-registration**: best fit for most government IdPs.
   - (c) **DCR**: deprecated, kept for back-compat.

   Credentials are bound to the issuing AS and MUST NOT be reused with a different AS [3].
5. **Authorization code + PKCE** with the **`resource`** parameter (RFC 8707) set to the MCP server's canonical URI, e.g. `resource=https%3A%2F%2Fmcp.example.com`, sent in both the authorization and token requests. Clients "MUST send this parameter regardless of whether authorization servers support it" [11].
6. **Issuer check (new, RFC 9207):** before redeeming the code, the client MUST validate the `iss` in the authorization response against the issuer it recorded. This blocks AS "mix-up" attacks [11][13].
7. The client calls MCP with `Authorization: Bearer <token>` on **every** HTTP request. Tokens are never placed in the query string [11].
8. **Step-up:** if a token lacks scope, the server returns **`403`** with `error="insufficient_scope"` and the full set of scopes the operation needs in one challenge. The client re-authorizes with the union of its old and new scopes [11].

### 4.3 What the *server* must do with tokens [11]
- "MCP servers MUST validate that access tokens were issued specifically for them as the intended audience" (RFC 8707 audience binding).
- Invalid or expired tokens get **401**. Insufficient scope gets **403**.
- "MCP servers MUST only accept tokens that are valid for use with their own resources." "MCP servers **MUST NOT accept or transit any other tokens**."
- Start with a minimal `scopes_supported`, escalate via targeted challenges, and avoid omnibus scopes like `*` or `full-access` [13].

### 4.4 Why token passthrough is forbidden [13]
"Token passthrough" means accepting a token the client got for some *other* API and forwarding it downstream unchanged. It is explicitly forbidden because:
- **It bypasses security controls.** Rate limits, validation and monitoring keyed to the audience are skipped.
- **It breaks audit and accountability.** The MCP server can't tell clients apart, and downstream logs show the wrong identity.
- **It breaks the trust boundary.** One stolen token works against every service that accepts it, and the MCP server becomes an exfiltration proxy.
- **It creates future-compatibility risk.** A "pure proxy" can't add controls later.

The correct pattern is for the MCP server to validate its *own* token. To call a downstream API, it then uses **its own** credentials or a token obtained for that API (e.g., via OAuth token exchange / on-behalf-of in your IdP). It never re-sends the inbound token.

### 4.5 Confused deputy (MCP proxy servers) [13]
**The attack conditions:** an MCP server that fronts a third-party API with a **static client ID**, allows dynamic client registration, and relies on the third-party AS's **consent cookie**. An attacker can then obtain an authorization code without the user's consent.

**The fix:** the proxy **MUST** implement **per-client consent** before forwarding to the third party. That means:
- a registry of approved `client_id`s per user;
- a consent page that shows the client name, scopes and `redirect_uri`, with CSRF protection and anti-framing;
- exact `redirect_uri` matching;
- a single-use, short-lived `state` that is set only *after* consent.

### 4.6 SDK support
- Python v2: `MCPServer(token_verifier=..., auth=AuthSettings(...))`. Use `get_access_token()` in handlers [20]. It adds RFC 9207 issuer validation [Python v2.0.0 release notes].
- TypeScript v2: `requireBearerAuth({ verifier })` middleware in front of `createMcpHandler`. Handlers read `ctx.http.authInfo`. Runnable examples exist: `bearer-auth`, `oauth`, `oauth-client-credentials`, `scoped-tools` [35][36].
- **Enterprise-Managed Authorization (EMA)** is an official extension that lets IT provision server access through the corporate IdP. It is relevant to regulated orgs, but adoption across hosts varies, so verify per host [2][16].

---

## 5. Step-by-step build walkthrough

**Scenario used throughout:** "ticket-desk", a help-desk server with:
- one **read-only tool** (`get_ticket`);
- one **action tool that requires human confirmation** (`close_ticket`);
- one **resource template** (`tickets://{id}`);
- one **prompt** (`triage_ticket`).

Swap the in-memory dict for your real system (ServiceNow, Jira, Remedy) in the lab extension.

### 5.1 Current package names and versions (verified 20 Oct 2026)
| Language | Install | Current version | Notes |
|---|---|---|---|
| Python | `uv add "mcp[cli]"` or `pip install "mcp[cli]"` | **mcp 2.3.0** (2 Oct 2026); 2.0.0 released 28 Jul 2026 | Requires Python ≥ 3.10. v1.x (latest 1.30.0) gets security fixes only. Pin `mcp>=1.28,<2` if you're not ready to migrate [19][28] |
| TypeScript | `npm install @modelcontextprotocol/server zod` | **@modelcontextprotocol/server 2.3.1** (5 Oct 2026) | ESM only, Node ≥ 20, Zod v4 (`import * as z from 'zod/v4'`). Optional adapters: `@modelcontextprotocol/express` 2.0.2, `@modelcontextprotocol/node` 2.1.1, plus `fastify` and `hono`. v1 `@modelcontextprotocol/sdk` (1.32.1) gets fixes for ≥ 6 months after 27 Jul 2026 [29][30][40] |
| Inspector | `npx @modelcontextprotocol/inspector` | **2.11.0** (14 Oct 2026) | Requires **Node ≥ 22.19.0** [41] |

**Gotchas from the v1 to v2 renames (expect learners to hit these):**
- **Python:** `from mcp.server.fastmcp import FastMCP` now raises `ModuleNotFoundError`. Use `from mcp.server import MCPServer`.
- **Python:** transport options (`host`, `port`, `json_response`, `stateless_http`) moved from the constructor to `run()`.
- **Python:** fields are snake_case (`structured_content`, `is_error`, `read_only_hint`) [20][24].
- **TypeScript:** `server.tool()` was replaced by `registerTool()`.
- **TypeScript:** `server.connect(new StdioServerTransport())` "still compiles, but a server started that way only serves 2025-era clients". Use `serveStdio(factory)` [18].
- **TypeScript:** `StreamableHTTPServerTransport` + `connect()` was replaced by `createMcpHandler(factory)` [35].
- **Both:** v2 servers answer **both** 2026-07-28 clients and 2025-era `initialize` clients from the same code [18][24].

> *Flag:* the official Python quickstart imports `httpx2` ("the HTTP client the SDK itself depends on") [18]. The examples below avoid outbound HTTP, so they don't depend on it.

### 5.2 Python: project setup
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh     # install uv (Windows: see [18])
uv init ticket-desk && cd ticket-desk
uv add "mcp[cli]"                                   # SDK 2.x + `mcp` CLI
uv add --dev pytest inline-snapshot                 # optional, for tests
```

### 5.3 Python: `server.py` (tested)
```python
"""ticket-desk: a minimal MCP server (Python SDK 2.x)."""
import json
import logging
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from mcp.server import MCPServer
from mcp.server.mcpserver import AcceptedElicitation, Elicit, ElicitationResult, Resolve
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

log = logging.getLogger("ticket-desk")  # logging writes to stderr, never stdout

mcp = MCPServer(
    "ticket-desk",
    version="1.0.0",
    instructions="Help-desk tickets. Look tickets up before acting on them.",
)

# Stand-in for a real ticketing API
TICKETS: dict[str, dict] = {
    "TCK-1001": {"id": "TCK-1001", "title": "VPN drops every 30 min", "status": "open", "priority": "high"},
    "TCK-1002": {"id": "TCK-1002", "title": "Printer on 3rd floor offline", "status": "open", "priority": "low"},
}

TicketId = Annotated[str, Field(pattern=r"^TCK-\d{4}$", description="Ticket ID, e.g. TCK-1001")]


class Ticket(BaseModel):
    id: str
    title: str
    status: Literal["open", "closed"]
    priority: Literal["low", "medium", "high"]


# 1) Read-only tool -> structured output (outputSchema is generated from the return type)
@mcp.tool(
    title="Look up a ticket",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def get_ticket(ticket_id: TicketId) -> Ticket:
    """Return one help-desk ticket by ID. Read-only."""
    log.info("get_ticket %s", ticket_id)
    if ticket_id not in TICKETS:
        raise ToolError(f"No ticket {ticket_id}. Check the ID and try again.")
    return Ticket(**TICKETS[ticket_id])


# 2) Action tool that requires human confirmation (elicitation via a resolver)
class Confirm(BaseModel):
    confirm: bool = Field(description="Yes, close this ticket")


async def confirm_close(ticket_id: str) -> Elicit[Confirm]:
    """Resolver: always ask the human before closing."""
    return Elicit(f"Close ticket {ticket_id}? This notifies the requester.", Confirm)


@mcp.tool(
    title="Close a ticket",
    annotations=ToolAnnotations(
        read_only_hint=False, destructive_hint=False, idempotent_hint=True, open_world_hint=False
    ),
)
async def close_ticket(
    ticket_id: TicketId,
    resolution: Annotated[str, Field(min_length=5, max_length=500)],
    confirm: Annotated[ElicitationResult[Confirm], Resolve(confirm_close)],
) -> str:
    """Close a ticket with a resolution note. Asks the user to confirm first."""
    if ticket_id not in TICKETS:
        raise ToolError(f"No ticket {ticket_id}.")
    match confirm:
        case AcceptedElicitation(data=Confirm(confirm=True)):
            TICKETS[ticket_id]["status"] = "closed"
            log.info("AUDIT close_ticket %s resolution=%r", ticket_id, resolution)
            return f"{ticket_id} closed."
        case _:
            return f"{ticket_id} NOT closed: the user did not confirm."


# 3) Resource template: application-controlled context
@mcp.resource("tickets://{ticket_id}", mime_type="application/json")
def ticket_resource(ticket_id: str) -> str:
    """A ticket as JSON, for attaching as context."""
    return json.dumps(TICKETS.get(ticket_id, {}))


# 4) Prompt: user-invoked template (slash command in most hosts)
@mcp.prompt(title="Triage a ticket")
def triage_ticket(ticket_id: str) -> str:
    """Draft a triage plan for one ticket."""
    return (
        f"Use get_ticket to read {ticket_id}. Propose priority, owner team and next step. "
        "Do not close the ticket."
    )


if __name__ == "__main__":
    mcp.run()  # stdio by default
```

**Teaching points (all verified when we ran the code):**
- **Type hints *are* the schema.** The `pattern` lands in `inputSchema`. A call with `"1001; DROP TABLE"` is rejected *before* your function runs, and comes back as an `is_error` result the model can read. The `-> Ticket` return type generates an `outputSchema`, and the result carries both `content` (JSON text) and `structured_content` [21].
- **`Resolve(confirm_close)` hides `confirm` from the model.** The parameter does *not* appear in `inputSchema`, so the model cannot pre-fill "confirm: true". The SDK asks the human. On a 2026-07-28 connection it **returns** an `input_required` result and the client retries. On a legacy connection it pushes `elicitation/create`. You write the code once [23]. We tested decline and accept in both eras.
- **Use `ctx.elicit()` only for legacy clients.** It "fail[s]" on 2026-07-28 connections because there are no server-initiated requests. Prefer resolvers [23].
- **Pick the right error.** `ToolError` yields a model-readable tool error. `MCPError(code=..., message=...)` yields a protocol error. Any other exception is sanitized to a generic message for remote callers [27].

### 5.4 Python: run over stdio, test, inspect
```bash
uv run server.py                       # waits silently on stdin (correct!)
uv run mcp dev server.py               # opens MCP Inspector against it (needs npx)
uv run mcp install server.py --name "Ticket Desk"   # registers with Claude Desktop
```
Unit test with the in-memory client (no subprocess, no port) [25]:
```python
# test_server.py
import pytest
from mcp import Client
from mcp.types import ElicitResult
from server import mcp, TICKETS

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_get_ticket():
    async with Client(mcp, raise_exceptions=True) as c:
        r = await c.call_tool("get_ticket", {"ticket_id": "TCK-1001"})
        assert r.structured_content["status"] == "open"
        bad = await c.call_tool("get_ticket", {"ticket_id": "TCK-9999"})
        assert bad.is_error

@pytest.mark.anyio
async def test_close_requires_confirmation():
    async def decline(context, params):          # stands in for the host's UI
        return ElicitResult(action="decline")
    async with Client(mcp, elicitation_callback=decline) as c:
        await c.call_tool("close_ticket", {"ticket_id": "TCK-1002", "resolution": "Replaced toner"})
    assert TICKETS["TCK-1002"]["status"] == "open"
```
Run it with `uv run pytest -q`.

### 5.5 Python: Streamable HTTP
For a quick local run:
```python
mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)   # -> http://127.0.0.1:8000/mcp
# or: uv run mcp run server.py --transport streamable-http
```
For deployment behind a real hostname, build the ASGI app and **allowlist hosts**. Without an allowlist, the localhost-only DNS-rebinding guard answers every request with **421 Misdirected Request** [26]. We verified this: the allowed host got 200, and `Host: evil.example` got 421.
```python
# app.py  ->  uvicorn app:app --host 0.0.0.0 --port 8000
import os
from mcp.server.transport_security import TransportSecuritySettings
from server import mcp

hosts = os.environ.get("MCP_ALLOWED_HOSTS", "localhost:*,127.0.0.1:*").split(",")
app = mcp.streamable_http_app(
    transport_security=TransportSecuritySettings(allowed_hosts=hosts, allowed_origins=[]),
)
```
Other `run()`/app options:
- `json_response=True`: a single JSON body, with no mid-call progress.
- `max_request_body_size`: 4 MiB by default.
- `stateless_http`: now a legacy-only knob, because "On 2026-07-28 there is no session" [24][26].
- Behind a TLS-terminating proxy, run uvicorn with `--proxy-headers --forwarded-allow-ips=...` [26].

### 5.6 TypeScript: project setup
```bash
mkdir ticket-desk && cd ticket-desk
npm init -y && npm pkg set type=module             # SDK is ESM-only
npm install @modelcontextprotocol/server zod
npm install -D tsx typescript @types/node
# for HTTP:  npm install @modelcontextprotocol/express @modelcontextprotocol/node express && npm i -D @types/express
```
The TS tutorials run `.ts` directly with `tsx`. The official quickstart instead compiles with `tsc` (`"module": "Node16"`) and runs `node build/index.js` [18][30].

### 5.7 TypeScript: `src/server.ts` (tested)
```ts
// ticket-desk: a minimal MCP server (TypeScript SDK v2)
import { acceptedContent, inputRequired, inputResponse, McpServer, ResourceTemplate } from '@modelcontextprotocol/server';
import type { CallToolResult, InputRequiredResult } from '@modelcontextprotocol/server';
import * as z from 'zod/v4';

const TICKETS: Record<string, { id: string; title: string; status: 'open' | 'closed'; priority: string }> = {
    'TCK-1001': { id: 'TCK-1001', title: 'VPN drops every 30 min', status: 'open', priority: 'high' },
    'TCK-1002': { id: 'TCK-1002', title: 'Printer on 3rd floor offline', status: 'open', priority: 'low' }
};

const TicketId = z.string().regex(/^TCK-\d{4}$/).describe('Ticket ID, e.g. TCK-1001');
const Confirm = z.object({ confirm: z.boolean().meta({ title: 'Yes, close this ticket' }) });

// Factory: the SDK calls this whenever it needs a fresh server instance
export function createServer(): McpServer {
    const server = new McpServer({ name: 'ticket-desk', version: '1.0.0' });

    // 1) Read-only tool with structured output
    server.registerTool(
        'get_ticket',
        {
            title: 'Look up a ticket',
            description: 'Return one help-desk ticket by ID. Read-only.',
            inputSchema: z.object({ ticket_id: TicketId }),
            outputSchema: z.object({ id: z.string(), title: z.string(), status: z.enum(['open', 'closed']), priority: z.string() }),
            annotations: { readOnlyHint: true, openWorldHint: false }
        },
        async ({ ticket_id }) => {
            console.error(`get_ticket ${ticket_id}`); // stderr only
            const t = TICKETS[ticket_id];
            if (!t) return { content: [{ type: 'text', text: `No ticket ${ticket_id}.` }], isError: true };
            return { content: [{ type: 'text', text: JSON.stringify(t) }], structuredContent: t };
        }
    );

    // 2) Action tool that requires human confirmation (MRTR input_required)
    server.registerTool(
        'close_ticket',
        {
            title: 'Close a ticket',
            description: 'Close a ticket with a resolution note. Asks the user to confirm first.',
            inputSchema: z.object({ ticket_id: TicketId, resolution: z.string().min(5).max(500) }),
            annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
        },
        async ({ ticket_id, resolution }, ctx): Promise<CallToolResult | InputRequiredResult> => {
            if (!TICKETS[ticket_id]) return { content: [{ type: 'text', text: `No ticket ${ticket_id}.` }], isError: true };
            // A decline/cancel must end the call, or the client is asked again
            const view = inputResponse(ctx.mcpReq.inputResponses, 'confirm');
            if (view.kind === 'elicit' && view.action !== 'accept') {
                return { content: [{ type: 'text', text: `${ticket_id} NOT closed (user chose ${view.action}).` }] };
            }
            const answer = acceptedContent(ctx.mcpReq.inputResponses, 'confirm', Confirm);
            if (answer === undefined) {
                return inputRequired({
                    inputRequests: {
                        confirm: inputRequired.elicit({
                            message: `Close ticket ${ticket_id}? This notifies the requester.`,
                            requestedSchema: Confirm
                        })
                    }
                });
            }
            if (!answer.confirm) return { content: [{ type: 'text', text: `${ticket_id} NOT closed: user did not confirm.` }] };
            TICKETS[ticket_id].status = 'closed';
            console.error(`AUDIT close_ticket ${ticket_id} resolution=${JSON.stringify(resolution)}`);
            return { content: [{ type: 'text', text: `${ticket_id} closed.` }] };
        }
    );

    // 3) Resource template
    server.registerResource(
        'ticket',
        new ResourceTemplate('tickets://{ticketId}', { list: undefined }),
        { title: 'Ticket JSON', description: 'A ticket as JSON', mimeType: 'application/json' },
        async (uri, { ticketId }) => ({
            contents: [{ uri: uri.href, mimeType: 'application/json', text: JSON.stringify(TICKETS[String(ticketId)] ?? {}) }]
        })
    );

    // 4) Prompt
    server.registerPrompt(
        'triage_ticket',
        { title: 'Triage a ticket', description: 'Draft a triage plan for one ticket', argsSchema: z.object({ ticket_id: z.string() }) },
        ({ ticket_id }) => ({
            messages: [{ role: 'user' as const, content: { type: 'text' as const, text: `Use get_ticket to read ${ticket_id}. Propose priority, owner and next step. Do not close it.` } }]
        })
    );

    return server;
}
```

**Real bug we hit (good teaching moment):** the first version only checked `acceptedContent(...) === undefined`. That function returns `undefined` for *missing, declined and cancelled* alike [34]. So when the user said **No**, the server asked again, and again, until the client gave up with `INPUT_REQUIRED_ROUNDS_EXCEEDED` after 10 rounds. The `inputResponse(...)` check above fixes it: **always handle decline/cancel explicitly.** The SDK's "legacy shim" (on by default) turns `inputRequired(...)` into a real pushed `elicitation/create` for 2025-era clients [34].

### 5.8 TypeScript: stdio entry point
```ts
// src/stdio.ts
import { serveStdio } from '@modelcontextprotocol/server/stdio';
import { createServer } from './server.js';

void serveStdio(createServer);
console.error('ticket-desk MCP server running on stdio');   // stderr, never console.log
```
Run with `npx tsx src/stdio.ts`. Check the modern era with:
`npx @modelcontextprotocol/inspector --cli npx tsx src/stdio.ts --protocol-era modern --method tools/list` [18].

### 5.9 TypeScript: Streamable HTTP entry point (Express)
```ts
// src/http.ts
import { createMcpExpressApp } from '@modelcontextprotocol/express';
import { toNodeHandler } from '@modelcontextprotocol/node';
import { createMcpHandler } from '@modelcontextprotocol/server';
import { createServer } from './server.js';

const handler = createMcpHandler(createServer); // fresh McpServer per request; stateless
const app = createMcpExpressApp();              // express.json() + Host/Origin checks on localhost
const node = toNodeHandler(handler);
app.all('/mcp', (req, res) => void node(req, res, req.body));
app.listen(3000, '127.0.0.1', () => console.error('ticket-desk on http://127.0.0.1:3000/mcp'));
```
- **Public bind:** use `createMcpExpressApp({ host: '0.0.0.0', allowedHosts: ['mcp.example.gov'] })`. Binding to all interfaces "drops that default" Host protection unless you name hosts [36].
- **Auth:** put `requireBearerAuth({ verifier })` in front of the route: `app.all('/mcp', auth, ...)` [36].
- **Response shape:** `createMcpHandler(factory, { responseMode: 'json' })` forces single-JSON responses [35].
- **Handler trust:** the handler itself "validates no Host header, no Origin header, and no token". Put the checks in front of it [35].
- **Why it matters:** in v1, DNS-rebinding protection was *not on by default* (CVE-2025-66414, fixed in `@modelcontextprotocol/sdk` 1.24.0) [58].

### 5.10 Quick wire-level smoke test (curl, 2026-07-28)
```bash
curl -s -X POST http://127.0.0.1:8000/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' -H 'Mcp-Method: server/discover' \
  -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{
        "io.modelcontextprotocol/protocolVersion":"2026-07-28",
        "io.modelcontextprotocol/clientCapabilities":{}}}}'
```
Observed against our Python server: `supportedVersions: ["2026-07-28"]`, the tools/prompts/resources capabilities, and `serverInfo` in `_meta`. Dropping the `Mcp-Method` header returned `-32020` "mcp-method header does not match the request body's method".

---

## 6. Testing and debugging

### 6.1 MCP Inspector (v2.x) [41]
One package with three front ends. It requires **Node ≥ 22.19.0**.
```bash
npx @modelcontextprotocol/inspector node build/index.js            # Web UI (default)
npx @modelcontextprotocol/inspector uv run server.py                 # Python stdio server
npx @modelcontextprotocol/inspector --cli node build/index.js --method tools/list
npx @modelcontextprotocol/inspector --cli https://host/mcp --transport http \
    --method tools/call --tool-name get_ticket --tool-arg ticket_id=TCK-1001 --format json
npx @modelcontextprotocol/inspector --tui node build/index.js        # terminal UI
```
- `--protocol-era modern|legacy` forces the 2026-07-28 or `initialize` behavior. Test both if you support older hosts [18][41].
- The web UI prints a URL with a **per-launch API token**. This was added after **CVE-2025-49596** (CVSS 9.4): Inspector versions below 0.14.1 had no auth between UI and proxy, so a malicious web page could reach it via 0.0.0.0/DNS rebinding and run commands [55].
- The Inspector stores OAuth tokens and stdio `env` secrets in the OS keychain. Without one, it writes `~/.mcp-inspector/secrets.json`, **unencrypted unless you supply a key** [41]. **Warn learners using shared or headless lab VMs.**
- The CLI mode is ideal for **CI**: assert on `tools/list` output so unexpected tool-definition changes fail the build (see 9.3).

### 6.2 Unit and integration tests
- **Python:** `Client(mcp, raise_exceptions=True)` gives an in-memory, era-neutral connection. Pin `mode="legacy"` to test 2025 behavior [25].
- **TypeScript:** drive `createMcpHandler(...).fetch` in-process via `StreamableHTTPClientTransport(url, { fetch: ... })` with `versionNegotiation: { mode: 'auto' }`. There is no port and no mock [37].
- **What to test:** schema rejection of bad inputs, `isError` paths, the decline/cancel paths of every confirmation, authorization (wrong audience gets 401, missing scope gets 403), and a **snapshot of `tools/list`**.

### 6.3 Logging
- **stdio:** stdout is the wire. Use `logging` (Python, which goes to stderr) or `console.error` (TS) [9][18].
- **HTTP:** stdout logging is fine [18].
- **Protocol logging** (`notifications/message`, `ctx.info()`) is deprecated in 2026-07-28. Use stderr or OpenTelemetry [3][20].
- **Audit log:** record who (token subject), which tool, the arguments (redacted), the result status and the latency, for every `tools/call`. The spec tells clients to "log tool usage for audit purposes" [6]. Do the same on the server.

### 6.4 Common errors and fixes
| Symptom | Likely cause | Fix |
|---|---|---|
| Host shows server "failed"/disconnected immediately | Something printed to **stdout** | Log to stderr. Remove `print`/`console.log` [18] |
| Host can't find the command | Relative paths / `uv` or `node` not on the host's PATH | Use **absolute paths** in config. Use the full path to `uv` [18] |
| Server works in the terminal, not in Claude Desktop | Env vars from your shell aren't inherited | Put them in the config `env` block or `mcp install -v KEY=...` [24] |
| `ModuleNotFoundError: mcp.server.fastmcp` | v1 code on the v2 SDK | `from mcp.server import MCPServer`, or pin `mcp<2` [20] |
| TS server ignores modern clients | Wired with `server.connect(new StdioServerTransport())` | Use `serveStdio(factory)` [18] |
| `421 Misdirected Request` / `403` on deploy | DNS-rebinding guard; real hostname not allowlisted | `transport_security` (Py) / `allowedHosts` (TS) [26][36] |
| `400` + `-32020 HeaderMismatch` | Custom client not sending `Mcp-Method`/`Mcp-Name` | Send the headers, or use an SDK client [10] |
| `400` + `-32022` | Protocol version not supported | Use a version from the `supported` list [1] |
| `ctx.elicit()` / `elicitInput` throws | Server-push elicitation on a 2026-07-28 connection | Use a resolver (Py) / `inputRequired` (TS) [23][34] |
| Infinite confirmation loop / `INPUT_REQUIRED_ROUNDS_EXCEEDED` | Decline/cancel not handled | Check the elicitation action explicitly (5.7) |
| `TypeError: MCPServer.__init__() got an unexpected keyword argument 'port'` | Transport option given to the constructor | Pass it to `run()` [24] |
| Copilot never calls the tool | Chat not in **Agent** mode / stale cache | Switch to Agent. Run "MCP: Reset Cached Tools" [38] |

---

## 7. Connecting to clients

> **Flag (verify per host before class):** v2 SDK servers serve both protocol eras, so connection works either way. We did **not** verify which hosts already speak 2026-07-28 natively and which still use `initialize`.

### 7.1 Claude Desktop (local stdio) [18][24]
Config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`
```json
{
  "mcpServers": {
    "ticket-desk": {
      "command": "/ABSOLUTE/PATH/TO/uv",
      "args": ["--directory", "/ABSOLUTE/PATH/ticket-desk", "run", "server.py"],
      "env": { "TICKET_API_TOKEN": "..." }
    }
  }
}
```
Restart the app afterwards. Python shortcut: `uv run mcp install server.py --name "Ticket Desk"` [24]. For packaged distribution, the registry supports **MCPB** bundles (`.mcpb`) [49].

### 7.2 Claude remote connectors (claude.ai, Desktop, mobile) [43]
- **Free/Pro/Max:** Customize > Connectors > "Add custom connector", then enter the HTTPS MCP URL.
- **Team/Enterprise:** the Owner adds it under Organization settings > Connectors > Add > Custom, and members connect.
- **Auth options:** OAuth via Claude's published **CIMD** identity (recommended), DCR, your own pre-registered client, or (beta) fixed request headers.
- **Admin controls:** admins can set individual tools to **Blocked**.

### 7.3 Claude Code [42]
```bash
claude mcp add ticket-desk -- uv --directory /abs/path/ticket-desk run server.py   # stdio
claude mcp add --transport http ticket-desk https://mcp.example.gov/mcp            # remote
claude mcp add --transport http ticket-desk https://mcp.example.gov/mcp -H "Authorization: Bearer $TOKEN"
claude mcp add --scope project ...   # writes .mcp.json for the team (scopes: local|project|user)
claude mcp list | get <name> | remove <name>;   /mcp  (status + OAuth login)
```
- `.mcp.json` supports `${VAR}` and `${VAR:-default}` expansion. Claude Code prompts before using project-scoped servers.
- Output limits: a warning above 10,000 tokens, and a default cap of 25,000 (`MAX_MCP_OUTPUT_TOKENS`) [42].

### 7.4 VS Code + GitHub Copilot [44][38]
- **VS Code format:** `.vscode/mcp.json` (workspace) or the user profile, under a top-level **`servers`** key.
- **Portable format:** `.mcp.json` at the workspace root, or `~/.copilot/mcp-config.json`, under a top-level **`mcpServers`** key.
```json
{
  "inputs": [{ "type": "promptString", "id": "token", "description": "Ticket API token", "password": true }],
  "servers": {
    "ticket-desk": { "type": "stdio", "command": "uv", "args": ["run", "server.py"],
                     "env": { "TICKET_API_TOKEN": "${input:token}" },
                     "sandboxEnabled": true,
                     "sandbox": { "network": { "allowedDomains": ["tickets.example.gov"] } } },
    "ticket-desk-remote": { "type": "http", "url": "https://mcp.example.gov/mcp" }
  }
}
```
- VS Code can **sandbox stdio servers** (filesystem and network allow-lists) on macOS/Linux [44].
- Organizations can restrict servers via a GitHub enterprise allowlist [44].
- *Flag:* VS Code's guided flow now labels `.vscode/mcp.json` "deprecated" in favor of the portable `.mcp.json`, but the former is still needed for `inputs` and sandboxing [44].

### 7.5 Cursor [38]
`.cursor/mcp.json` in the project, with the same `mcpServers` → `command`/`args` shape as Claude Desktop.

### 7.6 OpenAI: ChatGPT and the Agents SDK
- **ChatGPT Developer Mode** (Pro, Plus, Business, Enterprise, Edu; web): Settings > Apps > Advanced settings > Developer mode, then "Create app" pointing at your **remote** MCP server.
  - Supports SSE and streaming HTTP, with OAuth (static, CIMD or DCR) or no auth.
  - Write actions require confirmation unless `readOnlyHint` is set.
  - It carries an "Elevated risk" badge [46].
- **OpenAI Agents SDK (Python):**
  - `HostedMCPTool` lets the Responses API call a public server.
  - `MCPServerStreamableHttp` and `MCPServerStdio` are the connection classes. `MCPServerSse` is deprecated.
  - Approval control: `require_approval` ("always"/"never"/per-tool/callable).
  - Tool allow/block lists: `create_static_tool_filter`.
  - `cache_tools_list` is available. Warning: caching can mask rug-pulls; see 8.1 [45].

### 7.7 Discovery: the official MCP Registry [47][48][49]
- **What it is:** `registry.modelcontextprotocol.io` stores **metadata only** (`server.json`). It points to npm, PyPI, NuGet, crates.io, OCI images, MCPB bundles, or remote URLs. It is backed by Anthropic, GitHub, PulseMCP and Microsoft. **Status: still "preview"**, so breaking changes and data resets are possible [47].
- **Namespaces** are reverse-DNS (`io.github.user/server`, `gov.agency/server`) and verified by GitHub login, DNS or HTTP challenge [47].
- **No private servers.** Hosts are expected to consume **downstream aggregators/sub-registries** that implement the same OpenAPI spec. *For government:* run a **private registry** that implements the OpenAPI spec as your approved-server catalog. The official codebase "is not designed for self-hosting" [47].
- **Scanning is not the registry's job.** It is delegated to the package registries and aggregators [47].

---

## 8. Security for MCP servers

**Framing:** an MCP server acts with *delegated user authority*, is selected by a *probabilistic* model, and its outputs flow straight back into the model's context. The OWASP GenAI project's guide notes that delegated permissions, dynamic tool architectures and chained tool calls "amplify the impact of a single vulnerability" [51].

### 8.1 Threats, with real incidents
| Threat | What happens | Real-world example (sourced) | Server-side mitigations |
|---|---|---|---|
| **Tool poisoning / description injection** (OWASP MCP03) | Hidden instructions in a tool `description` or schema steer the model; users rarely see the full text | Invariant Labs (Apr 2025): an innocuous `add()` tool's description told the model to read `~/.cursor/mcp.json` / SSH keys and smuggle them out via a hidden parameter [52] | Review descriptions like code; keep them short and factual; CI snapshot of `tools/list`; scan with tools such as MCP-scan [53] |
| **Rug pull** (changed definitions) | A tool approved as safe later changes its definition | Invariant WhatsApp demo: a "fact of the day" server later redefined itself to hijack the legitimate `whatsapp-mcp` `send_message` and exfiltrate chat history [52] | **Pin versions/digests**; hosts should alert on definition changes; treat a `tools/list` diff as a change-control event |
| **Tool shadowing / cross-server** | A malicious server's descriptions influence how the model uses *another* server's tools | Same research [52] | Isolate high-trust servers; per-task server sets; host allow-lists |
| **Prompt injection via results** (MCP06) | Untrusted data returned by a tool (issue text, email, web page) carries instructions | GitHub MCP "toxic agent flow" (Invariant, 26 May 2025): a malicious public issue made the agent copy private-repo data (salary, relocation plans) into a public PR [53] | Least-privilege tokens (one repo, read-only); mark/sanitize untrusted content; require confirmation for writes; avoid combining private data + untrusted input + exfil channel in one session |
| **Confused deputy** | Proxy server lets attacker obtain auth codes without consent | Spec scenario [13] | Per-client consent, exact redirect URIs, single-use `state` [13] |
| **Token passthrough / audience failure** (MCP01/07) | Server accepts or forwards tokens not issued for it | Spec [11][13] | Validate `aud`/resource; never forward inbound tokens |
| **Cross-tenant data leak** | Logic bug returns another org's data | Asana MCP server (May–Jun 2025): bug exposed data across ~1,000 customers' orgs; server taken offline 4–17 Jun [54] | Tenant ID from the **verified token**, never from arguments; per-tenant tests; handle binding `<user_id>:<handle>` [13] |
| **Malicious package / supply chain** (MCP04) | Typosquatted or backdoored server | `postmark-mcp` on npm (Sep 2025): v1.0.16 silently BCC'd every email to an attacker domain; 1,643 downloads before removal (Koi Security) [57] | Install from verified publishers; pin exact versions + lockfiles/digests; internal mirror; SBOM; registry namespace checks |
| **Client/proxy RCE via OAuth metadata** | Malicious server returns crafted `authorization_endpoint` | `mcp-remote` **CVE-2025-6514** (CVSS 9.6; 0.0.5–0.1.15, fixed 0.1.16; JFrog, Jul 2025) → OS command injection [56] | Clients: allow only http(s) schemes, never shell-open URLs [13]; connect only to trusted servers over HTTPS |
| **Local server exposed to the browser** (DNS rebinding) | A web page drives a localhost server | MCP Inspector **CVE-2025-49596** (CVSS 9.4, fixed 0.14.1) [55]; TS SDK **CVE-2025-66414** (rebinding protection off by default, fixed 1.24.0) [58] | Bind 127.0.0.1; validate Host/Origin (v2 SDK defaults); require auth even locally |
| **STDIO config → command execution** | Untrusted MCP *configuration* (command + args) executes arbitrary commands | OX Security (Apr 2026) reported "by design" STDIO-config command execution across many MCP-consuming products (e.g., LiteLLM, Flowise, Windsurf CVEs). **Anthropic called the behavior "expected"** and declined a protocol change [59] | Treat MCP config as code: review, sign, allow-list; never let a model or web input write MCP config; sandbox launched servers [13] |
| **Command injection inside tools** (MCP05) | Tool passes model-supplied strings to a shell/SQL | Generic; flagged by Willison: avoid unescaped `os.system()` [52] | No shells; parameterized queries; strict schemas (`pattern`, `enum`, `maxLength`) |
| **SSRF** | Server (or client during OAuth discovery) fetches attacker-chosen URLs, e.g. `169.254.169.254` | Spec [13] | Egress proxy/allow-list; block private ranges; don't hand-roll IP parsing [13] |
| **Shadow MCP servers** (MCP09) | Unsanctioned servers on endpoints | OWASP [50] | Inventory; host allow-lists (VS Code/GitHub enterprise policy, Claude org connectors) |

*Flag on the OX Security item:* the THN article's CVE list has inconsistencies (it lists 11 entries under "10 vulnerabilities", and one CVE number appears twice) [59]. Cite it as a vendor research claim, not as settled fact.

### 8.2 OWASP references
- **OWASP MCP Top 10 (2025 IDs):**
  - MCP01 Token Mismanagement & Secret Exposure
  - MCP02 Privilege Escalation via Scope Creep
  - MCP03 Tool Poisoning
  - MCP04 Supply Chain Attacks & Dependency Tampering
  - MCP05 Command Injection & Execution
  - MCP06 Prompt Injection via Contextual Payloads
  - MCP07 Insufficient Authentication & Authorization
  - MCP08 Lack of Audit and Telemetry
  - MCP09 Shadow MCP Servers
  - MCP10 Context Injection & Over-Sharing

  Status: the project page says it is in "Phase 3, Beta Release and Pilot Testing" [50].
- **OWASP GenAI Security Project, "A Practical Guide for Secure MCP Server Development"** (16 Feb 2026). It covers secure architecture, strong authN/authZ, strict input validation, session isolation and hardened deployment [51].
- **The spec's own pages:** Security Best Practices [13] and Authorization Security Considerations [11].

### 8.3 Server hardening checklist (use as a handout)
1. **Least privilege.** Use read-only tools by default. Make each action a separate, narrowly scoped tool. Use per-tool OAuth scopes and minimal `scopes_supported` [13]. Put downstream service accounts on narrow roles.
2. **Human confirmation for side effects.** Use elicitation (resolver / `inputRequired`) for irreversible or external actions. Set `readOnlyHint`/`destructiveHint` honestly, but **never rely on hints for enforcement** [6].
3. **Input validation.** Use tight schemas (`pattern`, `enum`, `maxLength`, numeric bounds). Validate again in business logic. Cap argument size: TS `maxToolInputElements`, and 4 MiB default body limits in both SDKs [31][24].
4. **Output hygiene.** Return only the fields needed. Strip secrets and PII. Label untrusted third-party text as data. Keep results small (hosts truncate; Claude Code caps at 25k tokens by default) [42].
5. **AuthN/AuthZ (HTTP).** Use OAuth 2.1 + PRM. **Validate audience/resource.** Use 401 vs 403 correctly. **No token passthrough.** Authorize per call. Derive tenant/user from the token [11][13].
6. **State handles.** Use secure-random handles bound to the user, with an expiry. HMAC/AEAD-protect `requestState` when it affects authorization or logic. Include principal, TTL and request binding [8][13].
7. **Rate limits and timeouts.** Rate limiting is a spec MUST [6]. Add per-user and per-tool quotas. Use the `Mcp-Method`/`Mcp-Name` headers so the gateway or WAF can enforce them without parsing bodies [10].
8. **Audit.** Write structured logs of who, tool, redacted args, outcome and latency, with correlation IDs. Use OpenTelemetry traces [3]. Ship logs to your SIEM. This addresses OWASP MCP08 [50].
9. **Network.** Bind localhost for local servers. Enforce the Host/Origin allow-list. Use TLS everywhere. Use an **egress allow-list** (only the ticketing API's domain) via proxy or network policy [13].
10. **Secrets.** Get them from the environment or a secrets manager. Never put them in tool args, `x-mcp-header`, or logs. Rotate them. Beware the Inspector's plaintext fallback store [41].
11. **Supply chain.** Pin exact versions with lockfiles (`uv.lock`, `package-lock.json`). Pin container images by digest. Generate an SBOM. Mirror dependencies internally. Pin third-party MCP servers too [57].
12. **Isolation.** Run in a container as non-root, with a read-only root filesystem, dropped capabilities, and no host mounts beyond the needed scope. VS Code's stdio sandbox is an option for local use [44].

---

## 9. Packaging, deploying and change control

### 9.1 Dockerfile (Python, Streamable HTTP)
```dockerfile
# syntax=docker/dockerfile:1
# Pin by digest in production: FROM python:3.13-slim@sha256:<digest>
FROM python:3.13-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY server.py app.py ./
RUN useradd --uid 10001 --no-create-home mcp
USER 10001
ENV PATH="/app/.venv/bin:$PATH" \
    MCP_ALLOWED_HOSTS="mcp.example.gov,mcp.example.gov:*"
LABEL io.modelcontextprotocol.server.name="gov.example/ticket-desk"
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
```
Run it hardened, for example:
```bash
docker run --read-only --cap-drop ALL --security-opt no-new-privileges \
  -e TICKET_API_TOKEN --network mcp-egress -p 127.0.0.1:8000:8000 ticket-desk:1.0.0
```
- Put TLS termination, OAuth token validation and rate limiting at the gateway.
- `--network mcp-egress` stands for a network whose egress proxy allows only the ticketing API.
- The `LABEL` is how the MCP Registry verifies OCI image ownership [49].
- *Notes:* this Dockerfile was not built during research. The `uv` image tag and the base digest are placeholders to pin. For a **stdio** container (e.g., for Docker-based local hosts), use `CMD ["python","server.py"]` and launch with `docker run -i --rm ...` from the host config.

### 9.2 Publishing
- **PyPI:** add `<!-- mcp-name: io.github.you/ticket-desk -->` to the README, then `uv build && uv publish` [49].
- **npm:** add `"mcpName": "io.github.you/ticket-desk"` to `package.json`, then `npm publish --access public` [48].
- **Registry** [48]:
  1. Install `mcp-publisher` (`brew install mcp-publisher`, or a release binary).
  2. Run `mcp-publisher init` to create `server.json` (schema `2025-12-11`).
  3. Run `mcp-publisher login github` (or DNS/HTTP for your own domain).
  4. Run `mcp-publisher publish`.
  5. Verify with `curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=..."`.

  The name in `server.json` must match `mcpName`/`mcp-name`/the OCI label. GitHub Actions automation is documented.
- **Internal/government:** publish to an internal package mirror and a **private registry** (same OpenAPI shape), not the public registry. Public publication of internal servers is neither needed nor supported [47].

### 9.3 Versioning tool definitions and change control
- **Treat the tool surface as an API contract.** Tool names, descriptions, input/output schemas and annotations are what the model sees. A description edit can change model behavior, and an unreviewed edit is indistinguishable from a rug pull [52].
- **Semantic versioning** for the server package and `serverInfo.version`:
  - *major* = removed/renamed tool or breaking schema change;
  - *minor* = new tool or optional parameter;
  - *patch* = no change to `tools/list`.
- **Golden-file test:** in CI, run `npx @modelcontextprotocol/inspector --cli <server> --method tools/list --format json` (or the SDK's in-memory client) and diff against a committed snapshot. Any diff needs security and product review, like a firewall rule change.
- **Deterministic ordering and caching:** list results carry `ttlMs`/`cacheScope`, and the spec recommends deterministic tool order [3][6]. Plan cache TTLs so clients pick up approved changes. Emit `notifications/tools/list_changed` to `subscriptions/listen` subscribers when the set changes [6].
- **Deprecate, don't delete.** Mirror the spec's own policy: announce, keep the old tool for a defined window, then remove [1].
- **Pin consumers too.** Hosts and agents should pin server versions/digests. The OpenAI Agents SDK's `cache_tools_list` should be paired with deliberate invalidation [45].

---

## 10. Hands-on lab (90 minutes), check questions, misconceptions

### 10.1 Suggested 90-minute lab outline
Prerequisites (send ahead):
- Python 3.10+ with `uv`, **or** Node 20+.
- Node **22.19+** for the Inspector.
- Claude Desktop/Claude Code, or VS Code + Copilot.
- Pre-pull dependencies for networks with restricted egress.

| Time | Block | Activities | Facilitator notes |
|---|---|---|---|
| 0–10 | **Why MCP; mental model** | Host/client/server; tools vs resources vs prompts; demo an existing server in a host | Lead with the "2026-07-28 changed everything" warning about stale tutorials |
| 10–20 | **Wire tour** | Run Inspector against the finished server; watch `server/discover`, `tools/list`, `tools/call` JSON; curl one request | Point at `_meta`, `resultType`, `Mcp-Method` header |
| 20–40 | **Build 1: read-only tool** | Scaffold project; implement `get_ticket` with schema constraints + structured output; run via Inspector; try a bad ID | Checkpoint: invalid ID returns `isError`, not a crash. Common failure: `print()` on stdio |
| 40–55 | **Build 2: action + confirmation** | Implement `close_ticket` with elicitation; test accept **and** decline | Show the infinite-loop bug if decline isn't handled (TS) |
| 55–65 | **Build 3: resource + prompt; connect a host** | Add resource template + prompt; register in Claude Code/Desktop or VS Code; drive it in natural language | Absolute paths; restart host; Agent mode in Copilot |
| 65–75 | **Go remote** | Switch to Streamable HTTP; hit with Inspector `--transport http`; demonstrate 421/403 on wrong Host; discuss OAuth flow (diagram, no live IdP) | Optional: `requireBearerAuth` stub |
| 75–85 | **Red-team mini-exercise** | Pairs: (a) poison a description and watch the model's behavior; (b) return prompt-injected text from `get_ticket`; (c) diff `tools/list` in CI to catch it | Use only lab data; discuss mitigations from 8.3 |
| 85–90 | **Wrap + check questions** | 6 questions below; hand out hardening checklist + Dockerfile | Point to OWASP MCP Top 10 and spec security page |

**Stretch goals:**
- Replace the dict with a real read-only API.
- Add an audit log line and an OpenTelemetry span.
- Write a pytest/TS test for the decline path.
- Containerize with the Dockerfile.
- Publish to a private registry.

### 10.2 Six check questions (with answers)
1. **Q:** In 2026-07-28, how does a server learn the client's protocol version and capabilities, now that `initialize` is gone?
   **A:** From `_meta` on *every* request: `io.modelcontextprotocol/protocolVersion` and `io.modelcontextprotocol/clientCapabilities`. Clients may also call `server/discover` up front to learn the *server's* versions and capabilities [3][5].
2. **Q:** Your stdio server works when run by hand but the host shows it as failed. What's the most likely cause, and the fix?
   **A:** Non-protocol output on **stdout** (e.g., `print`/`console.log`), which corrupts JSON-RPC. Log to stderr. Also check absolute paths and env vars in the host config [9][18].
3. **Q:** A tool's `destructiveHint` is `false`. Can the host safely auto-approve it?
   **A:** Not on that basis alone. Annotations are **untrusted hints** unless the server is trusted, and they never enforce anything. Enforcement belongs in server-side authorization, scopes and confirmation [6][7].
4. **Q:** Why must an MCP server never forward the bearer token it received to a downstream API?
   **A:** That is **token passthrough**, which the spec forbids. The token's audience is the MCP server. Forwarding it bypasses downstream controls, breaks audit and trust boundaries, and turns the server into an exfiltration proxy. The server validates its own token and uses separate credentials (e.g., token exchange) downstream [11][13].
5. **Q:** In 2026-07-28, how does a server get a human's confirmation in the middle of a `tools/call`?
   **A:** Via **MRTR**. It returns `resultType: "input_required"` with an `elicitation/create` in `inputRequests` (plus an optional integrity-protected `requestState`). The client asks the user and **retries** the call with `inputResponses` and a new request id. Server-initiated requests are no longer allowed [8].
6. **Q:** Name two controls that would have limited the `postmark-mcp` incident, and two that would have limited the GitHub "toxic agent flow".
   **A:** *postmark-mcp:* pin exact versions or digests and review diffs before upgrading; install only from verified publishers or an internal mirror; restrict egress so mail can't go to unknown domains [57]. *GitHub flow:* least-privilege tokens (one repo, read-only); require human confirmation for writes such as creating PRs; don't mix private-data access with untrusted input in one session; monitor and scan tool calls [53].

### 10.3 Common misconceptions
| Misconception | Reality |
|---|---|
| "MCP is an Anthropic-only/Claude-only thing." | It's an open spec under the Linux Foundation's AAIF, supported by OpenAI, Microsoft/GitHub, Google, AWS, Cursor and others [15][2][45][46] |
| "MCP servers need `initialize` and sessions." | Not since 2026-07-28. That shape is now "legacy", which v2 SDKs still serve for older clients [3][39] |
| "FastMCP / `@modelcontextprotocol/sdk` is the current API." | v2: `MCPServer` (Python), `@modelcontextprotocol/server` (TS). v1 is maintenance-only [20][29] |
| "Tool annotations are a security control." | They're untrusted hints. Hosts use them for UX, but enforcement is your server's job [6] |
| "If it's local (stdio), it's safe." | Local servers run with the user's privileges. DNS rebinding, malicious configs and supply-chain attacks all hit local setups [13][55][59] |
| "The model only does what the user asked." | Tool descriptions and tool *results* are both prompt-injection channels [52][53] |
| "Just pass the user's token through to the backend." | Forbidden. Validate your own audience and get separate downstream credentials [11][13] |
| "The MCP Registry vets servers for security." | It verifies namespaces and hosts metadata only. Scanning is delegated to package registries and aggregators, and it's still in preview [47] |
| "SSE is how remote MCP works." | HTTP+SSE is deprecated. Use Streamable HTTP [10] |
| "Sampling/Roots are the way to call an LLM / scope files." | Both are deprecated in 2026-07-28. Call LLM APIs directly, and pass paths as arguments or config [3] |
| "More tools = more capable agent." | More surface = more risk and worse tool selection. Keep tools few, focused and well described [13][6] |

---

## Uncertainties and items to re-verify before delivery
1. **Host support for 2026-07-28.** We did not confirm which hosts (Claude apps, VS Code, ChatGPT, Cursor) natively speak the stateless era versus `initialize`. v2 SDK servers handle both.
2. **Registry status** is "preview" (no GA date found) [47].
3. **OWASP MCP Top 10** is in beta. Item IDs carry ":2025" and could be renumbered [50].
4. **TS legacy shim over stateless HTTP:** elicitation for 2025-era clients is documented and tested in-process. We did not test it against a real legacy host over HTTP [34][35].
5. **Python `server/discover`** on our test server advertised only `["2026-07-28"]`, yet the SDK still accepted legacy `initialize` (observed). Clients that rely solely on `supportedVersions` may behave differently.
6. **Tasks extension and EMA** SDK support varies by SDK and version. Check release notes.
7. **VS Code config locations** are in flux (`.vscode/mcp.json` labeled deprecated in the guided flow) [44].
8. **ChatGPT Developer Mode** lists SSE as supported even though the protocol deprecates it [46].
9. **Dockerfile** (9.1) was authored but not built during research. Pin the base image digest and the `uv` image tag yourself.
10. **OX Security (Apr 2026)** is vendor research, reported with a CVE-list inconsistency [59].

---

## Sources
1. MCP Specification: Versioning (current = 2026-07-28; deprecation windows). https://modelcontextprotocol.io/specification/versioning
2. MCP Blog: "The 2026-07-28 Specification" (28 Jul 2026). https://blog.modelcontextprotocol.io/posts/2026-07-28/
3. MCP Spec 2026-07-28: Key Changes (changelog). https://modelcontextprotocol.io/specification/2026-07-28/changelog
4. MCP Spec 2026-07-28: Architecture. https://modelcontextprotocol.io/specification/2026-07-28/architecture
5. MCP Spec 2026-07-28: Discovery (`server/discover`). https://modelcontextprotocol.io/specification/2026-07-28/server/discover
6. MCP Spec 2026-07-28: Tools. https://modelcontextprotocol.io/specification/2026-07-28/server/tools
7. MCP Spec 2026-07-28: schema.ts (ToolAnnotations, methods). https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/schema.ts
8. MCP Spec 2026-07-28: Multi Round-Trip Requests. https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr
9. MCP Spec 2026-07-28: stdio transport. https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio
10. MCP Spec 2026-07-28: Streamable HTTP transport. https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
11. MCP Spec 2026-07-28: Authorization. https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
12. MCP Spec 2026-07-28: Authorization Server Discovery. https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery
13. MCP Docs: Security Best Practices (2026-07-28). https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
14. MCP Spec 2025-11-25: Key Changes. https://modelcontextprotocol.io/specification/2025-11-25/changelog
15. MCP Blog: "MCP joins the Agentic AI Foundation" (9 Dec 2025). https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/ (see also https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
16. AAIF Blog: "MCP 2026-07-28: What's changing and how to migrate" (RC-era post). https://aaif.io/blog/mcp-2026-07-28-whats-changing-and-how-to-migrate
17. MCP Docs: SDKs and tiers. https://modelcontextprotocol.io/docs/2026-07-28/sdk
18. MCP Docs: Build an MCP server (2026-07-28 quickstart). https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server
19. Python SDK repository/README. https://github.com/modelcontextprotocol/python-sdk
20. Python SDK: Migration Guide v1 → v2. https://py.sdk.modelcontextprotocol.io/migration/ (v2.0.0 release notes summarized at https://newreleases.io/project/github/modelcontextprotocol/python-sdk/release/v2.0.0)
21. Python SDK docs: Tools. https://py.sdk.modelcontextprotocol.io/servers/tools/
22. Python SDK docs: Resources. https://py.sdk.modelcontextprotocol.io/servers/resources/
23. Python SDK docs: Elicitation (resolvers). https://py.sdk.modelcontextprotocol.io/handlers/elicitation/
24. Python SDK docs: Running your server. https://py.sdk.modelcontextprotocol.io/run/
25. Python SDK docs: Testing. https://py.sdk.modelcontextprotocol.io/get-started/testing/
26. Python SDK docs: Deploy & scale (transport_security). https://py.sdk.modelcontextprotocol.io/run/deploy/
27. Python SDK docs: Handling errors. https://py.sdk.modelcontextprotocol.io/servers/handling-errors/
28. PyPI: mcp (2.3.0, 2 Oct 2026; 2.0.0, 28 Jul 2026). https://pypi.org/project/mcp/
29. TypeScript SDK repository/README (v2, v1.x support window). https://github.com/modelcontextprotocol/typescript-sdk
30. TS SDK docs: Build your first server. https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/get-started/first-server.md
31. TS SDK docs: Tools. https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/servers/tools.md
32. TS SDK docs: Resources. https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/servers/resources.md
33. TS SDK docs: Prompts. https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/servers/prompts.md
34. TS SDK docs: input_required. https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/servers/input-required.md
35. TS SDK docs: Serve over HTTP. https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/http.md
36. TS SDK docs: Serve with Express. https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/express.md
37. TS SDK docs: Test a server. https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/testing.md
38. TS SDK docs: Plug into a real host (VS Code, Claude Code, Cursor). https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/get-started/real-host.md
39. TS SDK docs: Protocol versions (eras). https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/protocol-versions.md
40. npm: @modelcontextprotocol/server (2.3.1, 5 Oct 2026). https://www.npmjs.com/package/@modelcontextprotocol/server
41. MCP Docs: MCP Inspector (v2; Node ≥ 22.19.0). https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector
42. Claude Code docs: Connect Claude Code to tools via MCP. https://code.claude.com/docs/en/mcp
43. Claude docs: Third-party connectors with remote MCP. https://claude.com/docs/connectors/custom/remote-mcp
44. VS Code docs: MCP configuration reference; MCP servers. https://code.visualstudio.com/docs/agents/reference/mcp-configuration and https://code.visualstudio.com/docs/copilot/customization/mcp-servers
45. OpenAI Agents SDK (Python): MCP. https://openai.github.io/openai-agents-python/mcp/
46. OpenAI: ChatGPT Developer mode. https://developers.openai.com/api/docs/guides/developer-mode
47. MCP Registry: About. https://modelcontextprotocol.io/registry/about
48. MCP Registry: Quickstart (mcp-publisher). https://modelcontextprotocol.io/registry/quickstart
49. MCP Registry: Package types and ownership verification. https://modelcontextprotocol.io/registry/package-types
50. OWASP MCP Top 10. https://owasp.org/www-project-mcp-top-10/
51. OWASP GenAI Security Project: A Practical Guide for Secure MCP Server Development (16 Feb 2026). https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/
52. Simon Willison, "Model Context Protocol has prompt injection security problems" (9 Apr 2025; summarizes Invariant Labs tool-poisoning, rug-pull, WhatsApp research). https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/
53. Invariant Labs, "GitHub MCP Exploited: Accessing private repositories via MCP" (26 May 2025). https://invariantlabs.ai/blog/mcp-github-vulnerability
54. BleepingComputer, "Asana warns MCP AI feature exposed customer data to other orgs" (18 Jun 2025). https://bleepingcomputer.com/news/security/asana-warns-mcp-ai-feature-exposed-customer-data-to-other-orgs/
55. Oligo Security, "Critical RCE in Anthropic MCP Inspector (CVE-2025-49596)" (27 Jun 2025). https://www.oligo.security/blog/critical-rce-vulnerability-in-anthropic-mcp-inspector-cve-2025-49596
56. JFrog, "CVE-2025-6514: Critical mcp-remote RCE" (9 Jul 2025). https://jfrog.com/blog/2025-6514-critical-mcp-remote-rce-vulnerability/
57. The Hacker News, "First Malicious MCP Server Found Stealing Emails" (postmark-mcp; 29 Sep 2025). https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html
58. NVD, CVE-2025-66414 (TS SDK DNS-rebinding default; fixed 1.24.0). https://nvd.nist.gov/vuln/detail/CVE-2025-66414
59. The Hacker News, "Anthropic MCP Design Vulnerability Enables RCE…" (OX Security research; 20 Apr 2026). https://thehackernews.com/2026/04/anthropic-mcp-design-vulnerability.html
