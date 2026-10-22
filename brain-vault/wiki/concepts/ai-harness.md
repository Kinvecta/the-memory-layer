---
type: concept
summary: The harness is the app or platform around a model (interface, instructions, memory, permissions, tool loop, logging) that decides what the model can see and do; covers the six harness types and how to size one up.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s1-what-an-llm-is]]"]
related: ["[[large-language-model]]", "[[agent-skills]]", "[[tool-calling]]", "[[model-context-protocol]]", "[[apis-and-endpoints]]", "[[chatbot-workflow-agent]]", "[[containerization]]", "[[ai-governance-and-controls]]"]
aliases: [harness, agent harness]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# AI harness

**TL;DR:** The harness is the app or platform wrapped around a model: interface, instructions, memory, permissions, logging, and the loop that lets the model use tools. The harness, not the model, decides what AI can see and do, which is why security approves the harness. When your own software calls a model through an API, your software becomes the harness.

## What it is
| Part | What it is |
|---|---|
| Harness | The app or platform around the model: interface, instructions, memory, permissions, tool loop. Examples: Claude.ai, ChatGPT, Gemini app, Claude Code, a company's approved AI platform |
| Model | The engine that reads, reasons and writes ([[large-language-model]]) |
| Skill | Packaged instructions and resources the harness loads when a task matches ([[agent-skills]]) |
| Tool | A function the harness lets the model call ([[tool-calling]]) |
| API | Programmatic access with no vendor chat app in between ([[apis-and-endpoints]]) |

Source: [[source-ai-training-guide]] §2.1.

> [!tip] Rule of thumb
> The model thinks, skills teach it how, tools let it act, and the harness decides which of those it gets. An API lets your own software reach the model directly, which makes that software the harness ([[source-ai-training-guide]] §2.1).

## Why it matters
The same model behaves differently in different harnesses ([[source-ai-training-guide]] §2.1). Session 1 shows one model in three harnesses: a chat app (sees what you paste plus any enabled search or connectors; low reach, acts alone very little), a coding agent (reads and edits files, runs commands, loops; high reach, acts alone a lot), and your own script (sees only what your code sends; you decide reach and own every control). "Same engine. Different reach. Different risk" ([[source-s1-what-an-llm-is]] [5:08]).

## How it works
Inside the harness: instructions added to every request, memory it saves and feeds back, permissions and approval gates, and logging. The model only sees what the harness hands it ([[source-s1-what-an-llm-is]] [4:22]). With MCP ([[model-context-protocol]]), the model never talks to a tool server directly: the harness connects, lists tools, passes descriptions to the model, checks each request, runs approved ones and returns results, so permissions, approvals and logging all live in the harness ([[source-ai-training-guide]] §2.1). Retrieval works the same way: the harness picks finders and merges results ([[how-ai-finds-your-data]]).

## Six types of harness
1. Chat assistants (Claude.ai, ChatGPT, Gemini app).
2. AI built into existing tools: email, documents, ticketing, case systems.
3. Your organization's approved platform or gateway, several models behind one front door.
4. Coding and agent tools (Claude Code, Codex CLI, Gemini CLI) that read files, run commands, loop toward a goal.
5. Open-source agents you host yourself: flexible, with real supply-chain risk.
6. Your own software calling the model by API: you are the harness.

"Products change every month. Learn the categories, not the brand names" ([[source-s1-what-an-llm-is]] [5:50]).

## Sizing one up
Ask two questions: what can it reach, and how much does it act alone? Chat assistants sit low on both; built-in AI slightly higher; organization platforms in the middle; coding/agent tools and open-source agents high on both; your own software can land anywhere. The further up and right, the more controls it needs. "If your team can't answer 'what can it reach,' that's your first finding" ([[source-s1-what-an-llm-is]] [6:39]).

## In practice
- Every harness past chat runs in a container ([[containerization]]); harness controls are in [[ai-governance-and-controls]].
- Session 1 audit: for one team tool, name its type, models, reach, autonomy, and who approved it for what data.

## See also
[[large-language-model]] · [[agent-skills]] · [[tool-calling]] · [[ai-agents]] · [[source-s1-what-an-llm-is]]
