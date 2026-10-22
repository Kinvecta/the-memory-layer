---
type: concept
summary: Prompt injection is when instructions hidden in content the AI reads take over its behavior; OWASP ranks it the number-one LLM risk, and it is stopped by layered defenses and by removing one of three ingredients.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s7-tools-mcp-and-prompt-injection]]", "[[raw/transcripts/dda-build-an-mcp-server]]", "[[raw/research/mcp-build-brief]]"]
related: ["[[tool-calling]]", "[[model-context-protocol]]", "[[ai-governance-and-controls]]", "[[ai-agents]]", "[[egress-control-and-firewalls]]", "[[agent-skills]]", "[[building-an-mcp-server]]", "[[safe-prompting]]"]
aliases: ["indirect prompt injection", "tool poisoning"]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Prompt injection

**TL;DR:** Prompt injection is when instructions hidden inside content the AI reads (a PDF, web page, email, tool result or tool description) take over its behavior. No single defense stops it; layers do, and the attack also fails if you remove any one of its three ingredients: private data, untrusted content, and a way out. The risk grows with every training stage, because a chatbot only writes a bad summary while an agent with an email tool can actually send data.

## What it is
OWASP ranks prompt injection the number-one risk for LLM applications, because models cannot reliably tell the instructions their builders wrote from text a user or document supplies ([[source-ai-training-guide]] §4.1). In the **indirect** form, the attack is planted in documents, web pages, emails or database records the model later pulls in.

**Worked example** (guide §4.1; [[source-s7-tools-mcp-and-prompt-injection]] 3:28): a workflow summarizes vendor proposals. One PDF has white-on-white text telling the model to rate it highest and attach the evaluation sheet to its reply. Treating content as data helps but is not enough: the model is fooled and asks to reply to the vendor. Least access plus approval blocks it, because the reply needs a person.

## Why it matters
The risk scales with autonomy ([[five-stage-training-progression]]). Once AI can act through [[tool-calling]], hidden text becomes real actions. MCP adds channels: tool descriptions and tool results are both injection paths ([[source-mcp-build-brief]] §10.3). Real cases:
- **Tool poisoning** (Invariant Labs, Apr 2025): an innocent-looking `add()` tool's description told the model to read SSH keys and config and smuggle them out (brief §8.1).
- **Injection via results** (GitHub "toxic agent flow", 26 May 2025): a malicious public issue made an agent copy private-repo data into a public pull request.
- **Rug pull**: a tool approved as safe later changes its definition.

## How it works
**Three ingredients** (S7 4:16): private data (something worth stealing), untrusted content (text an attacker can write), and a way out (a tool that can send, post or fetch outside). With all three, the path runs straight through. **Remove any one and the attack fails.**

**Six layered defenses** (S7 4:41; guide §4.1):
1. Treat everything the model reads (files, web pages, tool results, outside skills) as data, never instructions.
2. Least access: tools get only what they need.
3. Human approval for any action that sends, changes or deletes.
4. Validate outputs: expected format, no unexpected links or recipients.
5. Container network limited to approved endpoints, so a hijacked model has nowhere to send data ([[egress-control-and-firewalls]]).
6. Review third-party skills line by line before installing ([[agent-skills]]).

In the S7 demo the attack gets past layers one and two and is stopped at layer three. Four and five are backups; six happens before install.

> [!warning] The AI-chosen URL
> Fetching a web page is a read, but if the AI picks the address it can leak data through the address itself. It runs only if the harness restricts destinations (S7 6:02).

## In practice
- **Server side** ([[building-an-mcp-server]]): peer-review tool descriptions like code; snapshot the tool list and fail the build on any change; confirm every write; least-privilege tokens.
- **Run time** (guide §4.1): monitor for injection signs such as unexpected tool calls, recipients or links; keep a kill switch.
- **Teaching aha** ([[source-dda-build-an-mcp-server]] 18:09): the poisoned description and the injected result never touch your code, yet they change what the model does. The schema, the confirmation and the snapshot are what catch them.

## See also
[[ai-governance-and-controls]] · [[tool-calling]] · [[model-context-protocol]] · [[ai-agents]] · [[hallucination-and-verification]]
