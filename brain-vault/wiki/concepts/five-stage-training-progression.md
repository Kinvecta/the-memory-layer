---
type: concept
summary: The guide's five-stage training path ordered by how much control the AI has - chat with saved instructions, API in a container, containerized workflows, tool calling, and harness with skills - with exercises, exit criteria, risks and how far each role goes.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s5-apis-endpoints-and-containers]]", "[[raw/transcripts/s8-agents-skills-and-running-the-program]]"]
related: ["[[ai-training-guide]]", "[[train-the-trainer-series]]", "[[apis-and-endpoints]]", "[[workflows]]", "[[tool-calling]]", "[[agent-skills]]", "[[ai-agents]]", "[[containerization]]", "[[measuring-training-results]]"]
aliases: [five stages, training progression, Stages 1-5]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Five-Stage Training Progression

**TL;DR:** Teams learn AI in five stages ordered by how much control the AI has, giving it more only as people prove they can contain and check it. Each stage adds one capability and one new risk, so when something breaks people know which layer to check, and every stage after chat runs in a container. Teams limited to chat and API can stop at Stage 3 and still have working automation.

## What it is
The training spine of the [[ai-training-guide]] ([[source-ai-training-guide]] §5.1). Control runs: none in chat, none in a single API call, none in a scripted workflow, some once it calls tools, most inside a harness with skills.

| Stage | Learn | Exercise | Ready when | New risk |
|---|---|---|---|---|
| 1. Chatbot + saved instructions | Rules of use, definitions, prompting, verifying, reusable instructions | Summarize a real non-sensitive memo, check every fact, save the prompt | Usable draft in 1-2 tries, errors caught, one saved instruction | Wrong tool for the data |
| 2. API in a container | API basics, keys, choosing the endpoint, building a container, limiting network | Containerize a script that sends one prompt plus a document | Builds, reaches only the approved endpoint, keys never in code or logs | Leaked keys |
| 3. Workflow + container + API | Chaining fixed steps, triggers, validation, logging, human review, MCP servers as fixed steps | Scripted status-report workflow on a schedule | Repeatable, flags bad output, logs every run | Bad output passed on |
| 4. Tool calling in a container | Read-only vs action tools, approval gates, MCP | Read-only lookup tool, then an approval-gated action tool, then package the lookup as an MCP server | Right tool picked, MCP server inside the container, no unapproved action | Unapproved actions |
| 5. Harness + skills + container | Containerized harness, skills from Stage 1 instructions, permissions, testing | Package a team skill, install it, test in a second harness | Triggers correctly, scripts contained, actions need approval | Untested skills |

Risks per stage are from [[source-s8-agents-skills-and-running-the-program]] [3:49]; the rest from [[source-ai-training-guide]] §5.1.

## Why it matters
Stacking one risk per stage keeps debugging tractable and matches autonomy to proven skill. It also maps to what an environment allows: chat only = Stage 1; chat + API = Stages 1-3; + tool calling = 1-4; full harness = 1-5 ([[source-ai-training-guide]] §2.1; [[source-s5-apis-endpoints-and-containers]] [3:56]). Low-code tools such as Power Automate are acceptable at Stage 3 if the tool is authorized.

## How it works
**How far each role goes** ([[source-ai-training-guide]] §5.2; planning estimates):

| Role | Target | Time | Success looks like |
|---|---|---|---|
| All personnel | Stage 1 | 2-3 hours | Uses an approved tool safely on a real task; saves one reusable instruction |
| Leaders | Stage 1 + demo of 2-5 | Half day | Names one pilot with a success measure |
| Analysts and operators | Stage 3 (4 if moving toward agents) | 2-3 days | Ships a containerized or approved low-code workflow on saved prompts |
| Technical staff | Stage 5 | 5-8 days | Runs a containerized harness with tested skills and approval gates |

Techniques are taught in stage order, each reusing what the previous built: [[safe-prompting]] -> [[apis-and-endpoints]] -> [[workflows]] -> [[tool-calling]] / [[model-context-protocol]] -> [[agent-skills]] and [[ai-agents]].

## In practice
- The facilitator course map in the guide runs six sessions (60 to 240 minutes each); the produced [[train-the-trainer-series]] expands this to eight sessions plus two deep dives.
- All Stage 2-5 exercises use one prepared sandbox: pre-scanned base image, per-student low-limit keys, made-up documents (one with a planted injection), sample database, starter library, containerized harness, low-code sandbox, sample MCP server ([[source-ai-training-guide]] §5.2).
- Judge success by changed work, not completions ([[measuring-training-results]]).

## See also
[[ai-training-guide]] · [[train-the-trainer-series]] · [[containerization]] · [[measuring-training-results]]
