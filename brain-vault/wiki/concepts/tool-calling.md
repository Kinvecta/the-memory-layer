---
type: concept
summary: Tool calling lets a model ask for a function to fetch facts or take actions while the harness checks, runs and logs it; read tools run freely, action tools wait for a person, and every result is data.
sources: ["[[raw/transcripts/s7-tools-mcp-and-prompt-injection]]", "[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[model-context-protocol]]", "[[prompt-injection]]", "[[ai-harness]]", "[[agent-skills]]", "[[ai-agents]]", "[[five-stage-training-progression]]", "[[building-an-mcp-server]]", "[[ai-governance-and-controls]]"]
aliases: ["function calling", "tool use", "tools"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Tool calling

**TL;DR:** Tool calling lets the model ask for a function (look up a ticket, search a library, send an email) while your code, the harness, decides whether to run it. Read-only tools run straight away from approved sources; anything that sends, changes or deletes waits for a person; and whatever comes back is untrusted data, not instructions. It is Stage 4 of the [[five-stage-training-progression]].

## What it is
A tool is "a function the harness lets the model call to fetch information or take action" ([[source-ai-training-guide]] §2.1). Examples: web search, reading a file, running code, sending an email. The model never executes anything itself. It emits a request; the [[ai-harness]] checks it, runs it if allowed, and hands the result back. The model can loop several times before answering (§5.2).

A common confusion: assuming the model "knows" something it actually fetched, or assuming it can reach any system. It reaches only what it is connected to (§2.1).

## Why it matters
Tools make AI useful and make mistakes real ([[source-s7-tools-mcp-and-prompt-injection]] 0:47):
- "It made up the ticket status." No tool was connected, so it guessed ([[hallucination-and-verification]]).
- "It sent the wrong file." An action ran without a person approving it.
- "A PDF told it what to do." Hidden instructions took over ([[prompt-injection]]).

With tools, a hijacked model can act, not just write a bad summary. That is why gating lives in the harness.

## How it works
The tool loop (S7 1:11; guide Figure 23): **request, check, approve, run, return.**
1. The model asks for a tool by name with arguments.
2. The harness checks the request and logs it.
3. A read from an approved source runs immediately. An action waits for human approval.
4. The result returns to the model as data.

Through an API, your own software is the harness, so your team owns permissions, approvals and logging (S7 1:44; [[apis-and-endpoints]]).

**Tool design rules** (S7 3:10; guide §5.2):
- Give each tool a clear name, description and input list. The model decides when to call it from those words.
- Treat descriptions as code and peer-review them, because the model reads them as instructions.
- Log every call.
- Start with read-only tools (lookups, searches) before any tool that sends or changes something.
- Package reusable tools as MCP servers so any harness can use them ([[model-context-protocol]]); run each in a container with only the endpoints it needs ([[egress-control-and-firewalls]]).

## In practice
**Gate exercise** (S7 6:02). Decide whether each runs straight away or waits:

| Tool | Gate |
|---|---|
| Search the policy library | Runs (read, approved source) |
| Look up a ticket | Runs |
| Read an uploaded PDF | Runs, but content is untrusted |
| Send an email to a vendor | Waits for a person |
| Update a vendor record | Waits |
| Delete a calendar event | Waits |
| Fetch a web page from a URL the AI chose | Runs only if the harness restricts destinations, because the address itself can leak data |

**Tools plus skills** (§3.4): tools supply facts, actions and ways to check work; skills supply the method ([[agent-skills]]). Given tools alone, the model improvises a different approach each time. Remove the tools and figures are guesses.

> [!tip] Rule of thumb
> "The model asks. The harness decides. And nothing the model reads is an instruction." (S7 5:47)

## See also
[[model-context-protocol]] · [[prompt-injection]] · [[ai-agents]] · [[workflows]] · [[building-an-mcp-server]] · [[ai-governance-and-controls]]
