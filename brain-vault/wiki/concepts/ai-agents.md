---
type: concept
summary: An AI agent pursues a goal by choosing its own steps and using tools in a plan-act-check loop; covers when to use one, Stage 5 guardrails (container, logging, approval gates, step review) and common misuse of the term.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s8-agents-skills-and-running-the-program]]"]
related: ["[[chatbot-workflow-agent]]", "[[agent-skills]]", "[[tool-calling]]", "[[ai-harness]]", "[[workflows]]", "[[prompt-injection]]", "[[containerization]]", "[[five-stage-training-progression]]"]
aliases: [agent, agentic AI, AI agent]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# AI Agents

**TL;DR:** An agent is an AI system that pursues a goal by choosing its own steps and using tools, looping through plan, act and check until done, then a person reviews. Because mistakes compound across steps, agents belong at Stage 5 only, running in a container with skills, logging and a human approval gate on any action that leaves. Many tasks labeled "agent" are really fixed workflows.

## What it is
The guide defines an agent as "an AI system that pursues a goal by choosing its own steps and using tools" ([[source-ai-training-guide]] Glossary). In the chatbot / workflow / agent split, the AI decides the steps at run time; it "plans, uses tools, checks results, and repeats until done." Example: "Find every contract expiring this quarter and draft renewal notices." Main risk: "mistakes compound across steps and actions" ([[source-ai-training-guide]] §2.1; [[chatbot-workflow-agent]]).

"Agentic" is a spectrum, not yes/no; most agentic tools today are lightly autonomous, and the word "now gets slapped on almost any product" ([[source-ai-training-guide]] Glossary).

## Why it matters
The field is moving "from chat to agents": tools take multi-step actions (search, draft, fill forms, run checks) and people shift from writing every word to reviewing and approving ([[source-ai-training-guide]] §1.3). But "telling AI, workflows and agents apart" is focus area 3; the common gap is "building an agent where a fixed workflow would do" ([[source-ai-training-guide]] §1.4). Agent work also widens exposure to [[prompt-injection]], since the agent reads documents and tool results.

## How it works
An agent is the model plus a [[ai-harness]] that runs a loop: the model requests [[tool-calling]] steps, the harness checks and runs approved ones, results return, and the model plans again. [[agent-skills]] supply the method so the same request runs the same steps; tools supply facts and actions ([[source-ai-training-guide]] §3.4).

**Guardrails shown in Session 8** ([[source-s8-agents-skills-and-running-the-program]] [2:50]):
- The agent runs inside a container ([[containerization]]).
- It plans, reads the tracker, checks rows, loops back to plan the draft and the send.
- Every step goes into the log.
- An attempted email send holds at the approval gate; a person reviews the steps and approves; only then does it leave.

Stage 5 practice rules ([[source-ai-training-guide]] §5.2): package proven saved prompts as skills and test they trigger correctly; require human approval before any action leaves the system; "review the agent's steps, not just its final answer."

## In practice
- Stage 5 exercise: package a team skill, install it in a containerized harness, test it in a second harness. Ready when the skill triggers when it should, its scripts stay inside the container, and actions need approval ([[five-stage-training-progression]]).
- Who goes this far: technical staff and designated power users (5-8 days); everyone else stops earlier.
- Stage 5's characteristic risk is untested skills ([[source-s8-agents-skills-and-running-the-program]] [3:49]).
- "Human in the loop" means a person approves before results are used or actions happen, not a glance after the fact ([[source-ai-training-guide]] Glossary).
- Agents that rewrite their own skills (Hermes) need human approval before an edited skill goes back into use ([[agent-skills]]).

> [!warning] Default to the workflow
> If the path can be drawn in advance, build a [[workflows]] instead; it is easier to authorize and fails more visibly.

## See also
[[chatbot-workflow-agent]] · [[agent-skills]] · [[tool-calling]] · [[ai-governance-and-controls]]
