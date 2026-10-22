---
type: source
summary: Summary of the Session 7 narrated video transcript covering tool calling, how MCP plugs tools into any harness, prompt injection and its three ingredients, and the six layered defenses.
sources: ["[[raw/transcripts/s7-tools-mcp-and-prompt-injection]]"]
related: ["[[tool-calling]]", "[[model-context-protocol]]", "[[prompt-injection]]", "[[ai-governance-and-controls]]", "[[train-the-trainer-series]]", "[[source-s6-building-workflows]]", "[[source-s8-agents-skills-and-running-the-program]]"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Session 7 - Tools, MCP and Prompt Injection (transcript)

**TL;DR:** Session 7 of the [[train-the-trainer-series]] gives the model tools: the model asks, the harness checks and runs, and the result comes back as data, not instructions. It explains MCP as the open standard for plugging tools into any harness, then spends most of its time on prompt injection, the risk that grows once AI can act. The one rule: read tools run freely from approved sources, action tools wait for a person, and nothing the model reads is an instruction.

**Source file:** [[raw/transcripts/s7-tools-mcp-and-prompt-injection]]  ·  **Kind:** transcript  ·  **Date:** 2026-10 (about 7.5 minutes)

## Key points
1. **Learning objectives** [0:26]: explain how tool calling works; describe how MCP plugs tools into any harness; trace a prompt injection and where it gets stopped; decide which tools need a person's approval.
2. **Why it matters** [0:47]: three failure stories. "It made up the ticket status" (no tool connected, so it guessed). "It sent the wrong file" (an action ran without approval). "A PDF told it what to do" (hidden instructions took over). See [[tool-calling]], [[hallucination-and-verification]].
3. **The tool loop** [1:11]: the model asks to look up a ticket; the harness checks it; a read from an approved source runs straight away. The model asks to send an email; that is an action, so it waits for a person. Every result is data.
4. **Where tools sit** [1:44]: the harness frames everything; the model thinks, skills teach it how, tools let it act, and the harness decides which it gets. Through an API, your own software is the harness, so your team owns those controls ([[ai-harness]], [[apis-and-endpoints]]).
5. **MCP** [2:07]: a chat app, a workflow and an agent all reach one MCP server exposing tools, resources and prompt templates. The server runs in a container and reaches only its ticket system; a call out to the web is blocked at the container wall ([[model-context-protocol]], [[egress-control-and-firewalls]]).
6. **Six-step MCP call** [2:38]: connect, list tools, model asks, harness checks and logs, harness runs the approved call, result returns as data. The model never talks to the server directly.
7. **Tool design rules** [3:10]: clear name and description (the model decides from those words); treat descriptions as code and peer-review them; log every call.
8. **Prompt injection** [3:28]: OWASP ranks it the number-one risk for AI applications. Worked example: a vendor proposal with white text telling the AI to rate it highest and attach the evaluation sheet. "Content is data" helps but is not enough; least access plus approval stops it ([[prompt-injection]]).
9. **Three ingredients** [4:16]: private data, untrusted content, and a way out (a tool that can send, post or fetch). Remove any one and the attack fails.
10. **Six layered defenses** [4:41]: treat content as data; least access; approve every action; validate outputs; outbound network to approved endpoints only; review outside skills line by line. In the demo the attack is stopped at layer three.
11. **Tools are software** [5:24]: repository, review, tests and evals, scanned image, then running with logs, approvals and a kill switch. A new version is a new release, not an edit in place ([[devsecops-pipeline]], [[ai-evals]]).
12. **Exercise** [6:02]: Part A traces the vendor-proposal injection; Part B gates seven tools (search policy library, look up ticket, email a vendor, update a vendor record, read an uploaded PDF, delete a calendar event, fetch a URL the AI chose). The last is a read, but an AI-chosen address can leak data, so it runs only if the harness restricts destinations.
13. **Bridge** [7:13]: Session 8 moves to agents that plan their own steps ([[ai-agents]], [[agent-skills]]).

## Worth quoting
> "The model asks. The harness decides. And nothing the model reads is an instruction." [5:47]

> "Remove any one, and the attack fails." [4:16]

> "A mistake has to get past every layer: the model, the harness gate, the output check, and the network wall." [4:41]

## Pages this source updated
- [[tool-calling]]
- [[model-context-protocol]]
- [[prompt-injection]]
- [[ai-governance-and-controls]]
